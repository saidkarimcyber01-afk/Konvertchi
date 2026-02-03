from __future__ import annotations

from aiogram import Router

from bot.handlers import documents, start


def setup_router() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(documents.router)
    return router
