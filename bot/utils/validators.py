from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FileValidationRules:
    max_size_mb: int
    allowed_mime_types: Iterable[str]


def is_size_valid(file_size: int, max_size_mb: int) -> bool:
    return file_size <= max_size_mb * 1024 * 1024


def is_mime_valid(mime_type: str | None, allowed_mime_types: Iterable[str]) -> bool:
    if not mime_type:
        return False
    return mime_type in allowed_mime_types
