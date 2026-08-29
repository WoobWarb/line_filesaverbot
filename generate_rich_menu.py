"""
Regenerates rich_menu.jpg without underlines using Pillow + Leelawadee font.
Run: python generate_rich_menu.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Leelawadee — built-in Windows Thai font, clean and modern
BOLD    = r'C:\Windows\Fonts\leelawdb.ttf'
REGULAR = r'C:\Windows\Fonts\leelawad.ttf'

# Emoji font (Windows built-in)
EMOJI_FONT_PATH = r'C:\Windows\Fonts\seguiemj.ttf'
HAS_EMOJI_FONT  = os.path.exists(EMOJI_FONT_PATH)

# --- Design constants ---
W, H       = 2500, 1686
COLS, ROWS = 3, 2
CW         = [833, 834, 833]
CH         = [843, 843]
BG         = (13, 27, 46)
CIRCLE     = (22, 42, 68)
TITLE_C    = (255, 255, 255)
SUB_C      = (122, 168, 206)

# --- Cell data ---
CELLS = [
    ('📁', 'ลิงค์ Drive',   'เปิดโฟลเดอร์ไฟล์'),
    ('🔧', 'ตั้งค่า',       'เชื่อม Google Drive'),
    ('💳', 'สมัคร Premium', 'อัปเกรดบัญชี'),
    ('📊', 'เช็คสถานะ',     'ดูการใช้งาน'),
    ('🔄', 'เก็บตก',        'อัปโหลดไฟล์ค้าง'),
    ('💸', 'แจ้งโอน',       'แจ้งชำระเงิน'),
]

def cell_origin(idx):
    col, row = idx % COLS, idx // COLS
    return sum(CW[:col]), sum(CH[:row])

def cell_size(idx):
    return CW[idx % COLS], CH[idx // COLS]

img  = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img, 'RGBA')

# Subtle gradient overlay
for y in range(H):
    alpha = int(18 * (1 - y / H))
    draw.line([(0, y), (W, y)], fill=(255, 255, 255, alpha))

# Grid dividers
x_pos = 0
for cw in CW[:-1]:
    x_pos += cw
    draw.line([(x_pos, 0), (x_pos, H)], fill=(255, 255, 255, 25), width=2)
draw.line([(0, CH[0]), (W, CH[0])], fill=(255, 255, 255, 25), width=2)

# Fonts
f_title    = ImageFont.truetype(BOLD,    82)
f_subtitle = ImageFont.truetype(REGULAR, 56)   # +10 — อ่านง่ายขึ้น
f_brand    = ImageFont.truetype(REGULAR, 34)
f_emoji    = ImageFont.truetype(EMOJI_FONT_PATH, 173) if HAS_EMOJI_FONT else None  # +20%

def draw_cell(idx, emoji, title, subtitle):
    ox, oy = cell_origin(idx)
    cw, ch = cell_size(idx)
    cx     = ox + cw // 2

    # Icon circle — 20% larger (144 -> 173)
    cr     = 173
    icon_y = oy + int(ch * 0.27)
    draw.ellipse([(cx - cr, icon_y - cr), (cx + cr, icon_y + cr)], fill=CIRCLE)

    # Emoji (colored via embedded_color)
    if f_emoji:
        bb = draw.textbbox((0, 0), emoji, font=f_emoji)
        ew, eh = bb[2] - bb[0], bb[3] - bb[1]
        draw.text(
            (cx - ew // 2, icon_y - eh // 2 - bb[1]),
            emoji, font=f_emoji, embedded_color=True
        )
    else:
        draw.ellipse([(cx - 48, icon_y - 48), (cx + 48, icon_y + 48)], fill=TITLE_C)

    # Title
    title_y = oy + int(ch * 0.615)
    bb = draw.textbbox((0, 0), title, font=f_title)
    draw.text((cx - (bb[2] - bb[0]) // 2, title_y), title, font=f_title, fill=TITLE_C)

    # Subtitle — gap เพิ่มจาก 16 -> 28
    sub_y = title_y + (bb[3] - bb[1]) + 28
    bb2   = draw.textbbox((0, 0), subtitle, font=f_subtitle)
    draw.text((cx - (bb2[2] - bb2[0]) // 2, sub_y), subtitle, font=f_subtitle, fill=SUB_C)

for i, (emoji, title, sub) in enumerate(CELLS):
    draw_cell(i, emoji, title, sub)

# Branding
bb = draw.textbbox((0, 0), 'FileSaverBot', font=f_brand)
draw.text((W - bb[2] - 24, H - bb[3] - 24), 'FileSaverBot', font=f_brand, fill=(80, 120, 160))

out = os.path.join(BASE_DIR, 'rich_menu_new.jpg')
img.save(out, 'JPEG', quality=95)
print(f'Saved: {out}')
