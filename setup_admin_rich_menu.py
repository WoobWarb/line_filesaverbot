"""
setup_admin_rich_menu.py
รันครั้งเดียวเพื่อสร้าง Admin Rich Menu และผูกกับแอดมินทุกคนในระบบ
"""
import os
import json
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
DB_FILE = os.path.join(os.path.dirname(__file__), 'chat_log.db')
HEADERS = {
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# --- 1. สร้าง Admin Rich Menu ---
body = {
    "size": {"width": 2500, "height": 1686},
    "selected": True,
    "name": "FileSaverBot Admin Menu",
    "chatBarText": "Admin Panel",
    "areas": [
        # แถวบน
        {"bounds": {"x": 0,    "y": 0,   "width": 833, "height": 843}, "action": {"type": "message", "text": "สถานะ"}},
        {"bounds": {"x": 833,  "y": 0,   "width": 834, "height": 843}, "action": {"type": "message", "text": "list id"}},
        {"bounds": {"x": 1667, "y": 0,   "width": 833, "height": 843}, "action": {"type": "message", "text": "/approve"}},
        # แถวล่าง
        {"bounds": {"x": 0,    "y": 843, "width": 833, "height": 843}, "action": {"type": "message", "text": "#สรุปแชท"}},
        {"bounds": {"x": 833,  "y": 843, "width": 834, "height": 843}, "action": {"type": "message", "text": "retry"}},
        {"bounds": {"x": 1667, "y": 843, "width": 833, "height": 843}, "action": {"type": "message", "text": "แจ้งโอน"}},
    ]
}

# ลบเมนูเก่าถ้ามี
old_admin_id = os.getenv('ADMIN_RICH_MENU_ID', '')
if old_admin_id:
    r = requests.delete(f"https://api.line.me/v2/bot/richmenu/{old_admin_id}",
                        headers={"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"})
    print(f"Delete old admin menu: {r.status_code}")

print("[*] Creating Admin Rich Menu...")
resp = requests.post("https://api.line.me/v2/bot/richmenu", headers=HEADERS, data=json.dumps(body))
resp.raise_for_status()
menu_id = resp.json()["richMenuId"]
print(f"[OK] Created: {menu_id}")

# --- 2. อัปโหลดรูป ---
image_path = os.path.join(os.path.dirname(__file__), "rich_menu_admin.jpg")
if not os.path.exists(image_path):
    print(f"[!] Image not found: {image_path}")
    print("    Run generate_admin_rich_menu.py first!")
else:
    print("[*] Uploading image...")
    with open(image_path, "rb") as f:
        r2 = requests.post(
            f"https://api-data.line.me/v2/bot/richmenu/{menu_id}/content",
            headers={"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}", "Content-Type": "image/jpeg"},
            data=f
        )
    if not r2.ok:
        print(f"[!] Upload error {r2.status_code}: {r2.text}")
        raise Exception("Image upload failed")
    print("[OK] Image uploaded")

# --- 3. ผูกกับแอดมินทุกคนในฐานข้อมูล ---
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute("SELECT id FROM notify_ids")
admin_ids = [row[0] for row in c.fetchall()]
conn.close()

print(f"[*] Linking to {len(admin_ids)} admin(s)...")
h = {"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"}
for aid in admin_ids:
    r3 = requests.post(f"https://api.line.me/v2/bot/user/{aid}/richmenu/{menu_id}", headers=h)
    status = "OK" if r3.ok else f"FAIL({r3.status_code})"
    print(f"    {aid[:15]}... -> {status}")

# --- 4. บันทึก ID ลง .env ---
env_path = os.path.join(os.path.dirname(__file__), '.env')
with open(env_path, 'r', encoding='utf-8') as f:
    env_content = f.read()

import re
if 'ADMIN_RICH_MENU_ID' in env_content:
    env_content = re.sub(r'ADMIN_RICH_MENU_ID\s*=.*', f"ADMIN_RICH_MENU_ID = '{menu_id}'", env_content)
else:
    env_content += f"\nADMIN_RICH_MENU_ID = '{menu_id}'\n"

with open(env_path, 'w', encoding='utf-8') as f:
    f.write(env_content)

print(f"\n[DONE] Admin Rich Menu ID: {menu_id}")
print(f"       Saved to .env")
print(f"       Linked to {len(admin_ids)} admin(s)")
