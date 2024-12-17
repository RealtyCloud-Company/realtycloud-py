# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional

from httpx import Response


__all__ = [
    "RealtycloudAPIStatusException",
    "RealtycloudBadRequestException",
    "RealtycloudForbiddenException",
    "RealtycloudNotFoundException",
    "RealtycloudServerErrorException",
    "RealtycloudInvalidKeyException",
    "RealtycloudFieldErrorException",
    "RealtycloudRequestLimitExceededException",
    "RealtycloudGenericErrorException",
]


class RealtycloudException(Exception):
    """Базовый класс исключений, возвращаемый, когда ничего более специфичного не применимо"""

    def __init__(self, message: Optional[str] = None) -> None:
        super(RealtycloudException, self).__init__(message)

        self.message = message

    def __str__(self) -> str:
        msg = self.message or "<empty message>"
        return msg

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={str(self)})"


class RealtycloudAPIStatusException(RealtycloudException):
    """Возвращается, когда API отвечает сообщением об ошибке"""

    def __init__(
        self,
        message: Optional[str] = None,
        http_status: Optional[int] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.http_status = http_status
        self.headers = headers or {}

    @classmethod
    def from_response(
        cls, response: Response, message: Optional[str] = None
    ) -> RealtycloudException:
        return cls(
            message=message or response.text,
            http_status=response.status_code,
            headers=dict(response.headers),
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={str(self)}, http_status={self.http_status})"


class RealtycloudBadRequestException(RealtycloudAPIStatusException):
    """Возвращается, когда API отвечает с ошибкой 400 Bad Request"""

    pass


class RealtycloudForbiddenException(RealtycloudAPIStatusException):
    """Возвращается, когда API отвечает с ошибкой 403 Forbidden"""

    pass


class RealtycloudNotFoundException(RealtycloudAPIStatusException):
    """Возвращается, когда API отвечает с ошибкой 404 Not Found"""

    pass


class RealtycloudServerErrorException(RealtycloudAPIStatusException):
    """Возвращается, когда API отвечает с ошибкой 500 Internal Server Error"""

    pass


class RealtycloudInvalidKeyException(RealtycloudAPIStatusException):
    """Возвращается, когда API отвечает с ошибкой о невалидном ключе"""

    pass


class RealtycloudFieldErrorException(RealtycloudAPIStatusException):
    """Возвращается, когда API отвечает с ошибкой об некорректно указанном поле"""

    pass


class RealtycloudRequestLimitExceededException(RealtycloudAPIStatusException):
    """Возвращается, когда API отвечает с ошибкой о превышении лимита запросов"""

    pass


class RealtycloudGenericErrorException(RealtycloudAPIStatusException):
    """Возвращается для других общих ошибок"""

    pass
