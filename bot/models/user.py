from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UserSettings:
    user_id: int
    language: str = "ru"
