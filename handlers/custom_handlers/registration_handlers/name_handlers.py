# handlers/registration/name_handlers.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import RegistartionStates
from utils.validators import validate_name, validate_last_name
from .router import reg_router


@reg_router.callback_query(F.data == "yes_button", RegistartionStates.name_state)
async def reg_name_get_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Подтверждает использование имени из Telegram."""
    user_data: list = callback.from_user.full_name.split()
    name: str = user_data[0]
    last_name: str = user_data[1]

    await state.update_data(name=name, last_name=last_name)
    await state.set_state(RegistartionStates.email_state)

    await callback.message.answer(
        text=f"<b>ЭТАП - 2: EM@IL</b>\n\nВведите email:",
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@reg_router.callback_query(F.data == "no_button", RegistartionStates.name_state)
async def reg_name_input_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Запрашивает ручной ввод имени."""
    await state.set_state(RegistartionStates.name_input_state)
    await callback.message.answer("Введите ваше имя:")
    await callback.answer()


@reg_router.message(RegistartionStates.name_input_state)
async def reg_name_validation_handler(message: Message, state: FSMContext) -> None:
    """Валидирует и сохраняет имя."""
    name_validation: dict = validate_name(message.text)

    if name_validation["is_valid"]:
        await state.update_data(name=name_validation["name"])
        await state.set_state(RegistartionStates.lastname_input_state)
        await message.answer("✅ Имя сохранено!\nТеперь введите фамилию:")
    else:
        await message.answer(f"❌ {name_validation['message']}\n\nПожалуйста, введите имя еще раз:")


@reg_router.message(RegistartionStates.lastname_input_state)
async def reg_lastname_input_handler(message: Message, state: FSMContext) -> None:
    """Валидирует и сохраняет фамилию."""
    lastname_validation: dict = validate_last_name(message.text)

    if lastname_validation["is_valid"]:
        await state.update_data(last_name=lastname_validation["last_name"])
        await state.set_state(RegistartionStates.email_state)

        await message.answer(
            text=f"<b>ЭТАП - 2: EM@IL</b>\n\n"
                 f"✅ Фамилия сохранена!\n"
                 f"Теперь введите email:",
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer(f"❌ {lastname_validation['message']}\n\nПожалуйста, введите фамилию еще раз:")
