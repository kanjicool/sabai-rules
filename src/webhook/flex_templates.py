"""LINE Flex Message templates and Quick Reply generators.

Provides rich visual representations for:
- Context-aware Quick Reply chips (max 20 chars label)
- Onboarding / Follow Event Welcome Flex Card
- Multi-category Carousel Flex Messages (Leave Policies, Benefits)
- HR Calculator promotion bubble
"""

from typing import Any
from linebot.v3.messaging import (
    QuickReply,
    QuickReplyItem,
    MessageAction,
    URIAction
)


def get_quick_replies(query: str = "") -> QuickReply:
    """Generates context-aware Quick Reply chips based on user query topic.
    
    Note: LINE restricts action.label to a maximum of 20 characters.
    """
    q = query.lower() if query else ""

    if any(k in q for k in ["ลา", "พักร้อน", "ลาป่วย", "คลอด", "leave"]):
        items = [
            QuickReplyItem(action=MessageAction(label="🏖️ พักร้อนระดับ 3", text="พนักงานระดับ 3 มีสิทธิ์ลาพักร้อนกี่วัน")),
            QuickReplyItem(action=MessageAction(label="🤒 ใบรับรองลาป่วย", text="ลาป่วยกี่วันต้องใช้ใบรับรองแพทย์ ได้เงินเดือนกี่วัน")),
            QuickReplyItem(action=MessageAction(label="👶 สิทธิการลาคลอด", text="ท้อง ลาคลอดได้กี่วัน ได้รับค่าจ้างไหม")),
            QuickReplyItem(action=MessageAction(label="🌴 พักร้อนสะสมได้ไหม", text="ถ้าใช้สิทธิวันลาพักผ่อนไม่หมด สะสมได้ไหม")),
            QuickReplyItem(action=MessageAction(label="❓ รวมคำถามพบบ่อย", text="รวมคำถามที่พบบ่อย")),
            QuickReplyItem(action=MessageAction(label="🧮 คำนวณวันลา", text="เปิดเครื่องคำนวณ HR")),
        ]
    elif any(k in q for k in ["ชดเชย", "เลิกจ้าง", "ไล่ออก", "พ้นสภาพ", "severance"]):
        items = [
            QuickReplyItem(action=MessageAction(label="💼 ทำงาน 4 ปีชดเชย", text="ทำงานมา 4 ปี ถ้าถูกเลิกจ้างจะได้เงินชดเชยกี่วัน")),
            QuickReplyItem(action=MessageAction(label="📊 ตารางค่าชดเชย", text="ตารางค่าชดเชยการเลิกจ้างมีเกณฑ์อย่างไรบ้าง")),
            QuickReplyItem(action=MessageAction(label="🚪 ลาออกได้เงินไหม", text="ลาออกเองได้เงินชดเชยไหม")),
            QuickReplyItem(action=MessageAction(label="❓ รวมคำถามพบบ่อย", text="รวมคำถามที่พบบ่อย")),
            QuickReplyItem(action=MessageAction(label="🧮 คำนวณค่าชดเชย", text="เปิดเครื่องคำนวณ HR")),
        ]
    elif any(k in q for k in ["กองทุน", "pvd", "สมทบ", "สำรองเลี้ยงชีพ"]):
        items = [
            QuickReplyItem(action=MessageAction(label="🏥 กองทุน PVD คืออะไร", text="กองทุน PVD คืออะไร")),
            QuickReplyItem(action=MessageAction(label="💰 นายจ้างสมทบกี่ %", text="เงินสมทบ PVD นายจ้างจ่ายให้กี่เปอร์เซ็นต์")),
            QuickReplyItem(action=MessageAction(label="🕊️ เงินช่วยงานศพ", text="ถ้าครอบครัวพนักงานเสียชีวิต บริษัทมีเงินช่วยเหลืออะไรบ้าง")),
            QuickReplyItem(action=MessageAction(label="🩺 ประกันสุขภาพ", text="ประกันสุขภาพพนักงานคุ้มครองอะไรบ้าง")),
            QuickReplyItem(action=MessageAction(label="❓ รวมคำถามพบบ่อย", text="รวมคำถามที่พบบ่อย")),
            QuickReplyItem(action=MessageAction(label="🧮 คำนวณเงิน PVD", text="เปิดเครื่องคำนวณ HR")),
        ]
    elif any(k in q for k in ["วินัย", "เตือน", "ลงโทษ", "ผิด", "ร้องทุกข์"]):
        items = [
            QuickReplyItem(action=MessageAction(label="⚖️ ลำดับโทษวินัย", text="บทลงโทษทางวินัยมีกี่ขั้นตอน อะไรบ้าง")),
            QuickReplyItem(action=MessageAction(label="⏳ อายุหนังสือเตือน", text="หนังสือเตือนมีอายุกี่ปี เมื่อไหร่ถึงจะหมดผล")),
            QuickReplyItem(action=MessageAction(label="📢 ขั้นตอนร้องทุกข์", text="ขั้นตอนการร้องทุกข์ของพนักงานต้องทำอย่างไร")),
            QuickReplyItem(action=MessageAction(label="❓ รวมคำถามพบบ่อย", text="รวมคำถามที่พบบ่อย")),
        ]
    elif any(k in q for k in ["ot", "โอที", "ล่วงเวลา", "เวลาทำงาน", "ทดลองงาน"]):
        items = [
            QuickReplyItem(action=MessageAction(label="⏰ โอทีวันหยุดกี่เท่า", text="ทำโอทีวันหยุดได้เงินกี่เท่า")),
            QuickReplyItem(action=MessageAction(label="⏳ ทดลองงานกี่วัน", text="ระยะเวลาทดลองงานของพนักงานใหม่มีกี่วัน")),
            QuickReplyItem(action=MessageAction(label="⏱️ สูตรคำนวณ OT", text="การคิดเงินค่าล่วงเวลา OT มีสูตรคำนวณอย่างไร")),
            QuickReplyItem(action=MessageAction(label="❓ รวมคำถามพบบ่อย", text="รวมคำถามที่พบบ่อย")),
        ]
    else:
        # Default starter quick replies - top frequent questions
        items = [
            QuickReplyItem(action=MessageAction(label="❓ รวมคำถามพบบ่อย", text="รวมคำถามที่พบบ่อย")),
            QuickReplyItem(action=MessageAction(label="🏖️ สิทธิ์วันลา", text="สรุปสิทธิวันลาทั้งหมด")),
            QuickReplyItem(action=MessageAction(label="💼 ตารางค่าชดเชย", text="ตารางค่าชดเชยการเลิกจ้างมีเกณฑ์อย่างไรบ้าง")),
            QuickReplyItem(action=MessageAction(label="🏥 กองทุน PVD คืออะไร", text="กองทุน PVD คืออะไร")),
            QuickReplyItem(action=MessageAction(label="⏰ โอทีวันหยุดกี่เท่า", text="ทำโอทีวันหยุดได้เงินกี่เท่า")),
            QuickReplyItem(action=MessageAction(label="⏳ ทดลองงานกี่วัน", text="ระยะเวลาทดลองงานของพนักงานใหม่มีกี่วัน")),
            QuickReplyItem(action=MessageAction(label="🤒 ใบรับรองลาป่วย", text="ลาป่วยกี่วันต้องใช้ใบรับรองแพทย์ ได้เงินเดือนกี่วัน")),
            QuickReplyItem(action=MessageAction(label="🕊️ เงินช่วยงานศพ", text="ถ้าครอบครัวพนักงานเสียชีวิต บริษัทมีเงินช่วยเหลืออะไรบ้าง")),
            QuickReplyItem(action=MessageAction(label="🧮 เครื่องคำนวณ HR", text="เปิดเครื่องคำนวณ HR")),
        ]

    return QuickReply(items=items)


def create_welcome_flex() -> dict[str, Any]:
    """Builds a friendly Onboarding Welcome Flex Message when adding as friend."""
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#009688",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "🌿 Sabai-Rules Assistant",
                    "color": "#ffffff",
                    "weight": "bold",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": "ผู้ช่วยระเบียบข้อบังคับและสิทธิประโยชน์ (PRIMO)",
                    "color": "#e0f2f1",
                    "size": "xs",
                    "margin": "sm"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "ยินดีต้อนรับครับ! 👋",
                    "weight": "bold",
                    "size": "md",
                    "color": "#1b5e20"
                },
                {
                    "type": "text",
                    "text": "ผมพร้อมช่วยตอบคำถามเกี่ยวกับกฎระเบียบ สวัสดิการ วันลาพักร้อน ค่าชดเชย และกองทุนสำรองเลี้ยงชีพ จากเอกสารทางการ 47 หน้า อย่างแม่นยำ พร้อมอ้างอิงเลขหน้าทุกคำตอบครับ",
                    "size": "xs",
                    "color": "#555555",
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "💡 ลองกดถามประเด็นยอดนิยมด้านล่างนี้ได้เลย:",
                    "size": "xs",
                    "weight": "bold",
                    "color": "#333333"
                },
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "color": "#00897b",
                    "action": {
                        "type": "message",
                        "label": "❓ รวมคำถามพบบ่อย (FAQ)",
                        "text": "รวมคำถามที่พบบ่อย"
                    }
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "color": "#e0f2f1",
                    "action": {
                        "type": "message",
                        "label": "🏖️ พนักงาน L3 ลาพักร้อนกี่วัน",
                        "text": "พนักงานระดับ 3 มีสิทธิ์ลาพักร้อนกี่วัน"
                    }
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "color": "#e0f2f1",
                    "action": {
                        "type": "message",
                        "label": "💼 ตารางค่าชดเชยเลิกจ้าง",
                        "text": "ตารางค่าชดเชยการเลิกจ้างมีเกณฑ์อย่างไรบ้าง"
                    }
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "color": "#e0f2f1",
                    "action": {
                        "type": "message",
                        "label": "🏥 เงินสมทบกองทุน PVD",
                        "text": "เงินสมทบ PVD นายจ้างจ่ายให้กี่เปอร์เซ็นต์"
                    }
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "color": "#0f766e",
                    "action": {
                        "type": "message",
                        "label": "🧮 เปิดเครื่องคำนวณสิทธิ์ HR",
                        "text": "เปิดเครื่องคำนวณ HR"
                    }
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "พิมพ์คำถามเป็นภาษาพูดได้ตลอด 24 ชั่วโมง 💬",
                    "size": "xxs",
                    "color": "#999999",
                    "align": "center"
                }
            ]
        }
    }


def create_leave_carousel() -> dict[str, Any]:
    """Builds an interactive 4-card Carousel Flex Message summarizing all leave policies."""
    cards = [
        {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#00897b",
                "contents": [
                    {"type": "text", "text": "🏖️ ลาพักผ่อนประจำปี", "color": "#ffffff", "weight": "bold", "size": "sm"},
                    {"type": "text", "text": "ตามระดับตำแหน่ง (หมวด 4)", "color": "#e0f2f1", "size": "xxs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "• ระดับ 1–2: 6 วันทำงาน/ปี", "size": "xs", "color": "#333333"},
                    {"type": "text", "text": "• ระดับ 3–5: 7 วันทำงาน/ปี", "size": "xs", "color": "#333333", "weight": "bold"},
                    {"type": "text", "text": "• ระดับ 6–8: 8 วันทำงาน/ปี", "size": "xs", "color": "#333333"},
                    {"type": "text", "text": "• ระดับ 9: 10 วันทำงาน/ปี", "size": "xs", "color": "#333333"},
                    {"type": "separator", "margin": "sm"},
                    {"type": "text", "text": "เงื่อนไข: ครบอายุงาน 1 ปีขึ้นไป", "size": "xxs", "color": "#888888", "margin": "sm"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "color": "#00897b",
                        "action": {
                            "type": "message",
                            "label": "ถามระดับ 3",
                            "text": "พนักงานระดับ 3 มีสิทธิ์ลาพักร้อนกี่วัน"
                        }
                    }
                ]
            }
        },
        {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#1e88e5",
                "contents": [
                    {"type": "text", "text": "🤒 ลาป่วย & ลากิจ", "color": "#ffffff", "weight": "bold", "size": "sm"},
                    {"type": "text", "text": "ข้อกำหนดใบรับรองแพทย์", "color": "#e3f2fd", "size": "xxs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "• ลาป่วย: ได้ตามจริง ได้รับค่าจ้างไม่เกิน 30 วัน/ปี", "size": "xs", "color": "#333333", "wrap": True},
                    {"type": "text", "text": "• ลาตั้งแต่ 3 วันขึ้นไป: ต้องแนบใบรับรองแพทย์แผนปัจจุบัน", "size": "xs", "color": "#d32f2f", "wrap": True, "weight": "bold"},
                    {"type": "text", "text": "• ลากิจธุระจำเป็น: ยื่นล่วงหน้า", "size": "xs", "color": "#333333", "margin": "xs"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "color": "#1e88e5",
                        "action": {
                            "type": "message",
                            "label": "เงื่อนไขลาป่วย",
                            "text": "ลาป่วยกี่วันต้องใช้ใบรับรองแพทย์ ได้เงินเดือนกี่วัน"
                        }
                    }
                ]
            }
        },
        {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#e91e63",
                "contents": [
                    {"type": "text", "text": "👶 ลาเพื่อคลอดบุตร", "color": "#ffffff", "weight": "bold", "size": "sm"},
                    {"type": "text", "text": "คุ้มครองตามกฎหมายแรงงาน", "color": "#fce4ec", "size": "xxs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "• จำนวนวันลา: ไม่เกิน 98 วัน (นับรวมวันหยุด)", "size": "xs", "color": "#333333", "wrap": True},
                    {"type": "text", "text": "• การจ่ายค่าจ้าง: ได้รับค่าจ้างไม่เกิน 45 วันทำงาน", "size": "xs", "color": "#ad1457", "wrap": True, "weight": "bold"},
                    {"type": "text", "text": "• รวมวันลาตรวจครรภ์ก่อนคลอด", "size": "xxs", "color": "#888888", "margin": "xs"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "color": "#e91e63",
                        "action": {
                            "type": "message",
                            "label": "รายละเอียดลาคลอด",
                            "text": "ท้อง ลาคลอดได้กี่วัน ได้รับค่าจ้างไหม"
                        }
                    }
                ]
            }
        },
        {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#5e35b1",
                "contents": [
                    {"type": "text", "text": "🕊️ วันลาอื่นๆ", "color": "#ffffff", "weight": "bold", "size": "sm"},
                    {"type": "text", "text": "ฌาปนกิจ ทำหมัน รับราชการ", "color": "#ede7f6", "size": "xxs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "• ลาฌาปนกิจ: บิดา มารดา คู่สมรส บุตร", "size": "xs", "color": "#333333"},
                    {"type": "text", "text": "• ลาทำหมัน: ตามที่แพทย์ระบุ", "size": "xs", "color": "#333333"},
                    {"type": "text", "text": "• ลารับราชการทหาร: ไม่เกิน 60 วัน", "size": "xs", "color": "#333333"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "color": "#5e35b1",
                        "action": {
                            "type": "message",
                            "label": "เงินช่วยงานศพ",
                            "text": "ถ้าครอบครัวพนักงานเสียชีวิต บริษัทมีเงินช่วยเหลืออะไรบ้าง"
                        }
                    }
                ]
            }
        }
    ]

    return {
        "type": "carousel",
        "contents": cards
    }


def create_faq_carousel() -> dict[str, Any]:
    """Builds an interactive 4-card Carousel Flex Message for Frequently Asked Questions (FAQ)."""
    cards = [
        {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#00897b",
                "paddingAll": "14px",
                "contents": [
                    {"type": "text", "text": "🏖️ หมวดวันลา & วันหยุด", "color": "#ffffff", "weight": "bold", "size": "sm"},
                    {"type": "text", "text": "คำถามยอดนิยมเรื่องสิทธิ์การลา", "color": "#e0f2f1", "size": "xxs", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#f0fdf4",
                        "action": {
                            "type": "message",
                            "label": "🏖️ ระดับ 3 ลาพักร้อนกี่วัน",
                            "text": "พนักงานระดับ 3 มีสิทธิ์ลาพักร้อนกี่วัน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#f0fdf4",
                        "action": {
                            "type": "message",
                            "label": "🤒 ใบรับรองแพทย์ลาป่วย",
                            "text": "ลาป่วยกี่วันต้องใช้ใบรับรองแพทย์ ได้เงินเดือนกี่วัน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#f0fdf4",
                        "action": {
                            "type": "message",
                            "label": "👶 สิทธิการลาคลอดบุตร",
                            "text": "ท้อง ลาคลอดได้กี่วัน ได้รับค่าจ้างไหม"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#f0fdf4",
                        "action": {
                            "type": "message",
                            "label": "🌴 พักร้อนสะสมได้ไหม",
                            "text": "ถ้าใช้สิทธิวันลาพักผ่อนไม่หมด สะสมได้ไหม"
                        }
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "color": "#00897b",
                        "action": {
                            "type": "message",
                            "label": "📋 สรุปสิทธิวันลาทั้งหมด",
                            "text": "สรุปสิทธิวันลาทั้งหมด"
                        }
                    }
                ]
            }
        },
        {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#1e88e5",
                "paddingAll": "14px",
                "contents": [
                    {"type": "text", "text": "💼 หมวดค่าชดเชย & เลิกจ้าง", "color": "#ffffff", "weight": "bold", "size": "sm"},
                    {"type": "text", "text": "เกณฑ์ค่าชดเชยตามกฎหมายแรงงาน", "color": "#e3f2fd", "size": "xxs", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#eff6ff",
                        "action": {
                            "type": "message",
                            "label": "💼 ทำงาน 4 ปี ชดเชยกี่วัน",
                            "text": "ทำงานมา 4 ปี ถ้าถูกเลิกจ้างจะได้เงินชดเชยกี่วัน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#eff6ff",
                        "action": {
                            "type": "message",
                            "label": "📊 เกณฑ์ตารางค่าชดเชย",
                            "text": "ตารางค่าชดเชยการเลิกจ้างมีเกณฑ์อย่างไรบ้าง"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#eff6ff",
                        "action": {
                            "type": "message",
                            "label": "📢 เลิกจ้างบอกล่วงหน้ากี่วัน",
                            "text": "การเลิกจ้างต้องบอกกล่าวล่วงหน้ากี่วัน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#eff6ff",
                        "action": {
                            "type": "message",
                            "label": "🚪 ลาออกเองได้เงินชดเชยไหม",
                            "text": "ลาออกเองได้เงินชดเชยไหม"
                        }
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "color": "#1e88e5",
                        "action": {
                            "type": "message",
                            "label": "🧮 คำนวณค่าชดเชย HR",
                            "text": "เปิดเครื่องคำนวณ HR"
                        }
                    }
                ]
            }
        },
        {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#0f766e",
                "paddingAll": "14px",
                "contents": [
                    {"type": "text", "text": "🏥 กองทุน PVD & สวัสดิการ", "color": "#ffffff", "weight": "bold", "size": "sm"},
                    {"type": "text", "text": "เงินสมทบ & เงินช่วยเหลือครอบครัว", "color": "#ccfbf1", "size": "xxs", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#f0fdfa",
                        "action": {
                            "type": "message",
                            "label": "🏥 กองทุน PVD คืออะไร",
                            "text": "กองทุน PVD คืออะไร"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#f0fdfa",
                        "action": {
                            "type": "message",
                            "label": "💰 นายจ้างสมทบ PVD กี่ %",
                            "text": "เงินสมทบ PVD นายจ้างจ่ายให้กี่เปอร์เซ็นต์"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#f0fdfa",
                        "action": {
                            "type": "message",
                            "label": "🕊️ เงินช่วยเหลือค่าทำศพ",
                            "text": "ถ้าครอบครัวพนักงานเสียชีวิต บริษัทมีเงินช่วยเหลืออะไรบ้าง"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#f0fdfa",
                        "action": {
                            "type": "message",
                            "label": "🩺 ประกันสุขภาพคุ้มครอง",
                            "text": "ประกันสุขภาพพนักงานคุ้มครองอะไรบ้าง"
                        }
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "color": "#0f766e",
                        "action": {
                            "type": "message",
                            "label": "🧮 คำนวณเงิน PVD สะสม",
                            "text": "เปิดเครื่องคำนวณ HR"
                        }
                    }
                ]
            }
        },
        {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#6a1b9a",
                "paddingAll": "14px",
                "contents": [
                    {"type": "text", "text": "⏰ เวลาทำงาน OT & วินัย", "color": "#ffffff", "weight": "bold", "size": "sm"},
                    {"type": "text", "text": "ชั่วโมงทำงาน ค่าล่วงเวลา บทลงโทษ", "color": "#f3e5f5", "size": "xxs", "margin": "xs"}
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#faf5ff",
                        "action": {
                            "type": "message",
                            "label": "⏰ โอทีวันหยุดได้กี่เท่า",
                            "text": "ทำโอทีวันหยุดได้เงินกี่เท่า"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#faf5ff",
                        "action": {
                            "type": "message",
                            "label": "⏳ ทดลองงานกี่วัน",
                            "text": "ระยะเวลาทดลองงานของพนักงานใหม่มีกี่วัน"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#faf5ff",
                        "action": {
                            "type": "message",
                            "label": "⚖️ ลำดับโทษทางวินัย",
                            "text": "บทลงโทษทางวินัยมีกี่ขั้นตอน อะไรบ้าง"
                        }
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "color": "#faf5ff",
                        "action": {
                            "type": "message",
                            "label": "⏳ อายุหนังสือเตือนกี่ปี",
                            "text": "หนังสือเตือนมีอายุกี่ปี เมื่อไหร่ถึงจะหมดผล"
                        }
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "color": "#6a1b9a",
                        "action": {
                            "type": "message",
                            "label": "📢 ขั้นตอนร้องทุกข์",
                            "text": "ขั้นตอนการร้องทุกข์ของพนักงานต้องทำอย่างไร"
                        }
                    }
                ]
            }
        }
    ]

    return {
        "type": "carousel",
        "contents": cards
    }


def create_calculator_card(calculator_url: str = "/liff/calculator") -> dict[str, Any]:
    """Builds a promotional Flex Card linking to the Interactive HR Calculator."""
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#0f766e",
            "paddingAll": "18px",
            "contents": [
                {
                    "type": "text",
                    "text": "🧮 Sabai HR Calculator",
                    "color": "#ffffff",
                    "weight": "bold",
                    "size": "md"
                },
                {
                    "type": "text",
                    "text": "เครื่องมือคำนวณสิทธิประโยชน์อัตโนมัติ",
                    "color": "#ccfbf1",
                    "size": "xs"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": "เลือกคำนวณสิทธิ์ของคุณได้ทันที ไม่ต้องเปิดตาราง:",
                    "size": "xs",
                    "color": "#333333",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "🌴 คำนวณวันลาพักร้อนสะสมตาม Level (1–9)",
                    "size": "xs",
                    "color": "#555555"
                },
                {
                    "type": "text",
                    "text": "💼 คำนวณเงินค่าชดเชยตามอายุงาน (ม.118)",
                    "size": "xs",
                    "color": "#555555"
                },
                {
                    "type": "text",
                    "text": "🏥 คำนวณเงินสมทบกองทุนสำรองเลี้ยงชีพ PVD (2–7%)",
                    "size": "xs",
                    "color": "#555555"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#0f766e",
                    "action": {
                        "type": "uri",
                        "label": "🚀 เปิดเครื่องคำนวณสิทธิ์ทันที",
                        "uri": calculator_url
                    }
                }
            ]
        }
    }

