"""Unit tests for LINE Chatbot UX improvements:
- Quick Replies (label length <= 20 chars)
- Welcome Onboarding Flex Card
- Leave Carousel Flex Message
- HR Calculator LIFF endpoint
"""

import pytest
from fastapi.testclient import TestClient
from src.webhook.flex_templates import (
    get_quick_replies,
    create_welcome_flex,
    create_leave_carousel,
    create_calculator_card,
    create_faq_carousel
)
from src.webhook.server import app

client = TestClient(app)


def test_quick_replies_label_length():
    """LINE Messaging API requires action label to be at most 20 characters."""
    topics = ["ลาพักร้อน", "เลิกจ้างชดเชย", "กองทุน PVD", "วินัย", "โอที", ""]
    for topic in topics:
        qr = get_quick_replies(topic)
        assert qr is not None
        assert len(qr.items) > 0
        for item in qr.items:
            label = item.action.label
            assert len(label) <= 20, f"Label '{label}' exceeds 20 characters limit ({len(label)} chars)"


def test_welcome_flex_structure():
    """Verifies welcome card format for FollowEvent."""
    bubble = create_welcome_flex()
    assert bubble["type"] == "bubble"
    assert "header" in bubble
    assert "body" in bubble
    assert "footer" in bubble
    assert bubble["header"]["backgroundColor"] == "#009688"


def test_leave_carousel_structure():
    """Verifies 4-card leave carousel structure."""
    carousel = create_leave_carousel()
    assert carousel["type"] == "carousel"
    assert len(carousel["contents"]) == 4
    for card in carousel["contents"]:
        assert card["type"] == "bubble"
        assert "header" in card
        assert "body" in card
        assert "footer" in card


def test_faq_carousel_structure():
    """Verifies 4-card FAQ carousel structure with categorized questions."""
    carousel = create_faq_carousel()
    assert carousel["type"] == "carousel"
    assert len(carousel["contents"]) == 4
    for card in carousel["contents"]:
        assert card["type"] == "bubble"
        assert "header" in card
        assert "body" in card
        assert "footer" in card
        # Ensure buttons exist in body
        assert len(card["body"]["contents"]) >= 3


def test_calculator_card_structure():
    """Verifies promotional card for LIFF calculator."""
    bubble = create_calculator_card("https://test.url/liff/calculator")
    assert bubble["type"] == "bubble"
    assert bubble["footer"]["contents"][0]["action"]["type"] == "uri"


def test_liff_calculator_endpoint():
    """Verifies GET /liff/calculator returns 200 and serves HTML."""
    response = client.get("/liff/calculator")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Sabai HR Calculator" in response.text
    assert "calcLeave" in response.text
    assert "calcSeverance" in response.text
    assert "calcPVD" in response.text
