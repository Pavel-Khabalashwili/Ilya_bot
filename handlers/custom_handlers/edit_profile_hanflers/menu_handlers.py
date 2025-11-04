from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import EditProfileStates
from database.crud import get_user
from .router import edit_router

@edit_router.callback_query(EditProfileStates.choose_field, F.data == "show_data")
async def show_all_data(callback: CallbackQuery, state: FSMContext) -> None:
    """Показывает все данные пользователя."""
    user_data: dict = get_user(telegram_id=callback.from_user.id)

    data_message: str = (
        f"<b>📊 ВАШИ ДАННЫЕ:</b>\n\n"
        f"👤 <b>Имя:</b> {user_data.get('name', 'Не указано')}\n"
        f"👥 <b>Фамилия:</b> {user_data.get('last_name', 'Не указана')}\n"
        f"📧 <b>Email:</b> {user_data.get('email', 'Не указан')}\n"
        f"📱 <b>Телефон:</b> {user_data.get('phone', 'Не указан')}\n"
        f"🎯 <b>Запрос:</b> {user_data.get('user_request', 'Не указан')}\n\n"
    )

    await callback.message.answer(data_message, parse_mode=ParseMode.HTML)
    await callback.answer()

@edit_router.callback_query(EditProfileStates.choose_field, F.data == "cancel_edit")
async def cancel_edit(callback: CallbackQuery, state: FSMContext) -> None:
    """Отменяет редактирование профиля."""
    await callback.message.answer("❌ Редактирование отменено.")
    await state.clear()
    await callback.answer()
