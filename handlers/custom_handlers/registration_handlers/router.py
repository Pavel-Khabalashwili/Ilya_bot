"""Основной роутер и общие функции"""
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import RegistartionStates
from keyboards import yes_no_keyboard


reg_router = Router()


async def ask_user_request(message: Message, state: FSMContext) -> None:
    """Запрашивает психологический запрос у пользователя."""
    await state.set_state(RegistartionStates.define_request)

    await message.answer(
        text=f"<b>🎯 ОПРЕДЕЛЕНИЕ ЗАПРОСА</b>\n\n"
             f"Чтобы наша встреча была максимально полезной для вас, я предлагаю заранее обозначить тему разговора.\n\n"
             f"<b>Что вас беспокоит или что хотели бы обсудить?</b>\n"
             f"Это может быть конкретная ситуация, вопрос или просто то, что сейчас на душе.\n\n"
             f"<b>Желаете описать запрос сейчас?</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=yes_no_keyboard
    )
