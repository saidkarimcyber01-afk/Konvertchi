from __future__ import annotations

from io import BytesIO
from typing import Optional

from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def docx_to_pdf(docx_bytes: bytes, title: Optional[str] = None) -> bytes:
    document = Document(BytesIO(docx_bytes))
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)

    elements = []
    if title:
        elements.append(Paragraph(f"<b>{title}</b>", ParagraphStyle(name="Title", fontSize=16)))
        elements.append(Spacer(1, 12))

    body_style = ParagraphStyle(name="Body", fontSize=12, leading=16)
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            elements.append(Spacer(1, 8))
            continue
        elements.append(Paragraph(text.replace("\n", "<br />"), body_style))
        elements.append(Spacer(1, 6))

    pdf.build(elements)
    return buffer.getvalue()
