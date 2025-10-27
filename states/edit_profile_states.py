from aiogram.fsm.state import State, StatesGroup


class EditProfileStates(StatesGroup):
    choose_field = State()      # Выбор поля для редактирования
    editing_name = State()      # Редактирование имени
    editing_last_name = State() # Редактирование фамилии
    editing_email = State()     # Редактирование email
    editing_phone = State()     # Редактирование телефона
    editing_request = State()   # Редактирование запроса
