from __future__ import annotations

from io import BytesIO
from typing import Iterable, Optional, Tuple

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


A4_WIDTH, A4_HEIGHT = A4
PASSPORT_SIZE = (354, 472)


def _fit_image_to_a4(image: Image.Image) -> Tuple[int, int]:
    max_width = A4_WIDTH - 80
    max_height = A4_HEIGHT - 120
    ratio = min(max_width / image.width, max_height / image.height)
    return int(image.width * ratio), int(image.height * ratio)


def images_to_pdf(images: Iterable[bytes], title: Optional[str] = None) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    for image_bytes in images:
        image = Image.open(BytesIO(image_bytes))
        image = image.convert("RGB")
        new_width, new_height = _fit_image_to_a4(image)
        resized = image.resize((new_width, new_height), Image.LANCZOS)

        y_position = (A4_HEIGHT - new_height) / 2
        if title:
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawCentredString(A4_WIDTH / 2, A4_HEIGHT - 40, title)
            y_position = (A4_HEIGHT - new_height) / 2 - 10

        pdf.drawImage(ImageReader(resized), (A4_WIDTH - new_width) / 2, y_position, new_width, new_height)
        pdf.showPage()

    pdf.save()
    return buffer.getvalue()


def image_to_passport(image_bytes: bytes, as_pdf: bool = False) -> bytes:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    target_ratio = 3 / 4
    current_ratio = width / height

    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        box = (left, 0, left + new_width, height)
    else:
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        box = (0, top, width, top + new_height)

    cropped = image.crop(box)
    resized = cropped.resize(PASSPORT_SIZE, Image.LANCZOS)

    if not as_pdf:
        buffer = BytesIO()
        resized.save(buffer, format="JPEG", quality=95)
        return buffer.getvalue()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.drawImage(ImageReader(resized), (A4_WIDTH - PASSPORT_SIZE[0]) / 2, (A4_HEIGHT - PASSPORT_SIZE[1]) / 2)
    pdf.showPage()
    pdf.save()
    return buffer.getvalue()
