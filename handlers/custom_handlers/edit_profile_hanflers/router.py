"""Основной роутер и общие функции"""
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import EditProfileStates
from database.crud import update_user_field
from keyboards import edit_profile_keyboard

edit_router = Router()

async def return_to_edit_menu(message: Message, state: FSMContext, success_message: str = None) -> None:
    """Возвращает пользователя в меню редактирования профиля и обновляет БД."""
    user_data = await state.get_data()
    current_state = await state.get_state()

    field_mapping = {
        'EditProfileStates:editing_name': 'name',
        'EditProfileStates:editing_last_name': 'last_name',
        'EditProfileStates:editing_email': 'email',
        'EditProfileStates:editing_phone': 'phone',
        'EditProfileStates:editing_request': 'user_request'
    }

    changed_field = field_mapping.get(current_state)

    if changed_field and changed_field in user_data:
        new_value = user_data[changed_field]
        update_user_field(
            telegram_id=message.from_user.id,
            field_name=changed_field,
            new_value=new_value
        )

    if success_message:
        await message.answer(success_message, parse_mode="HTML")

    await state.set_state(EditProfileStates.choose_field)
    await message.answer(
        "📋 <b>Выберите поле для редактирования:</b>",
        reply_markup=edit_profile_keyboard,
        parse_mode=ParseMode.HTML
    )
