# utils/validators.py
import re

def validate_request_length(request_text: str) -> dict:
    """
    Проверяет длину запроса пользователя
    """
    request_text = request_text.strip()

    result = {
        'is_valid': False,
        'message': '',
        'request': request_text
    }

    # Проверка на пустоту
    if not request_text:
        result['message'] = 'Запрос не может быть пустым'
        return result

    # Проверка минимальной длины
    if len(request_text) < 10:
        result['message'] = 'Запрос слишком короткий. Пожалуйста, опишите подробнее (минимум 10 символов)'
        return result

    # Проверка максимальной длины
    if len(request_text) > 2000:
        result['message'] = 'Запрос слишком длинный. Пожалуйста, опишите кратко (максимум 2000 символов)'
        return result

    result['is_valid'] = True
    result['message'] = 'Запрос валиден'
    return result

def validate_request_content(request_text: str) -> dict:
    """
    Проверяет содержание запроса на адекватность
    """
    request_text = request_text.strip().lower()

    result = {
        'is_valid': False,
        'message': '',
        'request': request_text
    }

    # Проверка на бессмысленный текст (много повторяющихся символов)
    if re.search(r'(.)\1{10,}', request_text):  # 10+ одинаковых символов подряд
        result['message'] = 'Запрос содержит подозрительные повторения'
        return result

    # Проверка на случайный набор символов
    if re.search(r'[a-z]{15,}', request_text) and not re.search(r'[а-я]', request_text):
        result['message'] = 'Запрос выглядит как случайный набор символов'
        return result

    # Проверка на минимальное количество слов
    words = request_text.split()
    if len(words) < 3:
        result['message'] = 'Пожалуйста, опишите запрос более развернуто (минимум 3 слова)'
        return result

    result['is_valid'] = True
    result['message'] = 'Содержание запроса валидно'
    return result

def validate_request_comprehensive(request_text: str) -> dict:
    """
    Комплексная проверка запроса пользователя
    """
    request_text = request_text.strip()

    result = {
        'is_valid': False,
        'message': '',
        'request': request_text
    }

    # Проверка длины
    length_check = validate_request_length(request_text)
    if not length_check['is_valid']:
        return length_check

    # Проверка содержания
    content_check = validate_request_content(request_text)
    if not content_check['is_valid']:
        return content_check

    result['is_valid'] = True
    result['message'] = 'Запрос принят! Психолог ознакомится с ним перед сеансом.'
    return result
