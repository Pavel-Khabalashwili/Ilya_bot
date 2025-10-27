from aiogram.fsm.state import State, StatesGroup


class UserRequest(StatesGroup):
    """Состояния для реализации запроса от пользователя"""
    define_request = State()
    input_request = State()
