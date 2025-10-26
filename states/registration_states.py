from aiogram.fsm.state import State, StatesGroup


class RegistartionStates(StatesGroup):
    """
    Состояния для регистрации пользователя
    """

    name_state = State()
    name_input_state = State()
    lastname_state = State()
    lastname_input_state = State()
    tel_number_state = State()
    email_state = State()

class UserRequest(StatesGroup):
    """Состояния для реализации запроса от пользователя"""
    define_request = State()
    input_request = State()
