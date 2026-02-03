from __future__ import annotations

from typing import Optional

from aiogram import Bot
from aiogram.types import Document, PhotoSize


async def download_document(bot: Bot, document: Document) -> bytes:
    file = await bot.get_file(document.file_id)
    downloaded = await bot.download_file(file.file_path)
    return downloaded.read() if hasattr(downloaded, "read") else downloaded


def extract_photo(message_photo: list[PhotoSize]) -> Optional[PhotoSize]:
    if not message_photo:
        return None
    return max(message_photo, key=lambda p: p.file_size or 0)


async def download_photo(bot: Bot, photo: PhotoSize) -> bytes:
    file = await bot.get_file(photo.file_id)
    downloaded = await bot.download_file(file.file_path)
    return downloaded.read() if hasattr(downloaded, "read") else downloaded
