from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import t


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Русский", callback_data="lang:ru")],
            [InlineKeyboardButton(text="O‘zbek", callback_data="lang:uz")],
        ]
    )


def menu_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(language, "menu_text_to_docx"), callback_data="action:text_docx")],
            [InlineKeyboardButton(text=t(language, "menu_text_to_pdf"), callback_data="action:text_pdf")],
            [InlineKeyboardButton(text=t(language, "menu_image_to_pdf"), callback_data="action:image_pdf")],
            [InlineKeyboardButton(text=t(language, "menu_image_to_passport"), callback_data="action:image_passport")],
            [InlineKeyboardButton(text=t(language, "menu_pdf_merge"), callback_data="action:pdf_merge")],
            [InlineKeyboardButton(text=t(language, "menu_docx_to_pdf"), callback_data="action:docx_pdf")],
            [InlineKeyboardButton(text=t(language, "menu_pdf_to_docx"), callback_data="action:pdf_docx")],
        ]
    )


def alignment_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(language, "button_left"), callback_data="align:left")],
            [InlineKeyboardButton(text=t(language, "button_center"), callback_data="align:center")],
            [InlineKeyboardButton(text=t(language, "button_right"), callback_data="align:right")],
            [InlineKeyboardButton(text=t(language, "button_justify"), callback_data="align:justify")],
        ]
    )


def style_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(language, "button_style_normal"), callback_data="style:normal")],
            [InlineKeyboardButton(text=t(language, "button_style_bold"), callback_data="style:bold")],
            [InlineKeyboardButton(text=t(language, "button_style_italic"), callback_data="style:italic")],
            [InlineKeyboardButton(text=t(language, "button_style_bold_italic"), callback_data="style:bold_italic")],
        ]
    )


def size_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(language, "button_size_12"), callback_data="size:12")],
            [InlineKeyboardButton(text=t(language, "button_size_14"), callback_data="size:14")],
            [InlineKeyboardButton(text=t(language, "button_size_16"), callback_data="size:16")],
        ]
    )


def done_keyboard(language: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t(language, "button_done"), callback_data="done")]]
    )
