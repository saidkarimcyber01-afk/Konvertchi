from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TextAlignment(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


class TextStyle(str, Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    BOLD_ITALIC = "bold_italic"


@dataclass
class TextDocumentOptions:
    title: str
    alignment: TextAlignment
    style: TextStyle
    font_size: int
    body: str
    output_format: str
    output_title: Optional[str] = None
