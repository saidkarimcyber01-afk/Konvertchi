from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.core.storage import UserSettingsStore
from bot.i18n import t
from bot.utils.keyboards import language_keyboard, menu_keyboard

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext, settings: UserSettingsStore) -> None:
    await state.clear()
    await message.answer(t("ru", "start"), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery, state: FSMContext, settings: UserSettingsStore) -> None:
    language = callback.data.split(":", 1)[1]
    settings.set_language(callback.from_user.id, language)
    await state.clear()
    await callback.message.answer(t(language, "language_set", language=t(language, "language_name")))
    await callback.message.answer(t(language, "menu_title"), reply_markup=menu_keyboard(language))
    await callback.answer()
