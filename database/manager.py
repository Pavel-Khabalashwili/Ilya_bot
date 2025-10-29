from sqlalchemy.orm import Session

from .engine import engine


class DatabaseManager:
    """Класс для работы с базой данных. Реализующий открытие и закрытие."""

    def __enter__(self):
        self.session = Session(bind=engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

        if exc_type:
            return True

