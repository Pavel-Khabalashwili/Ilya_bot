from sqlalchemy import create_engine, Boolean, Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.orm import relationship, sessionmaker

Base: DeclarativeBase = declarative_base()
engine = create_engine('sqlite:///psychology_bot.db')

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
        """Возвращает строковое представление объекта."""

        return (f"<User("
                f"id={self.id}, "
                f"name='{self.name}', "
                f"last_name={self.last_name}, "
                f"telegram_id={self.telegram_id})>")


class PsychologicalRequest(Base):
    """Класс описывающий запросы пользователя"""

    __tablename__ = "psychological_requests"

    id = Column(Integer, primary_key=True)
    request_text = Column(String(2000), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user_requests")

    #TODO repr str