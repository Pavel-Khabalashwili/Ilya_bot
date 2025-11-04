from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from keyboards import yes_no_keyboard
from states import RegistartionStates
from .router import reg_router


@reg_router.message(F.text == "РЕГИСТРАЦИЯ")
async def reg_name_handler(message: Message, state: FSMContext) -> None:
    """Начинает процесс регистрации."""
    await state.set_state(RegistartionStates.name_state)

    user = message.from_user
    telegram_id: int = user.id
    username_link: str = f"https://t.me/{user.username}" if user.username else "неопределенно"

    await state.update_data(telegram_id=telegram_id, username_link=username_link)

    question: str = (f"<b>ЭТАП - 1: ПОДТВЕРЖДЕНИЕ ИМЕНИ</b>\n\n"
                     f"Использовать текущее ФИО: <i>{message.from_user.full_name}</i> ?")

    await message.answer(text=question, parse_mode=ParseMode.HTML, reply_markup=yes_no_keyboard)
