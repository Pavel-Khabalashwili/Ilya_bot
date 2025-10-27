from sqlalchemy.orm import Session
from .models import Base, User, PsychologicalRequest
from .engine import engine

def create_tables():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)
    