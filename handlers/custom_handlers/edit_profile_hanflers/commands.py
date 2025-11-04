from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import EditProfileStates
from keyboards import edit_profile_keyboard
from .router import edit_router

@edit_router.message(Command("edit_profile"))
async def edit_profile_start(message: Message, state: FSMContext) -> None:
    """Обработчик команды редактирования профиля."""
    await state.set_state(EditProfileStates.choose_field)
    await message.answer(
        "📋 <b>Выберите поле для редактирования:</b>",
        reply_markup=edit_profile_keyboard,
        parse_mode="HTML"
    )

@edit_router.message(Command("make_request"))
async def make_request_command(message: Message, state: FSMContext) -> None:
    """Обработчик команды создания запроса."""
    await state.set_state(EditProfileStates.editing_request)
    await message.answer(
        f"<b>🎯 ЗАПРОС</b>\n\n"
        f"Запрос в психологии — это то, с чем вы приходите к психологу, "
        f"основная тема или проблема, которую вы хотите обсудить.\n\n"
        f"✏️ Введите новый запрос:",
        parse_mode=ParseMode.HTML
    )
