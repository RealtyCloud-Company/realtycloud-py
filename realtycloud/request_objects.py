from typing import Dict, Optional
from .validate import validate_address, validate_object_key, validate_owner
from datetime import datetime

__all__ = ["RealtyObject", "RealtyOwner"]


class RealtyObject:
    """Запрос на заказ объекта."""

    def __init__(self, key: str, address: Optional[str] = ""):
        validate_object_key(key)
        validate_address(address)
        self.key = key
        self.address = address

    def to_dict(self, product_name: str) -> Dict[str, str]:
        """Преобразование запроса в словарь для отправки."""
        return {
            "product_name": product_name,
            "object_key": self.key,
            "object_address": self.address,
        }


class RealtyOwner:
    """Данные владельца."""

    def __init__(
        self,
        last_name: str = "",
        first_name: str = "",
        middle_name: str = "",
        passport: str = "",
        birthday: str = "",
        region: str = "",
        inn: str = "",
        registration_number: str = "",
    ):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.passport = passport
        self.birthday = birthday
        self.region = region
        self.inn = inn
        self.registration_number = registration_number
        self.validate()

    def validate(self) -> None:
        """Проверка корректности данных владельца."""
        validate_owner(self)

    def _convert_date(self, date_str: str) -> str:
        """Конвертация даты в нужный формат."""
        return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%dT00:01:00.0Z")

    def to_dict(self) -> Dict[str, str]:
        """Преобразование данных владельца в словарь для отправки."""
        return {
            "owner_type": 0,
            "first": self.first_name,
            "surname": self.last_name,
            "patronymic": self.middle_name,
            "passport": self.passport,
            "birthday": self._convert_date(self.birthday),
            "region": self.region,
            "inn": self.inn,
            "registration_number": self.registration_number,
        }
