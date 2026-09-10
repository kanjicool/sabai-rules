"""FastAPI Ingress Webhook & LINE Messaging API Module (Phase 4).

This module manages:
- FastAPI ASGI application
- Signature verification (LINE X-Line-Signature)
- Asynchronous background task dispatch (< 0.2s HTTP 200 OK)
- LINE Flex Message and Quick Reply builder
- Cloudflare Tunnel ingress configuration
"""
