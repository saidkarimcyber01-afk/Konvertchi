from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.core.config import load_config
from bot.core.router import setup_router
from bot.core.storage import UserSettingsStore
from bot.services.document_service import DocumentService


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    bot = Bot(token=config.bot.token)
    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)

    dispatcher["config"] = config
    dispatcher["settings"] = UserSettingsStore()
    dispatcher["service"] = DocumentService()

    dispatcher.include_router(setup_router())
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
