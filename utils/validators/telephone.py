import re

def validate_phone(phone: str) -> dict:
    """
    Проверяет валидность номера телефона
    Возвращает dict с результатом проверки
    """
    phone = phone.strip()

    result = {
        'is_valid': False,
        'message': '',
        'phone': phone
    }

    # Проверка на пустоту
    if not phone:
        result['message'] = 'Номер телефона не может быть пустым'
        return result

    # Очищаем номер от всего кроме цифр и +
    cleaned_phone = re.sub(r'[^\d+]', '', phone)

    # Проверка длины
    if len(cleaned_phone) < 10:
        result['message'] = 'Номер телефона слишком короткий'
        return result

    if len(cleaned_phone) > 15:
        result['message'] = 'Номер телефона слишком длинный'
        return result

    # Проверка формата (должен начинаться с +7, 7, 8 или быть без кода)
    if not re.match(r'^(\+7|7|8)?\d{10}$', cleaned_phone):
        result['message'] = 'Неверный формат номера телефона'
        return result

    # Приводим к стандартному формату +7XXXXXXXXXX
    if cleaned_phone.startswith('8'):
        formatted_phone = '+7' + cleaned_phone[1:]
    elif cleaned_phone.startswith('7'):
        formatted_phone = '+' + cleaned_phone
    elif cleaned_phone.startswith('+7'):
        formatted_phone = cleaned_phone
    else:
        formatted_phone = '+7' + cleaned_phone

    result['is_valid'] = True
    result['message'] = 'Номер телефона валиден'
    result['phone'] = formatted_phone
    return result