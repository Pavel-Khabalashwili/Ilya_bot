import re


def validate_name(name: str) -> dict:
    """
    Проверяет валидность имени
    Возвращает dict с результатом проверки
    """
    name = name.strip()

    result = {
        'is_valid': False,
        'message': '',
        'name': name
    }

    # Проверка на пустоту
    if not name:
        result['message'] = 'Имя не может быть пустым'
        return result

    # Проверка длины
    if len(name) < 2:
        result['message'] = 'Имя слишком короткое (минимум 2 символа)'
        return result

    if len(name) > 50:
        result['message'] = 'Имя слишком длинное (максимум 50 символов)'
        return result

    # Проверка на допустимые символы (только буквы, дефисы, пробелы)
    if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\- ]+$', name):
        result['message'] = 'Имя может содержать только буквы, дефисы и пробелы'
        return result

    # Проверка на несколько пробелов подряд
    if '  ' in name:
        result['message'] = 'Имя не может содержать несколько пробелов подряд'
        return result

    # Проверка на начало/конец с дефиса или пробела
    if name.startswith(('-', ' ')) or name.endswith(('-', ' ')):
        result['message'] = 'Имя не может начинаться или заканчиваться пробелом или дефисом'
        return result

    result['is_valid'] = True
    result['message'] = 'Имя валидно'
    return result
