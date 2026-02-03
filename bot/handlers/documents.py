from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.core.config import AppConfig
from bot.core.storage import UserSettingsStore
from bot.i18n import t
from bot.models.documents import TextAlignment, TextStyle
from bot.services.document_service import DocumentService
from bot.utils.keyboards import alignment_keyboard, done_keyboard, menu_keyboard, size_keyboard, style_keyboard
from bot.utils.telegram import download_document, download_photo, extract_photo
from bot.utils.validators import is_mime_valid, is_size_valid

router = Router()


class TextStates(StatesGroup):
    waiting_title = State()
    waiting_alignment = State()
    waiting_style = State()
    waiting_font_size = State()
    waiting_body = State()


class ImagePdfStates(StatesGroup):
    waiting_title = State()
    collecting_images = State()


class ImagePassportStates(StatesGroup):
    waiting_image = State()


class PdfMergeStates(StatesGroup):
    collecting_pdfs = State()


class DocxToPdfStates(StatesGroup):
    waiting_docx = State()


class PdfToDocxStates(StatesGroup):
    waiting_pdf = State()


@router.callback_query(F.data.startswith("action:"))
async def menu_actions(
    callback: CallbackQuery,
    state: FSMContext,
    settings: UserSettingsStore,
) -> None:
    action = callback.data.split(":", 1)[1]
    language = settings.get(callback.from_user.id).language

    if action in {"text_docx", "text_pdf"}:
        await state.set_state(TextStates.waiting_title)
        await state.update_data(output_format="docx" if action == "text_docx" else "pdf")
        await callback.message.answer(t(language, "ask_title"))
    elif action == "image_pdf":
        await state.set_state(ImagePdfStates.waiting_title)
        await callback.message.answer(t(language, "ask_title"))
    elif action == "image_passport":
        await state.set_state(ImagePassportStates.waiting_image)
        await callback.message.answer(t(language, "ask_passport_image"))
    elif action == "pdf_merge":
        await state.set_state(PdfMergeStates.collecting_pdfs)
        await state.update_data(pdfs=[])
        await callback.message.answer(t(language, "ask_pdf_files"), reply_markup=done_keyboard(language))
    elif action == "docx_pdf":
        await state.set_state(DocxToPdfStates.waiting_docx)
        await callback.message.answer(t(language, "ask_docx_file"))
    elif action == "pdf_docx":
        await state.set_state(PdfToDocxStates.waiting_pdf)
        await callback.message.answer(t(language, "ask_pdf_file"))

    await callback.answer()


@router.message(TextStates.waiting_title)
async def text_title(message: Message, state: FSMContext, settings: UserSettingsStore) -> None:
    await state.update_data(title=message.text.strip())
    language = settings.get(message.from_user.id).language
    await state.set_state(TextStates.waiting_alignment)
    await message.answer(t(language, "ask_alignment"), reply_markup=alignment_keyboard(language))


@router.callback_query(TextStates.waiting_alignment, F.data.startswith("align:"))
async def text_alignment(callback: CallbackQuery, state: FSMContext, settings: UserSettingsStore) -> None:
    alignment = callback.data.split(":", 1)[1]
    await state.update_data(alignment=alignment)
    language = settings.get(callback.from_user.id).language
    await state.set_state(TextStates.waiting_style)
    await callback.message.answer(t(language, "ask_style"), reply_markup=style_keyboard(language))
    await callback.answer()


@router.callback_query(TextStates.waiting_style, F.data.startswith("style:"))
async def text_style(callback: CallbackQuery, state: FSMContext, settings: UserSettingsStore) -> None:
    style = callback.data.split(":", 1)[1]
    await state.update_data(style=style)
    language = settings.get(callback.from_user.id).language
    await state.set_state(TextStates.waiting_font_size)
    await callback.message.answer(t(language, "ask_font_size"), reply_markup=size_keyboard(language))
    await callback.answer()


@router.callback_query(TextStates.waiting_font_size, F.data.startswith("size:"))
async def text_font_size(callback: CallbackQuery, state: FSMContext, settings: UserSettingsStore) -> None:
    size = int(callback.data.split(":", 1)[1])
    await state.update_data(font_size=size)
    language = settings.get(callback.from_user.id).language
    await state.set_state(TextStates.waiting_body)
    await callback.message.answer(t(language, "ask_text"))
    await callback.answer()


@router.message(TextStates.waiting_body)
async def text_body(
    message: Message,
    state: FSMContext,
    settings: UserSettingsStore,
    config: AppConfig,
    service: DocumentService,
) -> None:
    language = settings.get(message.from_user.id).language
    text = message.text

    if message.document:
        if not is_mime_valid(message.document.mime_type, {"text/plain"}) or not is_size_valid(
            message.document.file_size or 0,
            config.bot.max_file_size_mb,
        ):
            await message.answer(t(language, "invalid_file"))
            return
        text_bytes = await download_document(message.bot, message.document)
        text = text_bytes.decode("utf-8", errors="ignore")

    if not text:
        await message.answer(t(language, "error"))
        return

    data = await state.get_data()
    document = service.text_to_document(
        title=data["title"],
        body=text,
        alignment=TextAlignment(data["alignment"]),
        style=TextStyle(data["style"]),
        font_size=data["font_size"],
        output_format=data["output_format"],
    )
    await state.clear()
    await message.answer_document((document.filename, document.content), caption=t(language, "success"))
    await message.answer(t(language, "menu_title"), reply_markup=menu_keyboard(language))


@router.message(ImagePdfStates.waiting_title)
async def image_pdf_title(message: Message, state: FSMContext, settings: UserSettingsStore) -> None:
    title = message.text.strip()
    if title.lower() in {"/skip", "-"}:
        title = None
    await state.update_data(title=title)
    language = settings.get(message.from_user.id).language
    await state.set_state(ImagePdfStates.collecting_images)
    await state.update_data(images=[])
    await message.answer(t(language, "ask_images"), reply_markup=done_keyboard(language))


@router.message(ImagePdfStates.collecting_images)
async def image_pdf_collect(
    message: Message,
    state: FSMContext,
    settings: UserSettingsStore,
    config: AppConfig,
) -> None:
    language = settings.get(message.from_user.id).language
    photo = extract_photo(message.photo)
    if not photo:
        await message.answer(t(language, "invalid_file"))
        return
    if not is_size_valid(photo.file_size or 0, config.bot.max_file_size_mb):
        await message.answer(t(language, "invalid_file"))
        return
    image_bytes = await download_photo(message.bot, photo)
    data = await state.get_data()
    images = data.get("images", [])
    images.append(image_bytes)
    await state.update_data(images=images)


@router.callback_query(ImagePdfStates.collecting_images, F.data == "done")
async def image_pdf_done(
    callback: CallbackQuery,
    state: FSMContext,
    settings: UserSettingsStore,
    service: DocumentService,
) -> None:
    language = settings.get(callback.from_user.id).language
    data = await state.get_data()
    images = data.get("images", [])
    if not images:
        await callback.message.answer(t(language, "no_files"))
        return
    document = service.images_to_pdf(images, title=data.get("title"))
    await state.clear()
    await callback.message.answer_document((document.filename, document.content), caption=t(language, "success"))
    await callback.message.answer(t(language, "menu_title"), reply_markup=menu_keyboard(language))
    await callback.answer()


@router.message(ImagePassportStates.waiting_image)
async def passport_image(
    message: Message,
    state: FSMContext,
    settings: UserSettingsStore,
    config: AppConfig,
    service: DocumentService,
) -> None:
    language = settings.get(message.from_user.id).language
    photo = extract_photo(message.photo)
    if not photo:
        await message.answer(t(language, "invalid_file"))
        return
    if not is_size_valid(photo.file_size or 0, config.bot.max_file_size_mb):
        await message.answer(t(language, "invalid_file"))
        return
    image_bytes = await download_photo(message.bot, photo)
    document = service.image_to_passport(image_bytes, as_pdf=False)
    await state.clear()
    await message.answer_document((document.filename, document.content), caption=t(language, "success"))
    await message.answer(t(language, "menu_title"), reply_markup=menu_keyboard(language))


@router.message(PdfMergeStates.collecting_pdfs)
async def pdf_merge_collect(
    message: Message,
    state: FSMContext,
    settings: UserSettingsStore,
    config: AppConfig,
) -> None:
    language = settings.get(message.from_user.id).language
    if not message.document or not is_mime_valid(message.document.mime_type, {"application/pdf"}):
        await message.answer(t(language, "invalid_file"))
        return
    if not is_size_valid(message.document.file_size or 0, config.bot.max_file_size_mb):
        await message.answer(t(language, "invalid_file"))
        return
    pdf_bytes = await download_document(message.bot, message.document)
    data = await state.get_data()
    pdfs = data.get("pdfs", [])
    pdfs.append(pdf_bytes)
    await state.update_data(pdfs=pdfs)


@router.callback_query(PdfMergeStates.collecting_pdfs, F.data == "done")
async def pdf_merge_done(
    callback: CallbackQuery,
    state: FSMContext,
    settings: UserSettingsStore,
    service: DocumentService,
) -> None:
    language = settings.get(callback.from_user.id).language
    data = await state.get_data()
    pdfs = data.get("pdfs", [])
    if not pdfs:
        await callback.message.answer(t(language, "no_files"))
        return
    document = service.merge_pdfs(pdfs)
    await state.clear()
    await callback.message.answer_document((document.filename, document.content), caption=t(language, "success"))
    await callback.message.answer(t(language, "menu_title"), reply_markup=menu_keyboard(language))
    await callback.answer()


@router.message(DocxToPdfStates.waiting_docx)
async def docx_to_pdf_handler(
    message: Message,
    state: FSMContext,
    settings: UserSettingsStore,
    config: AppConfig,
    service: DocumentService,
) -> None:
    language = settings.get(message.from_user.id).language
    if not message.document or not is_mime_valid(
        message.document.mime_type,
        {"application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
    ):
        await message.answer(t(language, "invalid_file"))
        return
    if not is_size_valid(message.document.file_size or 0, config.bot.max_file_size_mb):
        await message.answer(t(language, "invalid_file"))
        return
    docx_bytes = await download_document(message.bot, message.document)
    document = service.docx_to_pdf(docx_bytes, title=None)
    await state.clear()
    await message.answer_document((document.filename, document.content), caption=t(language, "success"))
    await message.answer(t(language, "menu_title"), reply_markup=menu_keyboard(language))


@router.message(PdfToDocxStates.waiting_pdf)
async def pdf_to_docx_handler(
    message: Message,
    state: FSMContext,
    settings: UserSettingsStore,
    config: AppConfig,
    service: DocumentService,
) -> None:
    language = settings.get(message.from_user.id).language
    if not message.document or not is_mime_valid(message.document.mime_type, {"application/pdf"}):
        await message.answer(t(language, "invalid_file"))
        return
    if not is_size_valid(message.document.file_size or 0, config.bot.max_file_size_mb):
        await message.answer(t(language, "invalid_file"))
        return
    pdf_bytes = await download_document(message.bot, message.document)
    document = service.pdf_to_docx(pdf_bytes)
    await state.clear()
    await message.answer_document((document.filename, document.content), caption=t(language, "success"))
    await message.answer(t(language, "menu_title"), reply_markup=menu_keyboard(language))
