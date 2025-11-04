from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import EditProfileStates
from utils.validators import validate_request_comprehensive
from .router import edit_router, return_to_edit_menu

@edit_router.callback_query(EditProfileStates.choose_field, F.data == "edit_request")
async def edit_request_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Начинает редактирование запроса."""
    await state.set_state(EditProfileStates.editing_request)
    await callback.message.answer(
        f"<b>🎯 ЗАПРОС</b>\n\n"
        f"Запрос в психологии — это то, с чем вы приходите к психологу, "
        f"основная тема или проблема, которую вы хотите обсудить.\n\n"
        f"✏️ Введите новый запрос:",
        parse_mode=ParseMode.HTML
    )
    await callback.answer()

@edit_router.message(EditProfileStates.editing_request)
async def edit_request_process(message: Message, state: FSMContext) -> None:
    """Обрабатывает ввод нового запроса."""
    validation: dict = validate_request_comprehensive(message.text)
    if validation["is_valid"]:
        await state.update_data(user_request=message.text)
        await return_to_edit_menu(
            message,
            state,
            "✅ Запрос обновлен!"
        )
    else:
        await message.answer(f"❌ {validation['message']}\n\n✏️ Пожалуйста, введите запрос еще раз:")
