from __future__ import annotations

from typing import Dict

from bot.i18n.ru import MESSAGES as RU_MESSAGES
from bot.i18n.uz import MESSAGES as UZ_MESSAGES


I18N_MAP: Dict[str, Dict[str, str]] = {
    "ru": RU_MESSAGES,
    "uz": UZ_MESSAGES,
}


def t(language: str, key: str, **kwargs: str) -> str:
    messages = I18N_MAP.get(language, RU_MESSAGES)
    text = messages.get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
