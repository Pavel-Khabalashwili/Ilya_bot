from sqlalchemy.orm import Session
from .models import Base, User, PsychologicalRequest
from .engine import engine

def create_tables():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)

def create_user(data: dict) -> None:
    """
    Функция создания пользователя
    :param data: Словарь с данными пользователя
    :return: None
    """

    name = data.get("name", "Имя не установлено")
    last_name = data.get("last_name", "Фамилия не установлена")
    email = data.get("email", "Email не установлен")
    phone = data.get("phone", "Телефон не установлен")
    user_requst = data.get("user_requst")

    