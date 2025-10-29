from sqlalchemy.orm import Session
from database.engine import engine
from database.models import Base, User, PsychologicalRequest
from database.manager import DatabaseManager


def create_tables():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)


def create_user(data: dict) -> User:
    """
    Функция создания пользователя
    :param data: Словарь с данными пользователя
    :return: Созданный пользователь или None
    """
    telegram_id = data["telegram_id"]
    profile_link = data["username_link"]
    name = data.get("name", "Не указано")
    last_name = data.get("last_name")
    email = data.get("email")
    phone = data.get("phone")
    user_request = data.get("user_request")

    with DatabaseManager() as session:
        # Проверяем, нет ли уже пользователя
        existing_user = session.query(User).filter(
            User.telegram_id == telegram_id
        ).first()

        if existing_user:
            print(f" Пользователь с ID {telegram_id} уже существует")
            return None

        # СОЗДАЕМ ПОЛЬЗОВАТЕЛЯ
        user = User(
            telegram_id=telegram_id,
            profile_link=profile_link,
            name=name,
            last_name=last_name,
            phone=phone,
            email=email,
        )
        session.add(user)
        session.flush()  #  получаем user.id

        # ЕСЛИ ЕСТЬ ЗАПРОС - СОЗДАЕМ ЕГО
        if user_request:
            request = PsychologicalRequest(
                request_text=user_request,
                user_id=user.id
            )
            session.add(request)

        print(f"✅ Создан пользователь: {user}")
        if user_request:
            print(f"✅ Создан запрос: {request}")


def show_all_data() -> None:

    with DatabaseManager() as session:
        users = session.query(User).all()

        print("\n" + "=" * 60)
        print("📊 ВСЕ ДАННЫЕ ИЗ БАЗЫ ДАННЫХ")
        print("=" * 60)

        if not users:
            print("❌ В базе данных нет пользователей")
            return

        print(f"👥 Всего пользователей: {len(users)}")

        for user in users:
            print(f"\n👤 ПОЛЬЗОВАТЕЛЬ:")
            print(f"   ID: {user.id}")
            print(f"   Telegram ID: {user.telegram_id}")
            print(f"   Имя: {user.name}")
            print(f"   Фамилия: {user.last_name or 'Не указана'}")
            print(f"   Телефон: {user.phone or 'Не указан'}")
            print(f"   Email: {user.email or 'Не указан'}")
            print(f"   Профиль: {user.profile_link}")
            print(f"   Дата регистрации: {user.created_at}")

            # Выводим запросы пользователя
            if user.user_requests:
                print(f"   📝 Запросов: {len(user.user_requests)}")
                for i, request in enumerate(user.user_requests, 1):
                    status = "🟢 Активный" if request.status else "🔴 Завершен"
                    print(f"      {i}. Запрос #{request.id} ({status}):")
                    print(f"         Текст: {request.request_text}")
                    print(f"         Создан: {request.created_at}")
            else:
                print(f"   📝 Запросов: 0")

            print("-" * 50)

if __name__ == '__main__':
    # create_tables()
    # test_data = {
    #     "telegram_id": 123456789,
    #     "username_link": "https://t.me/test_user",
    #     "name": "Тестовый",
    #     "last_name": "Пользователь",
    #     "phone": "+79991234567",
    #     "email": "test@mail.ru",
    #     "user_request": "Тестовый психологический запрос"
    # }
    #
    # create_user(data=test_data)

    show_all_data()

