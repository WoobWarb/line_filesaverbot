"""
setup_rich_menu.py
รันสคริปต์นี้ครั้งเดียวเพื่อสร้าง Rich Menu ใน LINE Bot
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# ----------- 1. สร้าง Rich Menu -----------
rich_menu_body = {
    "size": {"width": 2500, "height": 1686},
    "selected": True,
    "name": "FileSaverBot Menu",
    "chatBarText": "📂 เมนูบอท",
    "areas": [
        # แถวบน ซ้าย: ลิงค์ Drive
        {
            "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
            "action": {"type": "message", "text": "link"}
        },
        # แถวบน กลาง: ตั้งค่า
        {
            "bounds": {"x": 833, "y": 0, "width": 834, "height": 843},
            "action": {"type": "message", "text": "/setup"}
        },
        # แถวบน ขวา: สมัคร Premium
        {
            "bounds": {"x": 1667, "y": 0, "width": 833, "height": 843},
            "action": {"type": "message", "text": "/buy"}
        },
        # แถวล่าง ซ้าย: เช็คสถานะ
        {
            "bounds": {"x": 0, "y": 843, "width": 833, "height": 843},
            "action": {"type": "message", "text": "สถานะ"}
        },
        # แถวล่าง กลาง: เก็บตก
        {
            "bounds": {"x": 833, "y": 843, "width": 834, "height": 843},
            "action": {"type": "message", "text": "retry"}
        },
        # แถวล่าง ขวา: สรุปแชท
        {
            "bounds": {"x": 1667, "y": 843, "width": 833, "height": 843},
            "action": {"type": "message", "text": "#สรุปแชท"}
        }
    ]
}

print("📋 กำลังสร้าง Rich Menu...")
resp = requests.post(
    "https://api.line.me/v2/bot/richmenu",
    headers=HEADERS,
    data=json.dumps(rich_menu_body)
)
resp.raise_for_status()
rich_menu_id = resp.json()["richMenuId"]
print(f"✅ สร้าง Rich Menu สำเร็จ: {rich_menu_id}")

# ----------- 2. อัปโหลดรูป Rich Menu (JPEG <= 1MB) -----------
image_path = os.path.join(os.path.dirname(__file__), "rich_menu.jpg")

if not os.path.exists(image_path):
    print(f"[!] ไม่พบไฟล์รูป: {image_path}")
    print("    กรุณาวางรูปชื่อ rich_menu.jpg (2500x1686 px) ใน folder เดียวกัน แล้วรันใหม่")
    print(f"    Rich Menu ID: {rich_menu_id}")
else:
    print("[*] กำลังอัปโหลดรูป Rich Menu...")
    with open(image_path, "rb") as f:
        img_resp = requests.post(
            f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content",
            headers={
                "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
                "Content-Type": "image/jpeg"
            },
            data=f
        )
    if not img_resp.ok:
        print(f"[!] Upload error {img_resp.status_code}: {img_resp.text}")
        raise Exception("Image upload failed")
    print("[OK] อัปโหลดรูปสำเร็จ")

# ----------- 3. ตั้งเป็น Default Rich Menu -----------
print("🔗 กำลังตั้งเป็น Default Rich Menu...")
default_resp = requests.post(
    f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}",
    headers={"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"}
)
default_resp.raise_for_status()
print("✅ ตั้ง Default Rich Menu สำเร็จ!")

# ----------- บันทึก ID ลง .env -----------
env_path = os.path.join(os.path.dirname(__file__), '.env')
with open(env_path, 'r', encoding='utf-8') as f:
    env_content = f.read()

if 'RICH_MENU_ID' in env_content:
    import re
    env_content = re.sub(r'RICH_MENU_ID\s*=.*', f"RICH_MENU_ID = '{rich_menu_id}'", env_content)
else:
    env_content += f"\nRICH_MENU_ID = '{rich_menu_id}'\n"

with open(env_path, 'w', encoding='utf-8') as f:
    f.write(env_content)

print(f"\n🎉 เสร็จสมบูรณ์!")
print(f"   Rich Menu ID: {rich_menu_id}")
print(f"   บันทึก ID ลง .env แล้ว")
print(f"\n   ลองเปิดแชทกับบอทใน LINE ดูได้เลยครับ!")
