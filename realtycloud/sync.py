# -*- coding: utf-8 -*-
from typing import Dict, List, Optional, Tuple, Any
from httpx import Response, Client
from datetime import datetime
from re import match

from realtycloud import settings
from .exceptions import (
    RealtycloudBadRequestException,
    RealtycloudForbiddenException,
    RealtycloudNotFoundException,
    RealtycloudServerErrorException,
    RealtycloudInvalidKeyException,
    RealtycloudFieldErrorException,
    RealtycloudRequestLimitExceededException,
    RealtycloudAPIStatusException,
)
from .request_objects import RealtyObject, RealtyOwner

__all__ = ["Realtycloud", "RealtyObject", "RealtyOwner"]


class ClientBase:
    """Базовый класс для API клиента."""

    def __init__(self, base_url: str, token: str):
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "API-Key": token,
        }
        self._client = Client(base_url=base_url, headers=headers)

    def __enter__(self) -> "ClientBase":
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """Закрыть сетевые соединения."""
        self._client.close()

    def _get(
        self, url: str, params: Dict[str, Any], timeout: int = settings.TIMEOUT_SEC
    ) -> Dict[str, Any]:
        """GET-запрос к API Realtycloud."""
        try:
            response = self._client.get(url, params=params, timeout=timeout)
            response.raise_for_status()
        except Exception as e:
            self._handle_api_error(response)

        return response.json()

    def _post(
        self, url: str, data: Dict[str, Any], timeout: int = settings.TIMEOUT_SEC
    ) -> Dict[str, Any]:
        """POST-запрос к API Realtycloud."""
        try:
            response = self._client.post(url, json=data, timeout=timeout)
            response.raise_for_status()
        except Exception as e:
            self._handle_api_error(response)
        return response.json()

    def _handle_api_error(self, response: Response) -> None:
        """Обработка ошибок API и возбуждение соответствующих исключений."""
        if response.status_code == 400:
            raise RealtycloudBadRequestException.from_response(
                response,
                message=f"Статус: {response.status_code}. Сообщение: {response.text}",
            )
        if response.status_code == 403:
            raise RealtycloudForbiddenException.from_response(
                response,
                message=f"Статус: {response.status_code}. Сообщение: {response.text}",
            )
        if response.status_code == 404:
            raise RealtycloudNotFoundException.from_response(
                response,
                message=f"Статус: {response.status_code}. Сообщение: {response.text}",
            )
        if response.status_code == 500:
            error_message = response.json().get("error", "Неизвестная ошибка")
            if "невалидный ключ" in error_message:
                raise RealtycloudInvalidKeyException.from_response(
                    response,
                    message="Неверный ключ",
                )
            elif "неверно указано поле" in error_message:
                raise RealtycloudFieldErrorException.from_response(
                    response,
                    message="Неверно указано поле",
                )
            elif "вы превысили лимит использования поиска" in error_message:
                raise RealtycloudRequestLimitExceededException.from_response(
                    response,
                    message="Превышен лимит использования поиска",
                )
            else:
                raise RealtycloudServerErrorException.from_response(
                    response,
                    message=f"Статус: {response.status_code}. Сообщение: {response.text}",
                )
        raise RealtycloudAPIStatusException.from_response(
            response,
            message=f"Статус: {response.status_code}. Сообщение: {response.text}",
        )


class SuggestClient(ClientBase):
    """Клиент API Realtycloud поиска кадастровых номеров по адресу"""

    BASE_URL = "https://api.realtycloud.ru/search"

    def __init__(self, token: str):
        super().__init__(base_url=self.BASE_URL, token=token)

    def suggest(self, query: str) -> List[Dict]:
        """Получение предложений по заданному запросу."""
        params = {"query": query}
        response = self._get("", params)
        return [
            {
                "object_type": item.get("ObjectType"),
                "number": item.get("Number"),
                "address": item.get("Address"),
                "area": item.get("Area"),
                "cadastral_price": item.get("kad_price"),
                "status": item.get("Status"),
            }
            for item in response.get("data", [])
        ]


class EGRNClient(ClientBase):
    """Клиент API Realtycloud EGRN"""

    BASE_URL = "https://api.realtycloud.ru/order"
    PRODUCT_NAMES = {
        "object": "EgrnObject",
        "object_priority": "EgrnObjectFast",
        "right_list": "EgrnRightList",
        "right_list_priority": "EgrnRightListFast",
    }

    def __init__(self, token: str):
        super().__init__(base_url=self.BASE_URL, token=token)

    def _create_order_data(self, items: List[Tuple[str, str]]) -> Dict:
        """Создание данных заказа для заданного списка (product_name, (key, address))."""
        return {
            "order_items": [
                {
                    "product_name": product_name,
                    "object_key": key,
                    "object_address": address,
                }
                for product_name, (key, address) in items
            ]
        }

    def _post_request(
        self, product_name: str, items: List[RealtyObject]
    ) -> Optional[Dict]:
        """POST-запрос для заданных предметов."""
        data = {"order_items": [item.to_dict(product_name) for item in items]}
        response = self._post("", data)
        return response.get("data")

    def fetch_single_object(self, request: RealtyObject, **kwargs) -> Optional[Dict]:
        """Получить объект с заданным запросом."""
        product_name = self.PRODUCT_NAMES["object_priority"] if kwargs.get('priority', False) else self.PRODUCT_NAMES["object"]
        return self._post_request(product_name, [request])

    def fetch_multiple_objects(self, requests: List[RealtyObject], **kwargs) -> Optional[Dict]:
        """Получить несколько объектов, позволяя использовать необязательные адреса."""
        product_name = self.PRODUCT_NAMES["object_priority"] if kwargs.get('priority', False) else self.PRODUCT_NAMES["object"]
        return self._post_request(product_name, requests)

    def fetch_single_right_list(self, request: RealtyObject, **kwargs) -> Optional[Dict]:
        """Получить список прав с заданным ключом и необязательным адресом."""
        product_name = self.PRODUCT_NAMES["right_list_priority"] if kwargs.get('priority', False) else self.PRODUCT_NAMES["right_list"]
        return self._post_request(product_name, [request])

    def fetch_multiple_right_lists(
        self, requests: List[RealtyObject], **kwargs
    ) -> Optional[Dict]:
        """Получить несколько списков прав, позволяя использовать необязательные адреса."""
        product_name = self.PRODUCT_NAMES["right_list_priority"] if kwargs.get('priority', False) else self.PRODUCT_NAMES["right_list"]
        return self._post_request(product_name, requests)

    def fetch_multiple_full_data(self, request: RealtyObject, **kwargs) -> Optional[Dict]:
        """Получить полные данные для одного объекта и его прав с заданным ключом и необязательным адресом."""
        product_name_object = self.PRODUCT_NAMES["object_priority"] if kwargs.get('priority', False) else self.PRODUCT_NAMES["object"]
        product_name_right_list = self.PRODUCT_NAMES["right_list_priority"] if kwargs.get('priority', False) else self.PRODUCT_NAMES["right_list"]
        order_items = [
            request.to_dict(product_name_object),
            request.to_dict(product_name_right_list),
        ]
        response = self._post("", {"order_items": order_items})
        return response.get("data")


class RiskClient(ClientBase):
    """Клиент API риска Realtycloud."""

    BASE_URL = "https://api.realtycloud.ru/order"

    def __init__(self, token: str):
        super().__init__(base_url=self.BASE_URL, token=token)

    def fetch_risk_assessment_for_individual(
        self, object: RealtyObject, owners: List[RealtyOwner] = None, **kwargs
    ) -> Optional[Dict]:
        """Получить оценку риска для физического лица."""
        if owners is None:
            owners = []

        product_name = "RiskAssessmentFastV2" if kwargs.get('priority', False) else "RiskAssessmentV2"
        data = {
            "order_items": [
                {
                    "product_name": product_name,
                    "object_key": object.key,
                    "object_address": object.address,
                    "metadata": {"ownersData": [owner.to_dict() for owner in owners]},
                }
            ]
        }
        response = self._post("", data)
        return response.get("data")


class StatusClient(ClientBase):
    """Клиент API статуса Realtycloud."""

    BASE_URL = "https://api.realtycloud.ru/orders"

    def __init__(self, token: str):
        super().__init__(base_url=self.BASE_URL, token=token)

    def fetch_status(
        self, order_item_ids: List[str], offset: int = 0, limit: int = 1000
    ) -> Optional[Dict]:
        """Получить статус по заданным идентификаторам заказа."""
        if not order_item_ids:
            order_item_ids = []
        data = {"order_item_ids": order_item_ids, "offset": offset, "limit": limit}
        response = self._post("", data)
        return response.get("data")


class Realtycloud:
    """Синхронный клиент API Realtycloud."""

    def __init__(self, token: str):
        self._egrn_client = EGRNClient(token=token)
        self._suggest_client = SuggestClient(token=token)
        self._risk_client = RiskClient(token=token)
        self._status_client = StatusClient(token=token)

    def suggest(self, query: str, **kwargs) -> List[Dict]:
        """Запрос на получение списка кадастровых номеров по адресу"""
        return self._suggest_client.suggest(query=query, **kwargs)

    def order_single_object(self, request: RealtyObject, **kwargs) -> Optional[Dict]:
        """Запрос на отчет о характеристиках объекта недвижимости"""
        return self._egrn_client.fetch_single_object(request, **kwargs)

    def order_multiple_objects(
        self, requests: List[RealtyObject], **kwargs
    ) -> Optional[Dict]:
        """Запрос на оптовые отчеты о характеристиках объектов недвижимости"""
        return self._egrn_client.fetch_multiple_objects(requests, **kwargs)

    def order_single_right_list(
        self, request: RealtyObject, **kwargs
    ) -> Optional[Dict]:
        """Запрос на отчет о переходе прав объекта недвижимости"""
        return self._egrn_client.fetch_single_right_list(request, **kwargs)

    def order_multiple_right_lists(
        self, requests: List[RealtyObject], **kwargs
    ) -> Optional[Dict]:
        """Запрос на оптовые отчеты о переходе прав объектов недвижимости"""
        return self._egrn_client.fetch_multiple_right_lists(requests, **kwargs)

    def order_single_full_data(self, request: RealtyObject, **kwargs) -> Optional[Dict]:
        """Запрос на отчет о характеристиках и переходе прав объектов недвижимости"""
        return self._egrn_client.fetch_multiple_full_data(request, **kwargs)

    def order_multiple_full_data(
        self, requests: List[RealtyObject], **kwargs
    ) -> Optional[Dict]:
        """Запрос на оптовые отчеты о характеристиках и переходе прав объектов недвижимости"""
        return self._egrn_client.fetch_multiple_full_data(requests, **kwargs)

    def order_risk_assessment_for_individual(
        self, object: RealtyObject, owners: List[RealtyOwner] = None, **kwargs
    ) -> Optional[Dict]:
        """Запрос оценки рисков собственников, связанных с объектом недвижимости"""
        return self._risk_client.fetch_risk_assessment_for_individual(
            object, owners=owners, **kwargs
        )

    def check_status(
        self, order_item_ids: List[str], offset: int = 0, limit: int = 1000, **kwargs
    ):
        """
        После создания заказа вы получите уникальный идентификатор order_item_id для каждого продукта. Чтобы узнать текущий статус заказа, отправьте ваш order_item_id в массиве id.

        Если заказ выполнен, статус будет done, и появится ссылка для скачивания. Пожалуйста, соблюдайте интервал между запросами: опрашивать статус чаще, чем раз в 3 минуты, не имеет смысла. Если вам требуется более быстрая обработка, свяжитесь с нами, и мы предоставим вебхук для автоматического обновления статусов.

        ### Виды статусов заказа:
        - done — заказ готов.
        - refund — возврат средств произведен.
        - deleted — заказ удален.
        - waitingforpayment — заказ ожидает оплаты.
        - actionrequired — если заказ находится в этом статусе более 3 рабочих дней, возможно оформление возврата.
        - inprogress — заказ в работе, ожидайте его завершения.

        В зависимости от продукта, поле data в ответе будет содержать различные данные. Например, для большинства продуктов доступны следующие поля:
        - file_pdf_url — ссылка на отчет в формате PDF.
        - file_signed_zip_url — ссылка на zip-архив с подписью.
        """
        return self._status_client.fetch_status(
            order_item_ids=order_item_ids, offset=offset, limit=limit, **kwargs
        )
