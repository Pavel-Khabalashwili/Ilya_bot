from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import EditProfileStates
from utils.validators import validate_email, validate_phone
from keyboards import telephone_keyboard
from .router import edit_router, return_to_edit_menu

@edit_router.callback_query(EditProfileStates.choose_field, F.data == "edit_email")
async def edit_email_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Начинает редактирование email."""
    await state.set_state(EditProfileStates.editing_email)
    await callback.message.answer("✏️ Введите новый email:")
    await callback.answer()

@edit_router.message(EditProfileStates.editing_email)
async def edit_email_process(message: Message, state: FSMContext) -> None:
    """Обрабатывает ввод нового email."""
    validation: dict = validate_email(message.text)
    if validation["is_valid"]:
        await state.update_data(email=validation['email'])
        await return_to_edit_menu(
            message,
            state,
            f"✅ Email изменен на: <b>{validation['email']}</b>"
        )
    else:
        await message.answer(f"❌ {validation['message']}\n\n✏️ Пожалуйста, введите email еще раз:\n"
                             f"Пример: example@mail.ru")

@edit_router.callback_query(EditProfileStates.choose_field, F.data == "edit_phone")
async def edit_phone_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Начинает редактирование телефона."""
    await state.set_state(EditProfileStates.editing_phone)
    await callback.message.answer(
        "📱 Выберите способ ввода номера телефона:",
        reply_markup=telephone_keyboard
    )
    await callback.answer()

@edit_router.message(EditProfileStates.editing_phone, F.contact)
async def edit_phone_from_contact(message: Message, state: FSMContext) -> None:
    """Обрабатывает номер телефона из контакта."""
    phone_number: str = message.contact.phone_number
    validation: dict = validate_phone(phone_number)

    if validation["is_valid"]:
        await state.update_data(phone=validation['phone'])
        await return_to_edit_menu(
            message,
            state,
            f"✅ Телефон изменен на: <b>{validation['phone']}</b>"
        )
    else:
        await message.answer(
            f"❌ {validation['message']}\n\n"
            "📱 Пожалуйста, попробуйте еще раз:",
            reply_markup=telephone_keyboard
        )

@edit_router.message(EditProfileStates.editing_phone)
async def edit_phone_process(message: Message, state: FSMContext) -> None:
    """Обрабатывает номер телефона из ручного ввода."""
    if message.text.startswith('/'):
        return

    phone_number: str = message.text
    validation: dict = validate_phone(phone_number)

    if validation["is_valid"]:
        await state.update_data(phone=validation['phone'])
        await return_to_edit_menu(
            message,
            state,
            f"✅ Телефон изменен на: <b>{validation['phone']}</b>"
        )
    else:
        await message.answer(
            f"❌ {validation['message']}\n\n"
            "📱 Пожалуйста, введите номер телефона еще раз:",
            reply_markup=telephone_keyboard
        )
