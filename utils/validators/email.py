import re


def validate_email(email: str) -> dict:
    """
    Расширенная проверка email
    Возвращает словарь с результатом проверки
    """
    email = email.strip().lower()

    # Базовый паттерн
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    result = {
        'is_valid': False,
        'message': '',
        'email': email
    }

    # Проверка на пустоту
    if not email:
        result['message'] = 'Email не может быть пустым'
        return result

    # Проверка длины
    if len(email) > 254:
        result['message'] = 'Email слишком длинный'
        return result

    # Проверка формата
    if not re.match(pattern, email):
        result['message'] = 'Неверный формат email'
        return result

    # Разделение на локальную часть и домен
    local_part, domain = email.split('@')

    # Проверка длины локальной части
    if len(local_part) > 64:
        result['message'] = 'Локальная часть email слишком длинная'
        return result

    # Проверка на запрещенные символы
    if re.search(r'[^\w._%+-]', local_part):
        result['message'] = 'Email содержит запрещенные символы'
        return result

    # Проверка на точки в начале/конце
    if local_part.startswith('.') or local_part.endswith('.'):
        result['message'] = 'Email не может начинаться или заканчиваться точкой'
        return result

    # Проверка на двойные точки
    if '..' in local_part:
        result['message'] = 'Email не может содержать две точки подряд'
        return result

    result['is_valid'] = True
    result['message'] = 'Email валидный'
    return result
