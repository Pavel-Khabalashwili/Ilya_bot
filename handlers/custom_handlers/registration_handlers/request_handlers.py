# handlers/registration/request_handlers.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from states import RegistartionStates
from utils.validators import validate_request_comprehensive
from .router import reg_router
from .completion_handlers import complete_user_request


@reg_router.callback_query(RegistartionStates.define_request, F.data == "no_button")
async def user_request_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Завершает регистрацию без запроса."""
    await complete_user_request(callback.message, state)
    await callback.answer()


@reg_router.callback_query(RegistartionStates.define_request, F.data == "yes_button")
async def user_request_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Запрашивает ввод психологического запроса."""
    task: str = f"<b>🎯ЗАПРОС</b>\n\nВведите запрос:"

    await state.set_state(RegistartionStates.input_request)
    await callback.message.answer(task, parse_mode=ParseMode.HTML)
    await callback.answer()


@reg_router.message(RegistartionStates.input_request)
async def process_user_request(message: Message, state: FSMContext) -> None:
    """Валидирует и сохраняет психологический запрос."""
    user_input: str = message.text
    request_validation: dict = validate_request_comprehensive(user_input)

    if request_validation["is_valid"]:
        await complete_user_request(message, state, request_validation["request"])
    else:
        await message.answer(
            text=f"❌ {request_validation['message']}\n\n"
                 f"<b>Пожалуйста, опишите запрос еще раз:</b>\n"
                 f"<i>Пример: 'Хотел бы обсудить проблемы с тревожностью и стрессом на работе'</i>",
            parse_mode=ParseMode.HTML
        )
