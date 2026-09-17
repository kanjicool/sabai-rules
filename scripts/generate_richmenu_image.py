"""Generates a high-resolution (2500 x 1686 px) Rich Menu graphic for Sabai-Rules LINE OA.

Layout: Standard LINE 6-grid (2 rows x 3 columns)
Output: data/richmenu/richmenu_2500x1686.png
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "richmenu"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "richmenu_2500x1686.png"

WIDTH = 2500
HEIGHT = 1686
COLS = 3
ROWS = 2
CELL_W = WIDTH // COLS      # 833 px
CELL_H = HEIGHT // ROWS     # 843 px

ITEMS = [
    # Row 1
    {
        "row": 0, "col": 0,
        "title": "สิทธิ์วันลา",
        "sub": "พักร้อน L1-9, ลาป่วย, คลอด",
        "icon": "🏖️",
        "bg": "#00695c",
        "accent": "#4db6ac"
    },
    {
        "row": 0, "col": 1,
        "title": "ตารางค่าชดเชย",
        "sub": "เลิกจ้าง 30 - 300 วัน",
        "icon": "💼",
        "bg": "#004d40",
        "accent": "#80cbc4"
    },
    {
        "row": 0, "col": 2,
        "title": "กองทุน PVD",
        "sub": "นายจ้างสมทบ 2% - 7%",
        "icon": "🏥",
        "bg": "#00796b",
        "accent": "#a7ffeb"
    },
    # Row 2
    {
        "row": 1, "col": 0,
        "title": "เวลาทำงาน & OT",
        "sub": "อัตราล่วงเวลา 1 - 3 เท่า",
        "icon": "⏰",
        "bg": "#005b4f",
        "accent": "#80e27e"
    },
    {
        "row": 1, "col": 1,
        "title": "ระเบียบวินัย",
        "sub": "โทษ 4 ขั้น, ขาดงาน 3 วัน",
        "icon": "⚖️",
        "bg": "#00483f",
        "accent": "#ffe082"
    },
    {
        "row": 1, "col": 2,
        "title": "เครื่องคิดเลข HR",
        "sub": "คำนวณสิทธิ์วันลา & ค่าชดเชย",
        "icon": "🧮",
        "bg": "#0f766e",
        "accent": "#ffab40"
    }
]


def load_font(size: int):
    """Attempts to load common Windows/Unicode Thai fonts, fallback to default."""
    font_candidates = [
        "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/browa.ttf",
        "C:/Windows/Fonts/leelawad.ttf",
        "C:/Windows/Fonts/seguiemj.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    for p in font_candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def generate_richmenu():
    img = Image.new("RGB", (WIDTH, HEIGHT), color="#0f172a")
    draw = ImageDraw.Draw(img)

    font_title = load_font(68)
    font_sub = load_font(40)
    font_badge = load_font(30)

    for item in ITEMS:
        r = item["row"]
        c = item["col"]
        x1 = c * CELL_W
        y1 = r * CELL_H
        x2 = (c + 1) * CELL_W if c < COLS - 1 else WIDTH
        y2 = (r + 1) * CELL_H if r < ROWS - 1 else HEIGHT

        # Margin within cell
        pad = 12
        card_x1, card_y1, card_x2, card_y2 = x1 + pad, y1 + pad, x2 - pad, y2 - pad

        # Fill background rounded rect
        draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=32, fill=item["bg"])

        # Inner subtle gradient border
        draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=32, outline=item["accent"], width=3)

        # Center content coordinates
        mid_x = (card_x1 + card_x2) // 2
        mid_y = (card_y1 + card_y2) // 2

        # Draw Title
        title_text = f"{item['icon']} {item['title']}"
        draw.text((mid_x, mid_y - 45), title_text, fill="#ffffff", font=font_title, anchor="mm")

        # Draw Subtitle
        draw.text((mid_x, mid_y + 45), item["sub"], fill="#e0f2f1", font=font_sub, anchor="mm")

        # Bottom badge
        badge_rect = [mid_x - 140, card_y2 - 90, mid_x + 140, card_y2 - 35]
        draw.rounded_rectangle(badge_rect, radius=20, fill="#00000044", outline=item["accent"], width=2)
        draw.text((mid_x, card_y2 - 62), "แตะเพื่อดูข้อมูล", fill=item["accent"], font=font_badge, anchor="mm")

    # Add Top branding banner line
    img.save(OUTPUT_PATH, "PNG", quality=95)
    print(f"[OK] Generated Rich Menu Image at: {OUTPUT_PATH} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    generate_richmenu()
