from typing import Dict, Optional
from .validate import (
    validate_address,
    validate_object_key,
    validate_owner_legal,
    validate_owner_individual,
)
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
        company_name: str = "",
        registration_number: str = "",
        owner_type: int = "",
    ):
        self.owner_type = owner_type
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.passport = passport
        self.birthday = birthday
        self.region = region
        self.inn = inn
        self.registration_number = registration_number
        self.company_name = company_name
        self.validate()

    def validate(self) -> None:
        """Проверка корректности данных владельца."""
        if self.owner_type not in [0, 1]:
            raise ValueError(
                "Тип собственника должен быть указан явно: 0 - физическое лицо, 1 - юридическое лицо"
            )
        if self.owner_type == 0:
            validate_owner_individual(self)
        if self.owner_type == 1:
            validate_owner_legal(self)

    def _convert_date(self, date_str: str) -> str:
        """Конвертация даты в нужный формат."""
        return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%dT00:01:00.0Z")

    def to_dict(self) -> Dict[str, str]:
        """Преобразование данных владельца в словарь для отправки."""
        return {
            "owner_type": self.owner_type,
            "first": self.first_name,
            "surname": self.last_name,
            "patronymic": self.middle_name,
            "passport": self.passport,
            "birthday": self._convert_date(self.birthday) if self.birthday else "",
            "region": self.region,
            "inn": self.inn,
            "company_name": self.company_name,
            "registration_number": self.registration_number,
        }
