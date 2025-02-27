"""
    settings
"""
TIMEOUT_SEC = 30

# Регулярное выражение для проверки object_key
OBJECT_KEY_REGEX = r"^\d{1,2}:\d{1,2}:(\d|\d{6,7}):\d{1,10}$"
# Максимальная длина адреса
MAX_ADDRESS_LENGTH = 255
# Ограничения для полей владельца
LAST_NAME_FIRST_NAME_MIDDLE_NAME_REGEX = r"^[А-Яа-яЁё-]+$"
PASSPORT_LENGTH = 10
BIRTHDAY_FORMAT = "%d.%m.%Y"
REGION_MAX_LENGTH = 3
INN_LENGTH_LEGAL = 10
INN_LENGTH_INDIVIDUAL = 12
REGISTRATION_NUMBER_MAX_LENGTH = 60
COMPANY_NAME_MAX_LENGTH = 1024