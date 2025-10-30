from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship

from .engine import Base


class User(Base):
    """Класс описывающий пользователя"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    profile_link = Column(String(100))
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    user_request = Column(String, nullable=True)

    def __repr__(self):
        """Строковое представление для разработчиков"""
        return (f"<User("
                f"id={self.id}, "
                f"name='{self.name}', "
                f"last_name='{self.last_name}', "  # Добавил кавычки
                f"telegram_id={self.telegram_id})>")

    def __str__(self):
        """Строковое представление для пользователей"""
        if self.last_name:
            return f"👤 {self.name} {self.last_name} (ID: {self.telegram_id})"
        else:
            return f"👤 {self.name} (ID: {self.telegram_id})"
