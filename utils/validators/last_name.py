import re

def validate_last_name(last_name: str) -> dict:
    """
    Проверяет валидность фамилии
    Возвращает dict с результатом проверки
    """
    last_name = last_name.strip()

    result = {
        'is_valid': False,
        'message': '',
        'last_name': last_name
    }

    # Проверка на пустоту
    if not last_name:
        result['message'] = 'Фамилия не может быть пустой'
        return result

    # Проверка длины
    if len(last_name) < 2:
        result['message'] = 'Фамилия слишком короткая (минимум 2 символа)'
        return result

    if len(last_name) > 50:
        result['message'] = 'Фамилия слишком длинная (максимум 50 символов)'
        return result

    # Проверка на допустимые символы (только буквы, дефисы, пробелы)
    if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\- ]+$', last_name):
        result['message'] = 'Фамилия может содержать только буквы, дефисы и пробелы'
        return result

    # Проверка на несколько пробелов подряд
    if '  ' in last_name:
        result['message'] = 'Фамилия не может содержать несколько пробелов подряд'
        return result

    # Проверка на начало/конец с дефиса или пробела
    if last_name.startswith(('-', ' ')) or last_name.endswith(('-', ' ')):
        result['message'] = 'Фамилия не может начинаться или заканчиваться пробелом или дефисом'
        return result

    result['is_valid'] = True
    result['message'] = 'Фамилия валидна'
    return result