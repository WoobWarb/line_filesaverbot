import os
import sqlite3
from google import genai
from datetime import datetime, timedelta
from linebot.v3.messaging import (
    ApiClient, Configuration, MessagingApi,
    PushMessageRequest, TextMessage
)
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'chat_log.db')

_line_config = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)


def push_text(target_id, text):
    with ApiClient(_line_config) as api_client:
        MessagingApi(api_client).push_message(
            PushMessageRequest(to=target_id, messages=[TextMessage(type='text', text=text)])
        )


def send_weekly_summary():
    print(f"[{datetime.now()}] เริ่มต้นการรัน Weekly Summary...")

    if not GEMINI_API_KEY:
        print("ยังไม่ได้ตั้งค่า Gemini API Key")
        return

    client = genai.Client(api_key=GEMINI_API_KEY)

    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d 00:00:00')
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT source_id, message FROM chat_messages WHERE timestamp >= ? AND source_id LIKE 'C%'",
        (seven_days_ago,)
    )
    rows = c.fetchall()
    
    # ดึงข้อมูล config เพื่อเช็ค tier ของแต่ละ source_id
    c.execute("SELECT source_id, tier, expires_at FROM tenant_config")
    configs = {row[0]: {'tier': row[1], 'expires_at': row[2]} for row in c.fetchall()}
    
    conn.close()

    def is_premium(source_id):
        conf = configs.get(source_id, {'tier': 'FREE', 'expires_at': None})
        if conf['tier'] == 'VVIP':
            return True
        if conf['tier'] == 'PREMIUM':
            if conf['expires_at']:
                try:
                    expiry = datetime.fromisoformat(conf['expires_at'])
                    if expiry > datetime.now():
                        return True
                except:
                    pass
        return False

    if not rows:
        print("ไม่มีข้อความสะสมในรอบสัปดาห์")
        return

    chats_by_source = {}
    for source_id, msg in rows:
        chats_by_source.setdefault(source_id, []).append(msg)

    for source_id, messages in chats_by_source.items():
        if not is_premium(source_id):
            print(f"ข้ามห้อง {source_id} เนื่องจากเป็น Free Tier (ประหยัด Token)")
            continue
            
        if len(messages) < 5:
            print(f"ห้อง {source_id} มีข้อความน้อยกว่า 5 ประโยค ข้ามการสรุป")
            continue

        chat_text = "\n".join(messages)
        prompt = f"""
นี่คือข้อความแชทในรอบสัปดาห์ที่ผ่านมา:
{chat_text}

กรุณาสรุปเฉพาะ "งาน" หรือ "สิ่งที่ต้องทำ (Action Items)" ที่มีการพูดคุยตกลงกันเท่านั้น ไม่ต้องสรุปอารมณ์ ไม่ต้องสรุปเรื่องคุยเล่น ให้สรุปเป็นหัวข้อสั้นๆ กระชับ และตรงประเด็นที่สุด
"""
        try:
            print(f"กำลังวิเคราะห์และสรุปห้อง: {source_id}")
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            summary_text = "📊 **สรุปแชทประจำสัปดาห์ (วันจันทร์)**\n\n" + response.text.strip()
            push_text(source_id, summary_text)
            print(f"ส่งสรุปแชทไปที่ {source_id} สำเร็จ! ✅")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการส่งสรุปให้ {source_id}: {e}")


if __name__ == '__main__':
    send_weekly_summary()
