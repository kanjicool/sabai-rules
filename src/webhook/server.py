"""FastAPI Webhook Server for Sabai-Rules LINE Chatbot.

Provides endpoints for:
- GET /health: Health check and service status
- POST /callback: LINE Messaging API Webhook receiver
- POST /ask: Local testing endpoint for Vector RAG queries without LINE
"""

import logging
from pathlib import Path
from fastapi import FastAPI, Request, Header, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, FollowEvent
from src.webhook.line_handler import line_service
from src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sabai_rules.webhook")

app = FastAPI(
    title="Sabai-Rules LINE Chatbot API",
    description="Vector RAG HR Benefit Assistant for Primo Group",
    version="2.1.0"
)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class AskRequest(BaseModel):
    query: str
    top_k: int = 4


@app.get("/")
def index():
    """Root status endpoint."""
    return {
        "status": "online",
        "service": "Sabai-Rules HR Vector RAG Chatbot",
        "version": "2.1.0",
        "endpoints": {
            "health": "/health",
            "webhook": "/callback",
            "local_ask": "/ask",
            "liff_calculator": "/liff/calculator"
        }
    }


@app.get("/liff/calculator", response_class=FileResponse)
def get_liff_calculator():
    """Serves the interactive HR Calculator web app for LINE LIFF."""
    calc_html = STATIC_DIR / "calculator.html"
    if not calc_html.exists():
        raise HTTPException(status_code=404, detail="Calculator page not found")
    return FileResponse(str(calc_html), media_type="text/html")


@app.get("/health")
def health_check():
    """Health check endpoint checking store and components."""
    index_persisted = line_service.rag_engine.store.is_persisted()
    ollama_ok = line_service.rag_engine.llm.is_available()

    return {
        "status": "healthy",
        "vector_index_ready": index_persisted,
        "ollama_available": ollama_ok,
        "line_configured": bool(settings.LINE_CHANNEL_SECRET and settings.LINE_CHANNEL_ACCESS_TOKEN)
    }


@app.post("/ask")
async def local_ask(req: AskRequest):
    """Local debugging endpoint to test Vector RAG responses directly."""
    result = line_service.rag_engine.query(req.query, top_k=req.top_k)
    return {
        "query": result.query,
        "answer": result.answer,
        "citations": result.citations,
        "confidence_score": result.confidence_score,
        "formatted_text": result.format_line_text()
    }


@app.post("/callback")
async def line_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature: str | None = Header(default=None)
):
    """LINE Webhook callback handler supporting Text Messages and Follow Events."""
    body_bytes = await request.body()
    body_text = body_bytes.decode("utf-8")

    # If secret is set, require signature
    if settings.LINE_CHANNEL_SECRET:
        if not x_line_signature:
            raise HTTPException(status_code=400, detail="Missing X-Line-Signature header")
        try:
            events = line_service.parse_events(body_text, x_line_signature)
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="Invalid signature")
    else:
        # Development mode fallback
        events = []

    for event in events:
        user_id = getattr(event.source, "user_id", None)

        # 1. Text Message Event
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            background_tasks.add_task(
                line_service.handle_text_message,
                event.reply_token,
                event.message.text,
                user_id
            )
        # 2. Friend Add / Follow Event
        elif isinstance(event, FollowEvent):
            background_tasks.add_task(
                line_service.handle_follow_event,
                event.reply_token,
                user_id
            )

    return JSONResponse(content={"status": "OK"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.webhook.server:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
