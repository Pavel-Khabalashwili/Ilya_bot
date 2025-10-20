from aiogram.fsm.state import State, StatesGroup


class RegistartionStates(StatesGroup):

    name_state = State()
    lastname_state = State()
    tel_number_state = State()
    email_state = State()
    user_request_state = State