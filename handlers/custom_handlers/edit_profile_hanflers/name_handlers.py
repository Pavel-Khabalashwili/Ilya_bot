from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import EditProfileStates
from utils.validators import validate_name, validate_last_name
from .router import edit_router, return_to_edit_menu

@edit_router.callback_query(EditProfileStates.choose_field, F.data == "edit_name")
async def edit_name_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Начинает редактирование имени."""
    await state.set_state(EditProfileStates.editing_name)
    await callback.message.answer("✏️ Введите новое имя:")
    await callback.answer()

@edit_router.message(EditProfileStates.editing_name)
async def edit_name_process(message: Message, state: FSMContext) -> None:
    """Обрабатывает ввод нового имени."""
    validation: dict = validate_name(message.text)
    if validation["is_valid"]:
        await state.update_data(name=validation['name'])
        await return_to_edit_menu(
            message,
            state,
            f"✅ Имя изменено на: <b>{validation['name']}</b>"
        )
    else:
        await message.answer(f"❌ {validation['message']}\n\n✏️ Пожалуйста, введите имя еще раз:")

@edit_router.callback_query(EditProfileStates.choose_field, F.data == "edit_last_name")
async def edit_last_name_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Начинает редактирование фамилии."""
    await state.set_state(EditProfileStates.editing_last_name)
    await callback.message.answer("✏️ Введите новую фамилию:")
    await callback.answer()

@edit_router.message(EditProfileStates.editing_last_name)
async def edit_last_name_process(message: Message, state: FSMContext) -> None:
    """Обрабатывает ввод новой фамилии."""
    validation: dict = validate_last_name(message.text)
    if validation["is_valid"]:
        await state.update_data(last_name=validation['last_name'])
        await return_to_edit_menu(
            message,
            state,
            f"✅ Фамилия изменена на: <b>{validation['last_name']}</b>"
        )
    else:
        await message.answer(f"❌ {validation['message']}\n\n✏️ Пожалуйста, введите фамилию еще раз:")
