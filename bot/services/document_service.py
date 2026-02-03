from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

from bot.engines.docx_engine import docx_to_pdf
from bot.engines.image_engine import image_to_passport, images_to_pdf
from bot.engines.pdf_engine import merge_pdfs, pdf_to_docx
from bot.engines.text_engine import build_text_document
from bot.models.documents import TextAlignment, TextStyle


@dataclass
class GeneratedFile:
    content: bytes
    filename: str
    mime_type: str


class DocumentService:
    def text_to_document(
        self,
        title: str,
        body: str,
        alignment: TextAlignment,
        style: TextStyle,
        font_size: int,
        output_format: str,
    ) -> GeneratedFile:
        content, mime_type = build_text_document(title, body, alignment, style, font_size, output_format)
        filename = f"document.{output_format}"
        return GeneratedFile(content=content, filename=filename, mime_type=mime_type)

    def images_to_pdf(self, images: Iterable[bytes], title: Optional[str]) -> GeneratedFile:
        content = images_to_pdf(images, title=title)
        return GeneratedFile(content=content, filename="images.pdf", mime_type="application/pdf")

    def image_to_passport(self, image: bytes, as_pdf: bool) -> GeneratedFile:
        content = image_to_passport(image, as_pdf=as_pdf)
        extension = "pdf" if as_pdf else "jpg"
        mime_type = "application/pdf" if as_pdf else "image/jpeg"
        return GeneratedFile(content=content, filename=f"passport.{extension}", mime_type=mime_type)

    def merge_pdfs(self, pdf_files: Iterable[bytes]) -> GeneratedFile:
        content = merge_pdfs(pdf_files)
        return GeneratedFile(content=content, filename="merged.pdf", mime_type="application/pdf")

    def docx_to_pdf(self, docx_bytes: bytes, title: Optional[str]) -> GeneratedFile:
        content = docx_to_pdf(docx_bytes, title=title)
        return GeneratedFile(content=content, filename="document.pdf", mime_type="application/pdf")

    def pdf_to_docx(self, pdf_bytes: bytes) -> GeneratedFile:
        content = pdf_to_docx(pdf_bytes)
        return GeneratedFile(
            content=content,
            filename="document.docx",
            mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
