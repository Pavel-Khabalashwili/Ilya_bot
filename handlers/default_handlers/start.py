from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import registration_keyboard

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):

    await message.answer(f"Привет, {message.from_user.full_name}\n"
                         f"[CООБЩЕНИЕ ОТ ИЛЬИ]!\n"
                         f"Чтобы упростить процесс записи необходимо пройти регистрацию.\n"
                         f"Как будете готовы нажмите на кнопку регистраиция!", reply_markup=registration_keyboard)
