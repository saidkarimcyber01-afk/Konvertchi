from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class BotConfig:
    token: str
    max_file_size_mb: int = 20


@dataclass(frozen=True)
class AppConfig:
    bot: BotConfig


def load_config() -> AppConfig:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")
    max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "20"))
    return AppConfig(bot=BotConfig(token=token, max_file_size_mb=max_file_size_mb))
