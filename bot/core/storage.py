from __future__ import annotations

from typing import Dict

from bot.models.user import UserSettings


class UserSettingsStore:
    def __init__(self) -> None:
        self._settings: Dict[int, UserSettings] = {}

    def get(self, user_id: int) -> UserSettings:
        return self._settings.get(user_id, UserSettings(user_id=user_id))

    def set_language(self, user_id: int, language: str) -> None:
        settings = self.get(user_id)
        settings.language = language
        self._settings[user_id] = settings
