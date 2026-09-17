"""Script to create and register the Sabai-Rules 6-grid Rich Menu via LINE Messaging API.

Layout:
+-------------------+-------------------+-------------------+
| 🏖️ สิทธิ์วันลา     | 💼 ค่าชดเชย        | 🏥 กองทุน PVD      |
+-------------------+-------------------+-------------------+
| ⏰ เวลาทำงาน & OT  | ⚖️ ระเบียบวินัย     | 🧮 เครื่องคิดเลข HR|
+-------------------+-------------------+-------------------+
"""

import io
import sys
from pathlib import Path
from PIL import Image
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    MessagingApiBlob,
    RichMenuRequest,
    RichMenuArea,
    RichMenuBounds,
    RichMenuSize,
    MessageAction
)
from src.config import settings

DIR_PATH = Path(__file__).resolve().parent.parent / "data" / "richmenu"
ACTIVE_PATH = DIR_PATH / "richmenu_2500x1686_active.jpg"
V2_PATH = DIR_PATH / "richmenu_2500x1686_V2.png"
V1_PATH = DIR_PATH / "richmenu_2500x1686.png"


def prepare_richmenu_image() -> tuple[bytes, str]:
    """Prepares and resizes the Rich Menu image to exact 2500x1686 under 1MB."""
    if ACTIVE_PATH.exists():
        source_path = ACTIVE_PATH
    elif V2_PATH.exists():
        source_path = V2_PATH
    else:
        source_path = V1_PATH
    print(f"[INFO] Using source image: {source_path.name}")

    with Image.open(source_path) as im:
        im_rgb = im.convert("RGB")
        # Resize to exact LINE standard dimensions (2500 x 1686)
        if im_rgb.size != (2500, 1686):
            print(f"[INFO] Resizing from {im_rgb.size} to (2500, 1686) with LANCZOS...")
            im_rgb = im_rgb.resize((2500, 1686), Image.Resampling.LANCZOS)

        # Export as JPEG with quality 92 (approx 580 KB, well under 1MB limit)
        buf = io.BytesIO()
        im_rgb.save(buf, format="JPEG", quality=92, optimize=True)
        data = buf.getvalue()
        print(f"[INFO] Processed image size: {len(data):,} bytes ({len(data)/1024:.1f} KB)")
        return data, "image/jpeg"


def setup_richmenu():
    token = settings.LINE_CHANNEL_ACCESS_TOKEN
    if not token:
        print("[ERROR] LINE_CHANNEL_ACCESS_TOKEN is not set in .env file.")
        sys.exit(1)

    config = Configuration(access_token=token)
    api_client = ApiClient(config)
    messaging_api = MessagingApi(api_client)
    messaging_blob = MessagingApiBlob(api_client)

    # 1. Fetch and clean up existing old rich menus
    existing_menus = messaging_api.get_rich_menu_list().richmenus
    old_ids = [m.rich_menu_id for m in existing_menus]

    # 2. Define 6 Grids on 2500 x 1686 Canvas
    # Row 1
    area_leave = RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
        action=MessageAction(text="สรุปสิทธิวันลาทั้งหมด")
    )
    area_severance = RichMenuArea(
        bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
        action=MessageAction(text="ตารางค่าชดเชยการเลิกจ้างมีเกณฑ์อย่างไรบ้าง")
    )
    area_pvd = RichMenuArea(
        bounds=RichMenuBounds(x=1666, y=0, width=834, height=843),
        action=MessageAction(text="เงินสมทบ PVD นายจ้างจ่ายให้กี่เปอร์เซ็นต์")
    )
    # Row 2
    area_ot = RichMenuArea(
        bounds=RichMenuBounds(x=0, y=843, width=833, height=843),
        action=MessageAction(text="ทำโอทีวันหยุดได้เงินกี่เท่า")
    )
    area_discipline = RichMenuArea(
        bounds=RichMenuBounds(x=833, y=843, width=833, height=843),
        action=MessageAction(text="บทลงโทษทางวินัยมีกี่ขั้นตอน อะไรบ้าง")
    )
    area_calc = RichMenuArea(
        bounds=RichMenuBounds(x=1666, y=843, width=834, height=843),
        action=MessageAction(text="เปิดเครื่องคำนวณ HR")
    )

    rich_menu_req = RichMenuRequest(
        size=RichMenuSize(width=2500, height=1686),
        selected=True,
        name="Sabai-Rules V2 Gold Theme",
        chat_bar_text="เมนูข้อบังคับ",
        areas=[area_leave, area_severance, area_pvd, area_ot, area_discipline, area_calc]
    )

    print("[1/3] Creating Rich Menu structure via LINE Messaging API...")
    res = messaging_api.create_rich_menu(rich_menu_req)
    new_rich_menu_id = res.rich_menu_id
    print(f"      Created New Rich Menu ID: {new_rich_menu_id}")

    print("[2/3] Uploading processed Rich Menu image...")
    image_bytes, content_type = prepare_richmenu_image()
    messaging_blob.set_rich_menu_image(
        rich_menu_id=new_rich_menu_id,
        body=image_bytes,
        _headers={"Content-Type": content_type}
    )
    print("      Image uploaded successfully.")

    print("[3/3] Setting as Default Rich Menu for all users...")
    messaging_api.set_default_rich_menu(new_rich_menu_id)
    print("      New Default Rich Menu activated successfully!")

    # Clean up old rich menus
    for old_id in old_ids:
        try:
            messaging_api.delete_rich_menu(old_id)
            print(f"      Cleaned up old rich menu: {old_id}")
        except Exception as e:
            print(f"      Note: Could not delete {old_id}: {e}")

    print("\n=======================================================")
    print(f"SUCCESS: Rich Menu V2 ({new_rich_menu_id}) is now LIVE!")
    print("=======================================================")


if __name__ == "__main__":
    setup_richmenu()
