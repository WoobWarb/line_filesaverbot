import os
import sqlite3
import threading
import gc
import time
import requests
import queue
import shutil
import json
import re
import mimetypes
from datetime import datetime, timedelta
from flask import Flask, request, abort, render_template, redirect, url_for, send_file, send_from_directory, session
from functools import wraps
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, AudioMessage, FileMessage, ImageSendMessage,
    TemplateSendMessage, ButtonsTemplate, URITemplateAction, FollowEvent,
    FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, ButtonComponent, URIAction, SeparatorComponent
)
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google import genai
import google_auth_oauthlib.flow
import logging
import qrcode
from io import BytesIO
from dotenv import load_dotenv
import promptpay  # Local module

load_dotenv()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# In-memory store for PKCE code verifiers
pkce_store = {}

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')  # Fallback global folder ID
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
PROMPTPAY_ID = os.getenv('PROMPTPAY_ID', '0841234567')  # For billing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')  # Fallback global credentials file
DB_FILE = os.path.join(BASE_DIR, 'chat_log.db')
PENDING_DIR = os.path.join(BASE_DIR, 'pending_uploads')
SLIPS_DIR = os.path.join(BASE_DIR, 'slips')

if not os.path.exists(PENDING_DIR):
    os.makedirs(PENDING_DIR)

if not os.path.exists(SLIPS_DIR):
    os.makedirs(SLIPS_DIR)

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin1234')

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'filesaverbot-change-this-in-production')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

last_images = {}  # Map source_id -> filename of the last uploaded image in slips

def reply_text(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

def push_text(target_id, text):
    line_bot_api.push_message(target_id, TextSendMessage(text=text))

def reply_flex_raw(reply_token, alt_text, contents):
    """Send Flex Message bypassing SDK (supports clipboard action)."""
    resp = requests.post(
        'https://api.line.me/v2/bot/message/reply',
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'},
        json={"replyToken": reply_token, "messages": [{"type": "flex", "altText": alt_text, "contents": contents}]}
    )
    if resp.status_code != 200:
        raise Exception(f"LINE API {resp.status_code}: {resp.text}")

def assign_rich_menu(user_id, menu_env_key='RICH_MENU_ID'):
    """ผูก Rich Menu ให้กับ user คนใดคนหนึ่ง"""
    menu_id = os.getenv(menu_env_key, '')
    if not menu_id:
        return
    try:
        line_bot_api.link_rich_menu_to_user(user_id, menu_id)
        logger.info(f"[RICHMENU] Linked {menu_env_key} -> {user_id}")
    except Exception as e:
        logger.warning(f"[RICHMENU] Failed to link {menu_env_key} to {user_id}: {e}")

def unassign_rich_menu(user_id):
    """ถอด Rich Menu ส่วนตัวออกจาก user (กลับไปใช้ default)"""
    try:
        line_bot_api.unlink_rich_menu_from_user(user_id)
        logger.info(f"[RICHMENU] Unlinked from {user_id}")
    except Exception as e:
        logger.warning(f"[RICHMENU] Failed to unlink from {user_id}: {e}")

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
import time

# Cache for GA4
ga4_cache = {'timestamp': 0, 'data': None}

def get_ga4_stats_cached():
    global ga4_cache
    if time.time() - ga4_cache['timestamp'] < 300 and ga4_cache['data']:
        return ga4_cache['data']

    property_id = os.getenv("GA4_PROPERTY_ID")
    if not property_id or property_id == 'ใส่_เลข_PROPERTY_ID_ที่นี่':
        return {'total_views': 0, 'today_views': 0, 'today_users': 0, 'trend': []}

    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "file-saver-479919-feb9641cc74e.json"
        client = BetaAnalyticsDataClient()
        
        req_today = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="screenPageViews"), Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date="today", end_date="today")]
        )
        res_today = client.run_report(req_today)
        today_views = int(res_today.rows[0].metric_values[0].value) if res_today.rows else 0
        today_users = int(res_today.rows[0].metric_values[1].value) if res_today.rows else 0
        
        req_total = RunReportRequest(
            property=f"properties/{property_id}",
            metrics=[Metric(name="screenPageViews")],
            date_ranges=[DateRange(start_date="2020-01-01", end_date="today")]
        )
        res_total = client.run_report(req_total)
        total_views = int(res_total.rows[0].metric_values[0].value) if res_total.rows else 0
        
        req_trend = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="screenPageViews")],
            date_ranges=[DateRange(start_date="6daysAgo", end_date="today")]
        )
        res_trend = client.run_report(req_trend)
        
        trend_data = []
        for row in res_trend.rows:
            raw = row.dimension_values[0].value
            fmt = f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
            trend_data.append((fmt, int(row.metric_values[0].value)))
        trend_data.sort(key=lambda x: x[0])
        
        data = {'total_views': total_views, 'today_views': today_views, 'today_users': today_users, 'trend': trend_data}
        ga4_cache['timestamp'] = time.time()
        ga4_cache['data'] = data
        return data
    except Exception as e:
        print(f"GA4 Error: {e}")
        return {'total_views': 0, 'today_views': 0, 'today_users': 0, 'trend': []}

# --- 1. Database Setup ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_id TEXT,
            user_id TEXT,
            message TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS notify_ids (
            id TEXT PRIMARY KEY
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tenant_config (
            source_id TEXT PRIMARY KEY,
            google_refresh_token TEXT,
            google_folder_id TEXT,
            tier TEXT DEFAULT 'FREE',
            expires_at TEXT,
            created_at TEXT,
            drive_connected_at TEXT
        )
    ''')
    # Migration for existing DBs
    try:
        c.execute("ALTER TABLE tenant_config ADD COLUMN drive_connected_at TEXT")
        conn.commit()
    except Exception:
        pass
    c.execute('''
        CREATE TABLE IF NOT EXISTS usage_stats (
            source_id TEXT,
            date TEXT,
            upload_count INTEGER DEFAULT 0,
            summary_count INTEGER DEFAULT 0,
            PRIMARY KEY (source_id, date)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS used_slips (
            trans_ref TEXT PRIMARY KEY,
            user_id TEXT,
            amount REAL,
            processed_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS support_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            created_at TEXT,
            replied INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS page_views (
            date TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT,
            user_id TEXT,
            filename TEXT,
            file_url TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Tenant & Config Helpers ---
def get_tenant_config(source_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT google_refresh_token, google_folder_id, tier, expires_at, drive_connected_at FROM tenant_config WHERE source_id = ?", (source_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'refresh_token': row[0],
            'folder_id': row[1],
            'tier': row[2],
            'expires_at': row[3],
            'drive_connected_at': row[4]
        }
    return {
        'refresh_token': None,
        'folder_id': None,
        'tier': 'FREE',
        'expires_at': None,
        'drive_connected_at': None
    }

def update_tenant_config(source_id, **kwargs):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT 1 FROM tenant_config WHERE source_id = ?", (source_id,))
    exists = c.fetchone()
    if not exists:
        c.execute("INSERT INTO tenant_config (source_id, created_at) VALUES (?, ?)", (source_id, datetime.now().isoformat()))
        conn.commit()
        
    for k, v in kwargs.items():
        c.execute(f"UPDATE tenant_config SET {k} = ? WHERE source_id = ?", (v, source_id))
    conn.commit()
    conn.close()

def is_premium(source_id):
    config = get_tenant_config(source_id)
    if config['tier'] == 'VVIP':
        return True  # VVIP never expires
    if config['tier'] == 'PREMIUM':
        if config['expires_at']:
            try:
                expiry = datetime.fromisoformat(config['expires_at'])
                if expiry > datetime.now():
                    return True
            except Exception as e:
                logger.error(f"Expiry date parse error: {e}")
    return False

FREE_TRIAL_DAYS = 30

def check_and_revoke_expired_trial(user_id, config):
    """Free tier is now completely unlimited - never revokes."""
    return False

def get_trial_days_remaining(config):
    """Free tier is permanent - no countdown needed."""
    return None

def get_usage(source_id):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT upload_count, summary_count FROM usage_stats WHERE source_id = ? AND date = ?", (source_id, today))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0], row[1]
    return 0, 0

def increment_usage(source_id, upload=True):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT 1 FROM usage_stats WHERE source_id = ? AND date = ?", (source_id, today))
    exists = c.fetchone()
    if not exists:
        c.execute("INSERT INTO usage_stats (source_id, date) VALUES (?, ?)", (source_id, today))
        conn.commit()
        
    if upload:
        c.execute("UPDATE usage_stats SET upload_count = upload_count + 1 WHERE source_id = ? AND date = ?", (source_id, today))
    else:
        c.execute("UPDATE usage_stats SET summary_count = summary_count + 1 WHERE source_id = ? AND date = ?", (source_id, today))
    conn.commit()
    conn.close()

# --- Admin IDs Management ---
def get_notify_list():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id FROM notify_ids')
    ids = [r[0] for r in c.fetchall()]
    conn.close()
    return ids

def add_notify_id(nid):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO notify_ids (id) VALUES (?)', (nid,))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

def remove_notify_id(nid):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM notify_ids WHERE id = ?', (nid,))
    changes = conn.total_changes
    conn.commit()
    conn.close()
    return changes > 0

# --- Google Drive Setup ---
drive_service = None

def get_drive_service():
    global drive_service
    if drive_service:
        return drive_service
    
    try:
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE)
            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    with open(TOKEN_FILE, 'w') as f:
                        f.write(creds.to_json())
                except Exception as refresh_err:
                    logger.error(f"Token Refresh Error: {refresh_err}")
                    return None
            
            drive_service = build('drive', 'v3', credentials=creds)
            logger.info("Fallback Google Drive Connected!")
            return drive_service
        else:
            logger.warning(f"Fallback Token file not found: {TOKEN_FILE}")
    except Exception as e:
        logger.error(f"Fallback Drive Initialization Error: {e}")
    
    return None

def get_tenant_drive_service(source_id):
    config = get_tenant_config(source_id)
    refresh_token = config['refresh_token']
    folder_id = config['folder_id']
    
    if not refresh_token:
        return None, None
        
    try:
        import json
        with open(os.path.join(BASE_DIR, 'client_secret.json'), 'r') as f:
            secret_data = json.load(f)
            
        client_id = secret_data['web']['client_id']
        client_secret = secret_data['web']['client_secret']
        token_uri = secret_data['web']['token_uri']
        
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            token_uri=token_uri
        )
        
        # Refresh access token
        creds.refresh(Request())
        
        service = build('drive', 'v3', credentials=creds)
        return service, folder_id
    except Exception as e:
        logger.error(f"Error building tenant drive service for {source_id}: {e}")
        return None, None

# --- 2. Slip Verification ---
OUR_ACCOUNT = '4045290779'
OWNER_NAME_KEYWORDS = ['เชาว์', 'สุกใส']  # คำในชื่อเจ้าของบัญชี
PRICE_MONTHLY = 89
PRICE_YEARLY = 890

SLIP_VERIFY_PROMPT = """คุณคือผู้ช่วยตรวจสอบสลิปโอนเงินธนาคารไทย
วิเคราะห์รูปที่ส่งมาอย่างละเอียด ทำตามขั้นตอนนี้:
1. อ่านข้อมูลทั้งหมดจากตัวอักษรในรูป (ยอดเงิน เลขบัญชี ชื่อผู้รับ วันที่ เวลา เลข ref)
2. ถ้ามี QR code ให้ถอดรหัสด้วย แต่ถ้าถอดไม่ได้ก็ใช้ข้อมูลจากตัวอักษรแทนได้

ตอบเป็น JSON เท่านั้น ไม่มีข้อความอื่น:
{
  "found": true,
  "trans_ref": "เลข ref หรือ transaction id ที่เห็นในสลิป",
  "amount": 89.00,
  "destination_account": "เลขบัญชีผู้รับ เฉพาะตัวเลขไม่มีขีด",
  "destination_name": "ชื่อผู้รับ",
  "bank": "ธนาคารผู้รับ",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "status": "สำเร็จ หรือสถานะที่เห็น"
}
ถ้ารูปไม่ใช่สลิปโอนเงินเลย: {"found": false, "reason": "เหตุผล"}"""

def verify_slip_with_gemini(slip_path):
    try:
        from google.genai import types as _t
        mime = mimetypes.guess_type(slip_path)[0] or 'image/jpeg'
        with open(slip_path, 'rb') as f:
            img_bytes = f.read()
        client = genai.Client(api_key=GEMINI_API_KEY)
        image_part = _t.Part.from_bytes(data=img_bytes, mime_type=mime)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image_part, SLIP_VERIFY_PROMPT]
        )
        text = response.text.strip()
        logger.info(f'[SLIP] Gemini raw: {text[:300]}')
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            result = json.loads(match.group())
            logger.info(f'[SLIP] Parsed: {result}')
            return result
        logger.warning(f'[SLIP] No JSON found in Gemini response')
        return {'found': False, 'reason': 'parse error'}
    except Exception as e:
        logger.error(f'Slip verify error: {e}', exc_info=True)
        return {'found': False, 'reason': str(e)}

def is_slip_used(trans_ref):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT 1 FROM used_slips WHERE trans_ref = ?', (trans_ref,))
    result = c.fetchone()
    conn.close()
    return result is not None

def mark_slip_used(trans_ref, user_id, amount):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO used_slips (trans_ref, user_id, amount, processed_at) VALUES (?, ?, ?, ?)',
              (trans_ref, user_id, amount, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def process_slip_verification(user_id, slip_path, slip_file):
    result = verify_slip_with_gemini(slip_path)

    def notify_admin(reason=''):
        admins = get_notify_list()
        base_url = os.getenv('BASE_URL', 'https://filesaver.deathwolftech.site')
        slip_url = f"{base_url.rstrip('/')}/slips/{slip_file}"
        msg = (f"📢 แจ้งโอนเงินใหม่ (ตรวจสอบอัตโนมัติไม่ผ่าน)\n"
               f"👤 User: {user_id}\n"
               f"🔗 สลิป: {slip_url}\n"
               f"⚠️ เหตุผล: {reason}\n\n"
               f"หากยืนยันแล้วพิมพ์: /approve {user_id} 30")
        for admin_id in admins:
            try: push_text(admin_id, msg)
            except: pass

    if not result.get('found'):
        notify_admin(result.get('reason', 'อ่านสลิปไม่ได้'))
        push_text(user_id, "⚠️ ไม่สามารถอ่านสลิปอัตโนมัติได้ครับ\nได้แจ้งทีมงานแล้ว จะได้รับการยืนยันเร็วๆ นี้")
        return

    trans_ref = result.get('trans_ref', '')
    amount = float(result.get('amount', 0))
    destination = re.sub(r'\D', '', result.get('destination_account', ''))
    dest_name = result.get('destination_name', '')

    account_ok = OUR_ACCOUNT in destination or destination in OUR_ACCOUNT
    name_ok = any(kw in dest_name for kw in OWNER_NAME_KEYWORDS)

    if not account_ok and not name_ok:
        notify_admin(f'ปลายทาง: "{destination}" / "{dest_name}" ไม่ใช่บัญชีเรา')
        push_text(user_id, "⚠️ ไม่พบบัญชีของเราในสลิปครับ กรุณาตรวจสอบว่าโอนมาถูกบัญชี\nได้แจ้งทีมงานแล้วเช่นกัน")
        return

    if trans_ref and is_slip_used(trans_ref):
        push_text(user_id, "⚠️ สลิปนี้เคยใช้ยืนยันไปแล้วครับ ไม่สามารถใช้ซ้ำได้")
        return

    if abs(amount - PRICE_MONTHLY) < 1:
        days, tier_name = 30, 'รายเดือน'
    elif abs(amount - PRICE_YEARLY) < 1:
        days, tier_name = 365, 'รายปี'
    else:
        notify_admin(f'ยอดเงิน {amount:.0f} บ. ไม่ตรงแพ็กเกจ (89/890)')
        push_text(user_id, f"⚠️ ยอดเงิน {amount:.0f} บาท ไม่ตรงกับแพ็กเกจครับ (89 หรือ 890 บาท)\nได้แจ้งทีมงานแล้ว")
        return

    if trans_ref:
        mark_slip_used(trans_ref, user_id, amount)
    expiry = (datetime.now() + timedelta(days=days)).isoformat()
    update_tenant_config(user_id, tier='PREMIUM', expires_at=expiry)

    push_text(user_id,
        f"🎉 ยืนยันการชำระเงินสำเร็จ!\n"
        f"⭐ อัพเกรดเป็น Premium แพ็กเกจ{tier_name}\n"
        f"📅 ใช้งานได้ถึง: {expiry[:10]}\n"
        f"📁 พิมพ์ /setup เพื่อเชื่อมต่อ Google Drive ครับ"
    )
    for admin_id in get_notify_list():
        try:
            push_text(admin_id, f"✅ Auto-approved Premium\n👤 {user_id}\n💰 {amount:.0f} บ. ({tier_name})\n📋 Ref: {trans_ref}")
        except: pass

# --- 3. Queue & Worker System ---
upload_queue = queue.Queue()

def build_success_flex(file_name, subfolder_id):
    drive_uri = f"https://drive.google.com/drive/folders/{subfolder_id}" if subfolder_id else "https://drive.google.com"
    contents = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "paddingAll": "16px",
            "contents": [
                {"type": "text", "text": "✅ บันทึกสำเร็จ", "weight": "bold", "color": "#22c55e", "size": "sm"},
                {"type": "text", "text": file_name, "size": "sm", "color": "#333333", "wrap": True, "margin": "xs"},
                {"type": "text", "text": datetime.now().strftime('%Y-%m-%d  %H:%M'), "size": "xs", "color": "#aaaaaa", "margin": "xs"},
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "8px",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {"type": "uri", "label": "📂 เปิดโฟลเดอร์ Drive", "uri": drive_uri}
                }
            ]
        }
    }
    watermark = TextSendMessage(text="💡 สนใจดึงบอทเซฟไฟล์เข้ากลุ่มคุณ?\nเชิญใช้งานฟรี: https://line.me/R/ti/p/@605pmlbd")
    return FlexSendMessage(alt_text=f"บันทึกสำเร็จ: {file_name}", contents=contents), watermark

def upload_worker():
    logger.info("🚀 Upload Worker Started...")
    while True:
        try:
            file_path, file_name, reply_token, tenant_id, notify_id, source_label = upload_queue.get()
            logger.info(f"📦 Processing: {file_name} from {source_label} (Tenant: {tenant_id}, Room: {notify_id})")
            
            try:
                # Resolve tenant drive service
                service, target_folder_id = get_tenant_drive_service(tenant_id)
                
                # Fallback to default shared drive
                if not service:
                    service = get_drive_service()
                    target_folder_id = GOOGLE_DRIVE_FOLDER_ID
                    
                if not service:
                    raise Exception("No Google Drive Service credentials configured.")
                
                # Upload
                subfolder_id = upload_to_drive_dynamic(service, target_folder_id, file_path, file_name)

                if os.path.exists(file_path):
                    os.remove(file_path)
                
                drive_url = f"https://drive.google.com/drive/folders/{subfolder_id}" if subfolder_id else "https://drive.google.com"
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("INSERT INTO uploaded_files (source_id, user_id, filename, file_url, timestamp) VALUES (?, ?, ?, ?, ?)",
                          (tenant_id, notify_id, file_name, drive_url, datetime.now().isoformat()))
                conn.commit()
                conn.close()

                logger.info(f"✅ Successfully uploaded: {file_name}")
                success_msg, watermark_msg = build_success_flex(file_name, subfolder_id)
                
                # We can pass list of messages
                msgs_to_send = [success_msg, watermark_msg]
                if reply_token:
                    try: line_bot_api.reply_message(reply_token, msgs_to_send)
                    except: line_bot_api.push_message(notify_id, msgs_to_send)
                else:
                    line_bot_api.push_message(notify_id, msgs_to_send)
                
                # Notify Admins
                admins = get_notify_list()
                if admins:
                    admin_msg = f"📢 รายงานการเซฟไฟล์\n📂 ไฟล์: {file_name}\n🏠 จาก: {source_label} (User: {tenant_id})\n🕒 เวลา: {datetime.now().strftime('%H:%M:%S')}"
                    for admin_id in admins:
                        try: push_text(admin_id, admin_msg)
                        except: pass
            except Exception as e:
                logger.error(f"❌ Upload Error ({file_name}): {e}", exc_info=True)
                err_msg = f"❌ Error uploading {file_name}: {e}"
                if reply_token:
                    try: reply_text(reply_token, err_msg)
                    except: push_text(notify_id, err_msg)
                else:
                    push_text(notify_id, err_msg)
        except Exception as e:
            logger.critical(f"❌ Worker critical error: {e}", exc_info=True)
        finally:
            upload_queue.task_done()
            time.sleep(1)

def upload_to_drive_dynamic(service, target_folder_id, file_path, file_name, max_retries=3):
    if not target_folder_id:
        target_folder_id = 'root'
        
    today_str = datetime.now().strftime("%Y-%m-%d")
    query = f"mimeType='application/vnd.google-apps.folder' and name='{today_str}' and '{target_folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])
    
    if files:
        subfolder_id = files[0]['id']
    else:
        folder_metadata = {
            'name': today_str,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [target_folder_id]
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        subfolder_id = folder.get('id')

    metadata = {'name': file_name, 'parents': [subfolder_id]}

    for attempt in range(1, max_retries + 1):
        try:
            media = MediaFileUpload(file_path, resumable=True)
            service.files().create(body=metadata, media_body=media).execute()
            return subfolder_id
        except Exception as e:
            if attempt < max_retries:
                time.sleep(5)
            else:
                raise e

# --- 3. Gemini Summary ---
def run_summary(source_id, days=7):
    logger.info(f"\n[SUMMARY] เริ่มประมวลผล #สรุปแชท ในรอบ {days} วัน...")
    time_ago = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d 00:00:00')
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT message FROM chat_messages WHERE timestamp >= ? AND (source_id = ? OR source_id = 'PM All Project(NCT)')", (time_ago, source_id))
    rows = c.fetchall()
    conn.close()
    
    if rows:
        messages = [r[0] for r in rows]
        chat_text = "\n".join(messages)
        prompt = f"""
นี่คือข้อความแชทในรอบ {days} วันที่ผ่านมา:
{chat_text}

กรุณาสรุปเฉพาะ "งาน" หรือ "สิ่งที่ต้องทำ (Action Items)" ที่มีการพูดคุยตกลงกันเท่านั้น ไม่ต้องสรุปอารมณ์ ไม่ต้องสรุปเรื่องคุยเล่น ให้สรุปเป็นหัวข้อสั้นๆ กระชับ และตรงประเด็นที่สุด
"""
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            summary_text = f"📊 **สรุปแชทในรอบ {days} วัน (สั่งการด่วน)**\n\n" + response.text.strip()
            push_text(source_id, summary_text)
        except Exception as e:
            push_text(source_id, f"เกิดข้อผิดพลาด (Gemini): {e}")
        finally:
            gc.collect()
    else:
        push_text(source_id, f"ยังไม่มีข้อความแชทสะสมในรอบ {days} วันครับ")
        gc.collect()

# --- 4. Web OAuth & Payment Routes ---

@app.route("/")
def index():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Local tracking (Internal System)
    c.execute(
        "INSERT INTO page_views (date, count) VALUES (?, 1) "
        "ON CONFLICT(date) DO UPDATE SET count = count + 1",
        (today,)
    )
    conn.commit()    
    # ดึงยอดอัปโหลดรวม (บวกฐาน 15,200)
    c.execute("SELECT COALESCE(SUM(upload_count), 0) FROM usage_stats")
    real_uploads = c.fetchone()[0]
    total_uploads = 15200 + real_uploads
    
    conn.close()
    return render_template('index.html',
        google_verification=os.getenv('GOOGLE_SITE_VERIFICATION', ''),
        ga4_id=os.getenv('GA4_ID', ''),
        total_uploads=total_uploads
    )

@app.route('/privacy', strict_slashes=False)
def privacy():
    return render_template('privacy.html')

@app.route('/terms', strict_slashes=False)
def terms():
    return render_template('terms.html')

@app.route('/google038f759db67dff7a.html')
def google_site_verify():
    return 'google-site-verification: google038f759db67dff7a.html', 200, {'Content-Type': 'text/html'}

@app.route('/robots.txt')
def robots_txt():
    base_url = os.getenv('BASE_URL', 'https://filesaver.deathwolftech.site')
    body = (
        "User-agent: *\n"
        "Disallow: /admin\n"
        "Disallow: /admin/\n"
        "Disallow: /callback\n"
        "Disallow: /slips/\n"
        "Disallow: /payment/qr\n"
        "Allow: /\n\n"
        f"Sitemap: {base_url.rstrip('/')}/sitemap.xml\n"
    )
    return body, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/sitemap.xml')
def sitemap_xml():
    base_url = os.getenv('BASE_URL', 'https://filesaver.deathwolftech.site')
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url>\n'
        f'    <loc>{base_url.rstrip("/")}/</loc>\n'
        '    <changefreq>weekly</changefreq>\n'
        '    <priority>1.0</priority>\n'
        '  </url>\n'
        '</urlset>'
    )
    return body, 200, {'Content-Type': 'application/xml; charset=utf-8'}

@app.route("/auth")
def auth():
    source_id = request.args.get("state")
    liff_id = os.getenv('LIFF_ID', '')
    
    if not source_id:
        if liff_id:
            return render_template('auth.html', auth_url="#", liff_id=liff_id)
        return "Error: Missing LINE source_id (state parameter)", 400
        
    client_secret_path = os.path.join(BASE_DIR, 'client_secret.json')
    if not os.path.exists(client_secret_path):
        return "Error: Google Client Secret configuration is missing on server", 500
        
    base_url = os.getenv('BASE_URL')
    if not base_url:
        scheme = request.headers.get("X-Forwarded-Proto", "http")
        base_url = f"{scheme}://{request.host}"
        
    redirect_uri = f"{base_url.rstrip('/')}/google/callback"
    
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secret_path,
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive'],
        state=source_id,
        autogenerate_code_verifier=True
    )
    flow.redirect_uri = redirect_uri
    
    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    if hasattr(flow, 'code_verifier'):
        pkce_store[source_id] = flow.code_verifier
    
    return render_template('auth.html', auth_url=authorization_url, liff_id=liff_id)

@app.route("/google/callback")
def google_callback():
    state = request.args.get("state")
    code = request.args.get("code")
    
    if not state or not code:
        return "Error: Invalid request parameters from Google", 400
        
    client_secret_path = os.path.join(BASE_DIR, 'client_secret.json')
    base_url = os.getenv('BASE_URL')
    if not base_url:
        scheme = request.headers.get("X-Forwarded-Proto", "http")
        base_url = f"{scheme}://{request.host}"
        
    redirect_uri = f"{base_url.rstrip('/')}/google/callback"
    
    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secret_path,
            scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive'],
            state=state,
            autogenerate_code_verifier=True
        )
        flow.redirect_uri = redirect_uri
        
        if state in pkce_store:
            flow.code_verifier = pkce_store.pop(state)
            
        flow.fetch_token(authorization_response=request.url)
        
        credentials = flow.credentials
        refresh_token = credentials.refresh_token
        
        if not refresh_token:
            config = get_tenant_config(state)
            if config['refresh_token']:
                refresh_token = config['refresh_token']
            else:
                return redirect(url_for('auth', state=state))
                
        service = build('drive', 'v3', credentials=credentials)
        
        # Auto-create app folder
        folder_name = "LINE_FileSaver_Bot"
        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
        results = service.files().list(q=query, fields="files(id)").execute()
        folders = results.get('files', [])
        
        if folders:
            folder_id = folders[0]['id']
        else:
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            folder_id = folder.get('id')
            
        update_tenant_config(state,
            google_refresh_token=refresh_token,
            google_folder_id=folder_id,
            drive_connected_at=datetime.now().isoformat(),
            tier='FREE',
            expires_at=None
        )

        try:
            push_text(state,
                f"🎉 เชื่อมต่อ Google Drive สำเร็จ!\n"
                f"📁 ไฟล์จะบันทึกที่โฟลเดอร์: {folder_name}\n\n"
                f"✨ ใช้งานฟรี 100% ไม่จำกัดจำนวนไฟล์ตลอดชีพครับ! ✅\n"
                f"🤖 มีระบบ AI ช่วยวิเคราะห์และตั้งชื่อไฟล์ให้อัตโนมัติ"
            )
        except Exception as line_err:
            logger.error(f"Error sending LINE notification: {line_err}")
            
        config = get_tenant_config(state)
        return render_template('success.html', tier=config['tier'])
        
    except Exception as e:
        logger.error(f"Error in google_callback: {e}", exc_info=True)
        return f"Error occurred during authentication: {e}", 500

@app.route("/payment/qr")
def payment_qr():
    source_id = request.args.get("source_id")
    amount = float(request.args.get("amount", 99.00))
    
    payload = promptpay.generate_payload(PROMPTPAY_ID, amount)
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route("/slips/<filename>")
def get_slip(filename):
    return send_from_directory(SLIPS_DIR, filename)

# --- 5. LINE Handlers ---
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    logger.info(f"[CALLBACK] Received request: {body[:200]}...")
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("[CALLBACK] Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"[CALLBACK] Error: {e}", exc_info=True)
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):
    text = event.message.text
    text_lower = text.lower().strip()
    source_id = getattr(event.source, 'group_id', None) or getattr(event.source, 'user_id', None)
    user_id = getattr(event.source, 'user_id', None)
    logger.info(f"[TEXT] from={user_id} source={source_id} text={text!r}")
    
    # 1. บันทึกแชท (ยกเว้นคำสั่ง)
    if not text.startswith(('#', '/')) and text_lower not in ['ip', 'lp', 'status', 'id', 'list id', 'retry', 'link', 'drive', 'setup', 'เชื่อมต่อ', 'เช็คสถานะ', 'ซื้อ', 'สมัคร', 'buy', 'สถานะ', 'แจ้งโอน']:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO chat_messages (timestamp, source_id, user_id, message) VALUES (?, ?, ?, ?)',
                  (timestamp, source_id, user_id, text))
        conn.commit()
        conn.close()

    # 2. คำสั่งต่างๆ
    if text_lower == 'id':
        reply_text(event.reply_token, f"👤 User: {user_id}\n👥 Group: {getattr(event.source, 'group_id', 'None')}")
    
    elif text_lower == 'list id':
        ids = get_notify_list()
        msg = "📋 Admin List:\n" + "\n".join(ids) if ids else "📭 Empty"
        reply_text(event.reply_token, msg)

    elif text_lower.startswith('add id '):
        new_id = text[7:].strip()
        if add_notify_id(new_id):
            reply_text(event.reply_token, "✅ เพิ่ม Admin เรียบร้อย")
            # ผูก Admin Rich Menu ให้ทันที (ถ้ามี)
            if os.getenv('ADMIN_RICH_MENU_ID'):
                threading.Thread(target=assign_rich_menu, args=(new_id, 'ADMIN_RICH_MENU_ID'), daemon=True).start()
        else:
            reply_text(event.reply_token, "⚠️ ล้มเหลว หรือเป็นอยู่แล้ว")

    elif text_lower.startswith('del id '):
        del_id = text[7:].strip()
        if remove_notify_id(del_id):
            reply_text(event.reply_token, "🗑️ ลบ Admin เรียบร้อย")
            # คืน default Rich Menu
            threading.Thread(target=unassign_rich_menu, args=(del_id,), daemon=True).start()
        else:
            reply_text(event.reply_token, "⚠️ ไม่พบ ID")

    elif text_lower.startswith('/ค้นหา ') or text_lower.startswith('/search '):
        keyword = text[7:].strip() if text_lower.startswith('/ค้นหา') else text[8:].strip()
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT filename, file_url, timestamp FROM uploaded_files WHERE source_id = ? AND filename LIKE ? ORDER BY timestamp DESC LIMIT 5",
                  (source_id, f'%{keyword}%'))
        results = c.fetchall()
        conn.close()
        
        if results:
            msg = f"🔎 ผลการค้นหา '{keyword}':\n\n"
            for fname, furl, ts in results:
                d = ts[:10]
                msg += f"📄 {fname}\n📅 {d}\n🔗 {furl}\n\n"
            reply_text(event.reply_token, msg.strip())
        else:
            reply_text(event.reply_token, f"❌ ไม่พบไฟล์ที่ชื่อมีคำว่า '{keyword}' ในระบบครับ")

    elif text_lower in ['ip', 'lp', 'status', 'check', 'เช็คสถานะ', '/status', 'สถานะ']:
        config = get_tenant_config(user_id)
        tier = config['tier']
        expires_at = config['expires_at']
        folder_id = config['folder_id']
        uploads, _ = get_usage(user_id)
        is_admin = user_id in get_notify_list()
        is_vvip = tier == 'VVIP'

        # --- ข้อมูล Server (Admin หรือ VVIP เท่านั้น) ---
        if is_admin or is_vvip:
            try: ip = requests.get('https://api.ipify.org', timeout=5).text
            except: ip = "Unknown"
            pending = len(os.listdir(PENDING_DIR))
            msg = f"📊 สถานะระบบบอท\n"
            msg += f"🌐 IP: {ip}\n"
            msg += f"📁 Queue: {upload_queue.qsize()} | Pending: {pending}\n"
            msg += f"─────────────────\n"
        else:
            msg = f"📊 สถานะบัญชีของคุณ\n"

        # --- ข้อมูล Account (แสดงทุกคน) ---
        msg += f"⭐ แพ็กเกจ: ฟรีตลอดชีพ (Free Unlimited)\n"
        msg += f"📁 Drive: {'เชื่อมต่อแล้ว ✅' if folder_id else 'ยังไม่เชื่อมต่อ (พิมพ์ /setup)'}\n"
        msg += f"📤 วันนี้อัปโหลด: {uploads} ไฟล์ (ไม่จำกัดจำนวน)\n"
        msg += f"🤖 AI Auto-Rename: เปิดใช้งาน ✅"
            
        reply_text(event.reply_token, msg)
 
    elif text_lower in ['/uid', 'uid', 'myid', '/myid']:
        reply_text(event.reply_token, f"🪪 LINE User ID ของคุณ:\n{user_id}")

    elif text_lower in ['/setup', 'setup', 'เชื่อมต่อ']:
        base_url = os.getenv('BASE_URL')
        if not base_url:
            scheme = request.headers.get("X-Forwarded-Proto", "https")  # LINE requires https for URI actions
            base_url = f"{scheme}://{request.host}"
            
        liff_id = os.getenv('LIFF_ID')
        if liff_id:
            auth_link = f"https://liff.line.me/{liff_id}"
        else:
            auth_link = f"{base_url.rstrip('/')}/auth?state={user_id}"
            
        config = get_tenant_config(user_id)
        
        if config['folder_id']:
            body_text = f"บัญชีเชื่อมต่อแล้ว\nFolder ID: {config['folder_id'][:20]}..."
            btn_label = "เชื่อมใหม่ / เปลี่ยนบัญชี"
        else:
            body_text = "บอทจะสร้างโฟลเดอร์ชื่อ LINE_FileSaver_Bot ให้โดยอัตโนมัติ"
            btn_label = "เชื่อมต่อ Google Drive"

        buttons_template = ButtonsTemplate(
            title="ตั้งค่า Google Drive",
            text=body_text,
            actions=[
                URITemplateAction(
                    label=btn_label,
                    uri=auth_link
                )
            ]
        )
        template_message = TemplateSendMessage(
            alt_text="ตั้งค่า Google Drive",
            template=buttons_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)
 
    elif text_lower in ['/buy', 'buy', 'ซื้อ', 'สมัคร']:
        msg = (
            "🎉 FileSaverBot ให้บริการฟรี 100% ครับ!\n\n"
            "✨ อัปโหลดไฟล์ได้ไม่จำกัดจำนวน\n"
            "✨ เชื่อมต่อ Google Drive ส่วนตัวฟรีตลอดชีพ\n"
            "✨ AI วิเคราะห์และตั้งชื่อไฟล์ให้อัตโนมัติ\n\n"
            "👉 พิมพ์ /setup เพื่อเชื่อมต่อ Google Drive และเริ่มใช้งานได้ทันทีครับ"
        )
        reply_text(event.reply_token, msg)


    elif text_lower.startswith('#แจ้งโอน') or text_lower.startswith('แจ้งโอน'):
        slip_file = last_images.get(user_id)
        if not slip_file:
            reply_text(event.reply_token, "⚠️ ไม่พบรูปสลิปที่ส่งเข้ามาล่าสุดครับ กรุณาส่งรูปสลิปก่อน แล้วพิมพ์ แจ้งโอน อีกครั้ง")
            return

        slip_path = os.path.join(SLIPS_DIR, slip_file)
        reply_text(event.reply_token, "🔍 กำลังตรวจสอบสลิปอัตโนมัติ กรุณารอสักครู่...")
        threading.Thread(
            target=process_slip_verification,
            args=(user_id, slip_path, slip_file),
            daemon=True
        ).start()

    elif text_lower.startswith('/approve ') or text_lower.startswith('approve '):
        if user_id not in get_notify_list():
            reply_text(event.reply_token, "⚠️ คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้")
            return
            
        parts = text.split()
        if len(parts) < 3:
            reply_text(event.reply_token, "⚠️ รูปแบบคำสั่งไม่ถูกต้อง: /approve <user_id> <days>")
            return
            
        target_user_id = parts[1].strip()
        days_str = parts[2].strip().lower()

        # VVIP: ไม่มีวันหมดอายุ
        if days_str == 'vvip':
            update_tenant_config(target_user_id, tier='VVIP', expires_at=None)
            try:
                push_text(target_user_id, "👑 บัญชีของคุณได้รับการตั้งค่าเป็น VVIP แล้ว!\nใช้งานได้ไม่จำกัด ไม่มีวันหมดอายุ\n📁 พิมพ์ /setup เพื่อเชื่อมต่อ Google Drive")
            except Exception as push_err:
                logger.error(f"Failed to notify VVIP: {push_err}")
            reply_text(event.reply_token, f"👑 ตั้ง VVIP ให้ {target_user_id} เรียบร้อย")
            return

        if not days_str.isdigit():
            reply_text(event.reply_token, "⚠️ รูปแบบ: /approve <user_id> <days> หรือ /approve <user_id> vvip")
            return

        days = int(days_str)
        expiry_date = (datetime.now() + timedelta(days=days)).isoformat()

        update_tenant_config(target_user_id, tier='PREMIUM', expires_at=expiry_date)

        try:
            push_text(target_user_id, f"🎉 ยินดีด้วย! บัญชีของคุณได้รับการเปิดใช้งาน Premium เรียบร้อยแล้ว\n📅 ใช้งานได้ถึง: {expiry_date[:10]}\n📁 พิมพ์ /setup เพื่อเชื่อมต่อ Google Drive")
        except Exception as push_err:
            logger.error(f"Failed to notify target of approval: {push_err}")

        reply_text(event.reply_token, f"✅ อนุมัติ Premium ให้กับ ID: {target_user_id} จำนวน {days} วัน เรียบร้อยแล้ว")
 
    elif text_lower in ['link', 'drive', 'ขอลิงค์']:
        config = get_tenant_config(user_id)
        folder_id = config['folder_id'] or GOOGLE_DRIVE_FOLDER_ID
        url = f"https://drive.google.com/drive/folders/{folder_id}"
        reply_text(event.reply_token, f"📂 Link: {url}")
 
    elif text_lower in ['retry', 'เก็บตก']:
        threading.Thread(target=retry_pending_files, args=(user_id, source_id)).start()
        reply_text(event.reply_token, "🔍 กำลังตรวจสอบและส่งไฟล์ที่ค้างอยู่ครับ...")
 
    elif text.startswith('#สรุปแชท'):
        reply_text(event.reply_token, "ℹ️ คำสั่ง #สรุปแชท ย้ายไปให้บริการเฉพาะบนเซิร์ฟเวอร์ภายใน (Raspberry Pi) ครับ")

    elif text_lower.startswith('/support'):
        msg_body = text[8:].strip()
        if not msg_body:
            reply_text(event.reply_token, "⚠️ กรุณาระบุข้อความ เช่น\n/support ไฟล์หายครับ ช่วยตรวจสอบด้วยนะครับ")
            return
        # Save to DB
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO support_messages (user_id, message, created_at) VALUES (?, ?, ?)",
                  (user_id, msg_body, datetime.now().isoformat()))
        msg_id = c.lastrowid
        conn.commit()
        conn.close()
        # Notify admins
        for admin_id in get_notify_list():
            try:
                push_text(admin_id,
                    f"🆘 Support #{msg_id}\n"
                    f"👤 {user_id[:12]}...\n"
                    f"💬 {msg_body}\n\n"
                    f"ตอบกลับ: /reply {user_id} ข้อความ"
                )
            except: pass
        reply_text(event.reply_token, "✅ ส่งข้อความถึงทีมงานแล้วครับ จะติดต่อกลับโดยเร็วที่สุด 🙏")

    elif text_lower.startswith('/reply '):
        if user_id not in get_notify_list():
            reply_text(event.reply_token, "⚠️ คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
            return
        parts = text[7:].strip().split(' ', 1)
        if len(parts) < 2:
            reply_text(event.reply_token, "⚠️ รูปแบบ: /reply <user_id> <ข้อความ>")
            return
        target_id, reply_msg = parts[0].strip(), parts[1].strip()
        try:
            push_text(target_id, f"💬 ทีมงาน FileSaverBot:\n{reply_msg}")
            reply_text(event.reply_token, f"✅ ส่งข้อความถึงผู้ใช้แล้วครับ")
        except Exception as e:
            reply_text(event.reply_token, f"❌ ส่งไม่ได้: {e}")

def retry_pending_files(user_id, notify_id):
    files = os.listdir(PENDING_DIR)
    for filename in files:
        file_path = os.path.join(PENDING_DIR, filename)
        upload_queue.put((file_path, filename, None, user_id, notify_id, "Retry System"))

@handler.add(MessageEvent, message=[ImageMessage, VideoMessage, AudioMessage, FileMessage])
def handle_content(event):
    msg_id = event.message.id
    source_id = getattr(event.source, 'group_id', None) or getattr(event.source, 'user_id', None)
    user_id = getattr(event.source, 'user_id', None)
    source_label = "Group" if hasattr(event.source, 'group_id') else "User"
    
    # Check Drive connection — must have personal folder OR shared fallback
    config = get_tenant_config(user_id)

    if not config['folder_id'] and not GOOGLE_DRIVE_FOLDER_ID:
        reply_text(event.reply_token, "⚠️ ยังไม่ได้เชื่อมต่อ Google Drive ครับ\nพิมพ์ /setup เพื่อเชื่อมต่อก่อนนะครับ 📁")
        return
        
    ext = ""
    if isinstance(event.message, ImageMessage): ext = "jpg"
    elif isinstance(event.message, VideoMessage): ext = "mp4"
    elif isinstance(event.message, AudioMessage): ext = "m4a"
    
    if hasattr(event.message, 'file_name'): fname = event.message.file_name
    else: fname = f"{ext or 'file'}_{msg_id}.{ext or 'bin'}"
    
    temp_path = os.path.join(PENDING_DIR, fname)
    def download_and_queue():
        try:
            content = line_bot_api.get_message_content(msg_id)
            with open(temp_path, 'wb') as fd:
                for chunk in content.iter_content():
                    fd.write(chunk)
            
            final_fname = fname
            mime = "image/jpeg" if isinstance(event.message, ImageMessage) else "application/pdf"
            if isinstance(event.message, ImageMessage) or (hasattr(event.message, 'file_name') and ext in ['pdf', 'doc', 'docx', 'png']):
                final_fname = get_ai_filename(temp_path, mime, fname)
                if final_fname != fname:
                    new_temp = os.path.join(PENDING_DIR, final_fname)
                    os.rename(temp_path, new_temp)
                    temp_path = new_temp

            upload_queue.put((temp_path, final_fname, event.reply_token, user_id, source_id, source_label))
            increment_usage(user_id, upload=True)
        except Exception as e:
            logger.error(f"Download Error: {e}")
    threading.Thread(target=download_and_queue).start()


def get_ai_filename(file_path, mime_type, original_name):
    try:
        from google.genai import types as _t
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        client = genai.Client(api_key=GEMINI_API_KEY)
        part = _t.Part.from_bytes(data=file_bytes, mime_type=mime_type)
        prompt = '''วิเคราะห์ภาพหรือเอกสารนี้ แล้วตั้งชื่อไฟล์ให้เหมาะสมที่สุด (สั้นๆ กระชับ)
- ถ้ารูปนี้คือสลิปโอนเงิน ให้ตั้งชื่อว่า: Slip_[จำนวนเงิน]บาท_[ชื่อธนาคาร].jpg (เช่น Slip_500บาท_KBank.jpg)
- ถ้าเป็นรูปอื่นๆ ให้ตั้งชื่อตามสิ่งที่เห็นเด่นชัดที่สุด เช่น รูปหน้างาน_เทปูน.jpg, รูปใบเสร็จ_ค่าไฟ.jpg, แมวสีส้ม.jpg
- ถ้าเป็นเอกสาร ให้ตั้งชื่อสรุปเนื้อหา เช่น สรุปการประชุม_15พค.pdf
- ห้ามมีช่องว่าง (ใช้ _ แทน)
- ห้ามใช้อักขระพิเศษ ยกเว้น _ และ .
- นามสกุลไฟล์ต้องเหมือนเดิม
ตอบมาแค่ชื่อไฟล์บรรทัดเดียวเท่านั้น ห้ามมีคำอธิบายอื่น'''
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[part, prompt]
        )
        new_name = response.text.strip().replace(' ', '_')
        if '.' not in new_name:
            ext = original_name.split('.')[-1]
            new_name = f"{new_name}.{ext}"
        else:
            ext = original_name.split('.')[-1]
            new_name = f"{new_name.rsplit('.', 1)[0]}.{ext}"
        new_name = re.sub(r'[\\/*?:"<>|]', "", new_name)
        return new_name
    except Exception as e:
        logger.error(f"[AI Rename] Error: {e}")
        return original_name

# --- 6. Follow Event (Greeting) ---
@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    logger.info(f"[FOLLOW] New user: {user_id}")

    welcome = (
        "🎉 ยินดีต้อนรับสู่ FileSaverBot!\n\n"
        "📁 บอทช่วยบันทึกไฟล์จาก LINE → Google Drive อัตโนมัติ (ใช้งานฟรี 100%)\n\n"
        "🚀 เริ่มต้นใช้งานง่ายๆ:\n"
        "1️⃣ กดปุ่ม 'ตั้งค่า' หรือพิมพ์ /setup เพื่อเชื่อมต่อ Google Drive\n"
        "2️⃣ ส่งไฟล์ รูปภาพ วิดีโอ หรือเอกสารในแชท\n"
        "3️⃣ บอทจะบันทึกเข้า Drive ของคุณให้อัตโนมัติ ✅\n\n"
        "✨ ไม่จำกัดจำนวนไฟล์ ฟรีตลอดชีพ พร้อม AI ช่วยตั้งชื่อไฟล์อัตโนมัติ!"
    )
    try:
        reply_text(event.reply_token, welcome)
    except Exception as e:
        logger.error(f"[FOLLOW] Error sending greeting: {e}")

    # ผูก default rich menu ให้ user ใหม่
    if os.getenv('RICH_MENU_ID'):
        threading.Thread(target=assign_rich_menu, args=(user_id, 'RICH_MENU_ID'), daemon=True).start()


# --- 7. Admin Dashboard ---
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect('/admin/login')
        return f(*args, **kwargs)
    return decorated

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect('/admin')
    error = None
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect('/admin')
        error = 'รหัสผ่านไม่ถูกต้อง'
    return render_template('admin_login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin/login')

@app.route('/admin')
@admin_required
def admin_dashboard():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')

    c.execute("SELECT COUNT(*) FROM tenant_config")
    total_users = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM tenant_config WHERE tier='PREMIUM' AND expires_at > ?", (datetime.now().isoformat(),))
    premium_users = c.fetchone()[0]

    c.execute("SELECT COALESCE(SUM(upload_count), 0) FROM usage_stats WHERE date=?", (today,))
    today_uploads = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM used_slips")
    total_slips = c.fetchone()[0]

    c.execute("SELECT COALESCE(SUM(amount), 0) FROM used_slips")
    total_revenue = c.fetchone()[0]

    c.execute("""
        SELECT tc.source_id, tc.tier, tc.expires_at,
               CASE WHEN tc.google_folder_id IS NOT NULL THEN 1 ELSE 0 END,
               COALESCE(us.upload_count, 0),
               tc.created_at
        FROM tenant_config tc
        LEFT JOIN usage_stats us ON tc.source_id = us.source_id AND us.date = ?
        ORDER BY tc.created_at DESC
    """, (today,))
    users = c.fetchall()

    c.execute("SELECT id FROM notify_ids")
    admins = [r[0] for r in c.fetchall()]

    c.execute("SELECT trans_ref, user_id, amount, processed_at FROM used_slips ORDER BY processed_at DESC LIMIT 15")
    slips = c.fetchall()

    # Upload trend last 7 days
    c.execute("""
        SELECT date, COALESCE(SUM(upload_count), 0)
        FROM usage_stats
        WHERE date >= date('now', '-6 days')
        GROUP BY date ORDER BY date
    """)
    trend = c.fetchall()

    # Support messages (unread first)
    c.execute("""
        SELECT id, user_id, message, created_at, replied
        FROM support_messages
        ORDER BY replied ASC, created_at DESC
        LIMIT 30
    """)
    support_msgs = c.fetchall()
    unread_count = sum(1 for s in support_msgs if not s[4])

    # Page view stats (Local System)
    c.execute("""
        SELECT date, count FROM page_views
        WHERE date >= date('now', '-6 days')
        ORDER BY date
    """)
    local_views_trend = c.fetchall()
    c.execute("SELECT COALESCE(SUM(count), 0) FROM page_views")
    local_total_views = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(count), 0) FROM page_views WHERE date = ?", (today,))
    local_today_views = c.fetchone()[0]

    # Page view stats from GA4
    ga4_data = get_ga4_stats_cached()
    ga4_trend = ga4_data['trend']
    ga4_total = ga4_data['total_views']
    ga4_today = ga4_data['today_views']
    
    conn.close()
    return render_template('admin_dashboard.html',
        total_users=total_users, premium_users=premium_users,
        today_uploads=today_uploads, total_slips=total_slips,
        total_revenue=total_revenue, users=users, admins=admins,
        slips=slips, trend=trend, support_msgs=support_msgs,
        unread_count=unread_count, 
        local_views_trend=local_views_trend, local_total_views=local_total_views, local_today_views=local_today_views,
        ga4_trend=ga4_trend, ga4_total=ga4_total, ga4_today=ga4_today,
        now=datetime.now()
    )

@app.route('/admin/approve/<user_id>/<int:days>', methods=['POST'])
@admin_required
def admin_approve(user_id, days):
    expiry = (datetime.now() + timedelta(days=days)).isoformat()
    update_tenant_config(user_id, tier='PREMIUM', expires_at=expiry)
    try:
        push_text(user_id, f"🎉 บัญชีของคุณได้รับการเปิดใช้งาน Premium แล้ว!\n📅 ใช้งานได้ถึง: {expiry[:10]}\n📁 พิมพ์ /setup เพื่อเชื่อมต่อ Google Drive")
    except: pass
    return redirect('/admin')

@app.route('/admin/revoke/<user_id>', methods=['POST'])
@admin_required
def admin_revoke(user_id):
    update_tenant_config(user_id, tier='FREE', expires_at=None)
    try:
        push_text(user_id, "ℹ️ บัญชี Premium ของคุณถูกยกเลิกแล้วครับ")
    except: pass
    return redirect('/admin')

@app.route('/admin/add-line-admin', methods=['POST'])
@admin_required
def admin_add_line_admin():
    new_id = request.form.get('line_id', '').strip()
    if new_id:
        add_notify_id(new_id)
        try:
            assign_rich_menu(new_id, 'ADMIN_RICH_MENU_ID')
        except: pass
    return redirect('/admin')

@app.route('/admin/remove-line-admin/<path:admin_id>', methods=['POST'])
@admin_required
def admin_remove_line_admin(admin_id):
    remove_notify_id(admin_id)
    return redirect('/admin')

@app.route('/admin/message/<user_id>', methods=['POST'])
@admin_required
def admin_message(user_id):
    msg = request.form.get('message', '').strip()
    if msg:
        try:
            push_text(user_id, f"💬 ทีมงาน FileSaverBot:\n{msg}")
        except Exception as e:
            logger.error(f"Admin message push error: {e}")
    return redirect('/admin')

@app.route('/admin/support/<int:msg_id>/mark-replied', methods=['POST'])
@admin_required
def admin_mark_replied(msg_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE support_messages SET replied=1 WHERE id=?", (msg_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')


if __name__ == "__main__":
    threading.Thread(target=upload_worker, daemon=True).start()
    app.run(host='0.0.0.0', port=5020)
