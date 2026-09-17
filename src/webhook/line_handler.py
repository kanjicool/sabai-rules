"""LINE Bot Webhook Handler for Vector RAG Assistant.

Handles webhook verification, message parsing, and asynchronous reply
dispatching using line-bot-sdk v3.
"""

import json
import logging
from typing import Any
from linebot.v3 import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import httpx
from src.config import settings
from src.rag.vector_rag import VectorRAGEngine

from src.webhook.flex_templates import (
    get_quick_replies,
    create_welcome_flex,
    create_leave_carousel,
    create_calculator_card,
    create_faq_carousel
)

logger = logging.getLogger(__name__)


def resolve_calculator_url() -> str:
    """Dynamically resolves the public URL for HR Calculator."""
    # 1. First priority: Auto-detect from active cloudflared tunnel if running
    try:
        import subprocess, re
        task_out = subprocess.check_output(
            ["tasklist", "/FI", "IMAGENAME eq cloudflared.exe", "/FO", "CSV"],
            text=True,
            stderr=subprocess.DEVNULL
        )
        pids = {line.split(",")[1].strip('"') for line in task_out.splitlines() if "cloudflared.exe" in line}
        if pids:
            net_out = subprocess.check_output(
                ["netstat", "-ano", "-p", "tcp"],
                text=True,
                stderr=subprocess.DEVNULL
            )
            for line in net_out.splitlines():
                if any(pid in line for pid in pids) and "LISTENING" in line:
                    m = re.search(r"127\.0\.0\.1:(\d+)", line)
                    if m:
                        port = m.group(1)
                        try:
                            with httpx.Client(timeout=0.6) as client:
                                r = client.get(f"http://127.0.0.1:{port}/metrics")
                                match = re.search(r'userHostname="([^"]+)"', r.text)
                                if match:
                                    detected = match.group(1).rstrip("/")
                                    logger.info(f"Auto-detected active Cloudflare tunnel: {detected}")
                                    return f"{detected}/liff/calculator"
                        except Exception:
                            pass
    except Exception as e:
        logger.debug(f"Cloudflared auto-detection skipped: {e}")

    # 2. Fallback to settings.PUBLIC_URL from .env
    if settings.PUBLIC_URL:
        return f"{settings.PUBLIC_URL.rstrip('/')}/liff/calculator"

    # 3. Fallback to localhost
    return f"http://localhost:{settings.PORT}/liff/calculator"


class LineBotService:
    """Service to process LINE webhook events and dispatch Vector RAG replies."""

    def __init__(self):
        self.secret = settings.LINE_CHANNEL_SECRET
        self.token = settings.LINE_CHANNEL_ACCESS_TOKEN
        self.rag_engine = VectorRAGEngine()

        if self.secret:
            self.parser = WebhookParser(self.secret)
        else:
            self.parser = None
            logger.warning("LINE_CHANNEL_SECRET not set. Running in development test mode.")

        if self.token:
            configuration = Configuration(access_token=self.token)
            self.api_client = ApiClient(configuration)
            self.messaging_api = MessagingApi(self.api_client)
        else:
            self.messaging_api = None
            logger.warning("LINE_CHANNEL_ACCESS_TOKEN not set. Running in development test mode.")

    async def show_loading_animation(self, user_id: str, loading_seconds: int = 20):
        """Displays bouncing loading dots ('กำลังพิมพ์...') in LINE chat immediately."""
        if not self.token or not user_id:
            return
        url = "https://api.line.me/v2/bot/chat/loading/start"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "chatId": user_id,
            "loadingSeconds": loading_seconds
        }
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 202:
                    logger.info(f"LINE Loading indicator started for user {user_id[:8]}...")
        except Exception as e:
            logger.debug(f"Could not trigger LINE loading animation: {e}")

    def parse_events(self, body: str, signature: str) -> list[Any]:
        """Parses and validates signature of LINE webhook payload."""
        if not self.parser:
            # Test mode: return empty or bypass
            return []
        try:
            return self.parser.parse(body, signature)
        except InvalidSignatureError:
            logger.error("Invalid LINE signature received.")
            raise

    async def handle_follow_event(self, reply_token: str, user_id: str | None = None):
        """Handles new friend add / follow event with a rich Welcome Onboarding Flex card."""
        logger.info(f"User {user_id} followed the bot. Sending welcome onboarding card.")
        welcome_bubble = create_welcome_flex()
        quick_reply = get_quick_replies()

        if self.messaging_api and reply_token != "dummy_token":
            try:
                flex_container = FlexContainer.from_dict(welcome_bubble)
                flex_message = FlexMessage(
                    alt_text="ยินดีต้อนรับสู่ Sabai-Rules HR Assistant 🌿",
                    contents=flex_container,
                    quick_reply=quick_reply
                )
                self.messaging_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[flex_message]
                    )
                )
                logger.info("Successfully sent Welcome Flex message to LINE.")
            except Exception as e:
                logger.error(f"Failed sending Welcome Flex message: {e}")
                self.messaging_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(
                            text="ยินดีต้อนรับสู่ Sabai-Rules HR Assistant! 🌿\nพิมพ์ถามสิทธิ์วันลา ค่าชดเชย หรือสวัสดิการได้เลยครับ",
                            quick_reply=quick_reply
                        )]
                    )
                )

    async def handle_text_message(self, reply_token: str, user_text: str, user_id: str | None = None) -> str:
        """Processes user question through Vector RAG and sends reply to LINE with Quick Replies."""
        if user_id:
            await self.show_loading_animation(user_id)

        clean_text = user_text.strip()
        logger.info(f"Received user query: {clean_text}")
        quick_reply = get_quick_replies(clean_text)

        # 1. Interactive Shortcut: Direct Calculator Request
        if any(kw in clean_text.lower() for kw in ["เปิดเครื่องคำนวณ", "เครื่องคิดเลข", "เครื่องคำนวณ"]):
            calc_url = resolve_calculator_url()
            calc_dict = create_calculator_card(calculator_url=calc_url)
            if self.messaging_api and reply_token != "dummy_token":
                try:
                    flex_container = FlexContainer.from_dict(calc_dict)
                    self.messaging_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=reply_token,
                            messages=[FlexMessage(alt_text="HR Calculator", contents=flex_container, quick_reply=quick_reply)]
                        )
                    )
                except Exception as e:
                    logger.warning(f"Failed sending Calculator card: {e}")
            else:
                logger.info(f"[Mock Reply] Would send Calculator Card with URL: {calc_url}")
            return "Opened HR Calculator"

        # 2. Interactive Shortcut: All Leave Types Carousel
        if any(kw in clean_text for kw in ["สรุปสิทธิวันลาทั้งหมด", "สิทธิการลาทั้งหมด", "ประเภทการลาทั้งหมด"]):
            carousel_dict = create_leave_carousel()
            if self.messaging_api and reply_token != "dummy_token":
                try:
                    flex_container = FlexContainer.from_dict(carousel_dict)
                    self.messaging_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=reply_token,
                            messages=[FlexMessage(alt_text="สรุปสิทธิวันลา 4 ประเภท", contents=flex_container, quick_reply=quick_reply)]
                        )
                    )
                except Exception as e:
                    logger.warning(f"Failed sending Leave Carousel: {e}")
            else:
                logger.info("[Mock Reply] Would send Leave Carousel")
            return "Sent Leave Carousel"

        # 3. Interactive Shortcut: Frequently Asked Questions (FAQ) Carousel
        if any(kw in clean_text.lower() for kw in [
            "คำถามที่พบบ่อย", "คำถามบ่อย", "คำถามยอดนิยม", "คำถามฮิต", 
            "faq", "รวมคำถาม", "มีคำถามอะไรบ้าง", "คำถามแนะนำ"
        ]):
            faq_dict = create_faq_carousel()
            if self.messaging_api and reply_token != "dummy_token":
                try:
                    flex_container = FlexContainer.from_dict(faq_dict)
                    self.messaging_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=reply_token,
                            messages=[FlexMessage(alt_text="รวมคำถามพบบ่อย (FAQ)", contents=flex_container, quick_reply=quick_reply)]
                        )
                    )
                except Exception as e:
                    logger.warning(f"Failed sending FAQ Carousel: {e}")
            else:
                logger.info("[Mock Reply] Would send FAQ Carousel")
            return "Sent FAQ Carousel"

        # 4. Standard RAG Query Flow
        rag_result = self.rag_engine.query(clean_text, top_k=3)
        formatted_reply = rag_result.format_line_text()

        if self.messaging_api and reply_token != "dummy_token":
            try:
                # Send Flex Message with Quick Reply chips
                flex_dict = rag_result.to_flex_bubble()
                flex_container = FlexContainer.from_dict(flex_dict)
                flex_message = FlexMessage(
                    alt_text="HR Benefit Answer",
                    contents=flex_container,
                    quick_reply=quick_reply
                )

                self.messaging_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[flex_message]
                    )
                )
                logger.info("Successfully sent Flex Message with Quick Replies to LINE.")
            except Exception as e:
                logger.warning(f"Failed sending Flex Message, falling back to text: {e}")
                self.messaging_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[TextMessage(text=formatted_reply, quick_reply=quick_reply)]
                    )
                )
        else:
            logger.info("[Mock Reply] Would send to LINE with Quick Replies:\n" + formatted_reply)

        return formatted_reply


line_service = LineBotService()
