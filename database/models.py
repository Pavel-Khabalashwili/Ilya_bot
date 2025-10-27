from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship

from .engine import Base


class User(Base):
    """Класс описывающий пользователя"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user_requests = relationship("PsychologicalRequest", back_populates="user")

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


class PsychologicalRequest(Base):
    """Класс описывающий запросы пользователя"""

    __tablename__ = "psychological_requests"

    id = Column(Integer, primary_key=True)
    request_text = Column(String(2000), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user_requests")

    def __repr__(self):
        """Строковое представление для разработчиков (отладка)"""
        status_text = "активный" if self.status else "завершен"
        text_preview = self.request_text[:30] + "..." if len(self.request_text) > 30 else self.request_text
        return (f"<PsychologicalRequest("
                f"id={self.id}, "
                f"user_id={self.user_id}, "
                f"status='{status_text}', "
                f"text='{text_preview}')>")

    def __str__(self):
        """Строковое представление для пользователей"""
        status_text = "🟢 активный" if self.status else "🔴 завершен"
        text_preview = self.request_text[:80] + "..." if len(self.request_text) > 80 else self.request_text
        return f"🎯 Запрос #{self.id} ({status_text}): {text_preview}"
