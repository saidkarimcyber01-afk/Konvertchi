from __future__ import annotations

from io import BytesIO
from typing import Iterable

from docx import Document
from pypdf import PdfReader, PdfWriter


def merge_pdfs(pdf_files: Iterable[bytes]) -> bytes:
    writer = PdfWriter()
    for pdf_bytes in pdf_files:
        reader = PdfReader(BytesIO(pdf_bytes))
        for page in reader.pages:
            writer.add_page(page)
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def pdf_to_docx(pdf_bytes: bytes) -> bytes:
    reader = PdfReader(BytesIO(pdf_bytes))
    document = Document()

    for page in reader.pages:
        text = page.extract_text() or ""
        for line in text.splitlines():
            document.add_paragraph(line)
        document.add_page_break()

    output = BytesIO()
    document.save(output)
    return output.getvalue()
