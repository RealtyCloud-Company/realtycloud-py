# -*- coding: utf-8 -*-
from re import match
from realtycloud import settings
from datetime import datetime


def validate_object_key(object_key: str) -> None:
    """Проверка корректности object_key."""
    if not match(settings.OBJECT_KEY_REGEX, object_key):
        raise ValueError(
            f"Неверный object_key: {object_key}. Должен соответствовать регулярному выражению {settings.OBJECT_KEY_REGEX}."
        )


def validate_address(address: str) -> None:
    """Проверка корректности адреса."""
    if len(address) > settings.MAX_ADDRESS_LENGTH:
        raise ValueError(
            f"Адрес не может превышать {settings.MAX_ADDRESS_LENGTH} символов."
        )


def validate_owner(owner) -> None:
    """Проверка корректности данных владельца."""
    if owner.last_name and not match(
        settings.LAST_NAME_FIRST_NAME_MIDDLE_NAME_REGEX, owner.last_name
    ):
        raise ValueError(
            "Фамилия должна состоять из символов А-Яа-яЁё и не может превышать 60 символов."
        )
    if owner.first_name and not match(
        settings.LAST_NAME_FIRST_NAME_MIDDLE_NAME_REGEX, owner.first_name
    ):
        raise ValueError(
            "Имя должно состоять из символов А-Яа-яЁё и не может превышать 60 символов."
        )
    if owner.middle_name and not match(
        settings.LAST_NAME_FIRST_NAME_MIDDLE_NAME_REGEX, owner.middle_name
    ):
        raise ValueError(
            "Отчество должно состоять из символов А-Яа-яЁё и не может превышать 60 символов."
        )

    if owner.passport and (
        len(owner.passport) != settings.PASSPORT_LENGTH or not owner.passport.isdigit()
    ):
        raise ValueError("Паспорт должен быть строкой из точно 10 цифр.")

    if owner.birthday:
        try:
            datetime.strptime(owner.birthday, settings.BIRTHDAY_FORMAT)
        except ValueError:
            raise ValueError("Дата рождения должна быть в формате DD.MM.YYYY.")

    if owner.region:
        if (
            not (1 <= len(owner.region) <= settings.REGION_MAX_LENGTH)
            or not owner.region.isdigit()
        ):
            raise ValueError(
                f"Регион должен быть строкой из цифр с максимальной длиной {settings.REGION_MAX_LENGTH}."
            )
        if len(owner.region) == 1:
            owner.region = owner.region.zfill(2)

    if owner.inn != "" and (len(owner.inn) != settings.INN_LENGTH or not owner.inn.isdigit()):
        raise ValueError("ИНН должен быть строкой из точно 12 цифр.")

    if owner.registration_number and len(owner.registration_number) > settings.REGISTRATION_NUMBER_MAX_LENGTH:
        raise ValueError(
            f"Регистрационный номер не может превышать {settings.REGISTRATION_NUMBER_MAX_LENGTH} символов."
        )
