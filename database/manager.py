from sqlalchemy.orm import Session

from .engine import engine


class DatabaseManager:
    """Класс для работы с базой данных. Реализующий открытие и закрытие."""

    def __enter__(self):
        self.session = Session(bind=engine)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type:
            self.session.rollback()  # Откат при ошибке
            print(f"❌ Ошибка: {exc_type.__name__}: {exc_val}")
        else:
            self.session.commit()  # Сохранение при успехе

        self.session.close()
        return False  # НЕ подавляем исключения
