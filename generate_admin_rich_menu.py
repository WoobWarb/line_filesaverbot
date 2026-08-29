"""
generate_admin_rich_menu.py - สร้างรูป Admin Rich Menu
ปุ่มพิเศษสำหรับแอดมิน: สถานะระบบ | Admin List | อนุมัติ | สรุปแชท | เก็บตก | แจ้งโอน
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2500, 1686
COLS, ROWS = 3, 2
CELL_W = W // COLS
CELL_H = H // ROWS

# สี Admin theme (เข้มกว่า + สีแดง-ทอง accent)
BG_TOP  = (20, 10, 30)      # dark purple-black
BG_BOT  = (35, 18, 50)      # deep purple
ACCENT  = (220, 160, 50)     # gold
SUB_COL = (200, 170, 255)    # lavender
TEXT_COL= (255, 255, 255)

FONT_PATH_EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
FONT_PATH_TEXT  = "C:/Windows/Fonts/ARIALUNI.TTF"

BUTTONS = [
    ("📊", "สถานะระบบ",   "IP / Queue / Usage"),
    ("👥", "Admin List",   "รายชื่อแอดมิน"),
    ("✅", "อนุมัติ",      "/approve <id> <วัน>"),
    ("📋", "สรุปแชท",     "AI สรุปงาน"),
    ("🔄", "เก็บตก",      "อัปโหลดไฟล์ค้าง"),
    ("💸", "แจ้งโอน",     "ตรวจสลิปชำระเงิน"),
]

img = Image.new("RGB", (W, H), BG_TOP)
draw = ImageDraw.Draw(img, "RGBA")

# Gradient
for y in range(H):
    t = y / H
    r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
    g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
    b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

try:
    font_emoji = ImageFont.truetype(FONT_PATH_EMOJI, 160)
except:
    font_emoji = ImageFont.load_default()
try:
    font_label = ImageFont.truetype(FONT_PATH_TEXT, 90)
    font_sub   = ImageFont.truetype(FONT_PATH_TEXT, 48)
    font_brand = ImageFont.truetype(FONT_PATH_TEXT, 44)
except:
    font_label = ImageFont.load_default()
    font_sub   = font_label
    font_brand = font_label

# Dividers
for col in range(1, COLS):
    x = col * CELL_W
    draw.rectangle([x - 1, 0, x + 1, H], fill=(255, 215, 80, 40))
draw.rectangle([0, CELL_H - 1, W, CELL_H + 1], fill=(255, 215, 80, 40))

# Admin badge แถบทอง บน
draw.rectangle([0, 0, W, 8], fill=(220, 160, 50, 200))
draw.rectangle([0, H - 8, W, H], fill=(220, 160, 50, 200))

def draw_button(idx, emoji, label, sublabel):
    col = idx % COLS
    row = idx // COLS
    cx = col * CELL_W + CELL_W // 2
    cy = row * CELL_H + CELL_H // 2

    # glow วงกลม
    r = 145
    draw.ellipse([cx - r, cy - 155 - r, cx + r, cy - 155 + r], fill=(220, 160, 50, 18))
    r2 = 110
    draw.ellipse([cx - r2, cy - 155 - r2, cx + r2, cy - 155 + r2], fill=(220, 160, 50, 28))

    # emoji
    try:
        bbox = draw.textbbox((0, 0), emoji, font=font_emoji)
        ew = bbox[2] - bbox[0]
        eh = bbox[3] - bbox[1]
        draw.text((cx - ew // 2, cy - 155 - eh // 2), emoji, font=font_emoji, embedded_color=True)
    except:
        draw.ellipse([cx-80, cy-235, cx+80, cy-75], fill=ACCENT)

    # เส้น accent ทอง
    line_y = cy + 115
    draw.rectangle([cx - 60, line_y, cx + 60, line_y + 4], fill=ACCENT)

    # label
    try:
        bbox = draw.textbbox((0, 0), label, font=font_label)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, cy + 20), label, font=font_label, fill=TEXT_COL)
    except:
        draw.text((cx - 100, cy + 20), label, font=font_label, fill=TEXT_COL)

    # sublabel
    try:
        bbox = draw.textbbox((0, 0), sublabel, font=font_sub)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, cy + 130), sublabel, font=font_sub, fill=SUB_COL)
    except:
        draw.text((cx - 80, cy + 130), sublabel, font=font_sub, fill=SUB_COL)

for i, (em, lb, sl) in enumerate(BUTTONS):
    draw_button(i, em, lb, sl)

# Branding
brand = "FileSaverBot — Admin"
try:
    bbox = draw.textbbox((0, 0), brand, font=font_brand)
    bw = bbox[2] - bbox[0]
    draw.text((W - bw - 30, H - 60), brand, font=font_brand, fill=(200, 160, 80))
except:
    pass

out = "rich_menu_admin.jpg"
img.save(out, "JPEG", quality=92, optimize=True)
size_kb = os.path.getsize(out) / 1024
print(f"[OK] Saved: {out}  ({size_kb:.0f} KB)  {img.size}")
