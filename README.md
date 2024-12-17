
# Realtycloud API Client

> Обёртка поверх [Realtycloud API](https://download.realtycloud.ru/static/doc.html) 


## Содержание
  - [Установка](#установка)
  - [Начало работы](#начало-работы)
  - [Токен](#токен)
  - [Примеры использования](#примеры-использования)
    1.  [Получение кадастрового номера по адресу](#получение-кадастрового-номера-по-адресу)
    2.  [Создание заказов с отчетами из ЕГРН](#создание-заказов-с-отчетами-из-егрн)
        1.  [Методы для создания одиночных заказов](#методы-для-создания-одиночных-заказов)
            -   [О характеристиках объекта недвижимости](#о-характеристиках-объекта-недвижимости)
            -   [О переходе прав объекта недвижимости](#о-переходе-прав-объекта-недвижимости)
            -   [О характеристиках и переходе прав](#о-характеристиках-и-переходе-прав-объекта-недвижимости)
        2.  [Методы для создания оптовых заказов](#методы-для-создания-оптовых-заказов)
            -   [О характеристиках объекта недвижимости](#о-характеристиках-объекта-недвижимости-оптовый-заказ)
            -   [О переходе прав объекта недвижимости](#о-переходе-прав-объектов-недвижимости-оптовый-заказ)
            -   [О характеристиках и переходе прав](#о-характеристиках-и-переходе-прав-объекта-недвижимости-оптовый-заказ)
    2.  [Проверка на риски, связанных с объектом недвижимости](#проверка-на-риски-связанных-с-объектом-недвижимости)
    3.  [Проверка статусов заказов](#проверка-статусов-заказов)
  - [Получение помощи](#получение-помощи)
  - [Внесение своего вклада в проект](#внесение-своего-вклада-в-проект)
  - [Спонсоры](#спонсоры)
  - [Лицензия](#лицензия)


## Установка

Зависимости:

-   Python 3.7+
-   [httpx](https://pypi.org/project/httpx/)

Вы можете установить или обновить Realtycloud API Client с помощью команды:
```sh
pip install -U realtycloud
```


## Начало работы

Приступив к работе, первым делом необходимо создать экземпляр клиента.

Инициализация синхронного клиента:

```python
from realtycloud.sync import Realtycloud, Owner, OrderObjectRequest

token = "Replace with Realtycloud API key"

realtycloud = Realtycloud(token)
```


## Токен
Токен можно получить в разделе [Настройки](https://realtycloud.ru/user/settings/) Вашего личного кабинета realtycloud.ru

## Примеры использования

### [Получение кадастрового номера по адресу](https://download.realtycloud.ru/static/doc.html#product-10)
```python
>>> realtycloud.suggest("Москва, Рязанский пр-кт, д 74")
[
    { 'object_type': 'Земельный участок', ... },
    { 'object_type': 'Комната, Жилое помещение', ... },
    { 'object_type': 'Нежилое помещение, Нежилые помещения', ... },
    ...
]
```

### Создание заказов с отчетами из ЕГРН

Система поддерживает два варианта создания заказов:

1. **Одиночный заказ**:
   - Это удобный вариант, если вам нужна проверка только одного объекта недвижимости
2. **Оптовый заказ**:
   - Это позволяет вам сэкономить, так как все проверки будут обработаны в одном заказе


### Методы для создания одиночных заказов:

#### [О характеристиках объекта недвижимости](https://download.realtycloud.ru/static/doc.html#product-4)

```python
>>> realty_object = RealtyObject(key="77:04:0002010:1100", address="Москва, Рязанский пр-кт, д 74")
>>> realtycloud.order_single_object(realty_object)
{
    "id": "96d8909d-49d8-41ca-a4c5-25ca7d2fe0ae",
    "order_items": [
        {
            "order_item_id": "d1d29b4a-e281-434f-98b0-54c62af0494e",
            "price": "25",
            "product_name": "EgrnObject"
        }
    ],
    "total_amount": "25",
    "account_info": {
        "not_enough_money": False,
        "balance_current": "200",
        "balance_before": "225"
    }
}
```

#### [О переходе прав объекта недвижимости](https://download.realtycloud.ru/static/doc.html#product-4)

```python
>>> realty_object = RealtyObject(key="77:04:0002010:1100", address="Москва, Рязанский пр-кт, д 74")
>>> realtycloud.order_single_right_list(realty_object)
{
    "id": "96d8909d-49d8-41ca-a4c5-25ca7d2fe0ae",
    "order_items": [
        {
            "order_item_id": "d1d29b4a-e281-434f-98b0-54c62af0494e",
            "price": "25",
            "product_name": "EgrnRightList"
        }
    ],
    "total_amount": "25",
    "account_info": {
        "not_enough_money": False,
        "balance_current": "200",
        "balance_before": "225"
    }
}
```


#### [О характеристиках и переходе прав объекта недвижимости](https://download.realtycloud.ru/static/doc.html#product-4)

```python
>>> realty_object = RealtyObject(key="77:04:0002010:1100", address="Москва, Рязанский пр-кт, д 74")
>>> realtycloud.order_single_full_data(realty_object)
{
    "id": "96d8909d-49d8-41ca-a4c5-25ca7d2fe0ae",
    "order_items": [
        {
            "order_item_id": "d1d29b4a-e281-434f-98b0-54c62af0494e",
            "price": "25",
            "product_name": "EgrnObject"
        },
        {
            "order_item_id": "9ccbea20-02e2-4545-a22d-4d4e93dbe994",
            "price": "25",
            "product_name": "EgrnRightList"
        }
    ],
    "total_amount": "25",
    "account_info": {
        "not_enough_money": False,
        "balance_current": "200",
        "balance_before": "225"
    }
}
```

### Методы для создания оптовых заказов:


#### [О характеристиках объекта недвижимости (оптовый заказ)](https://download.realtycloud.ru/static/doc.html#product-4)

```python
>>> realty_objects = [RealtyObject(key="77:04:0002010:1100", address="Москва, Рязанский пр-кт, д 74"), RealtyObject(key="77:04:0002010:1101")]
>>> realtycloud.order_multiple_objects(realty_objects)
{
    "id": "96d8909d-49d8-41ca-a4c5-25ca7d2fe0ae",
    "order_items": [
        {
            "order_item_id": "d1d29b4a-e281-434f-98b0-54c62af0494e",
            "price": "25",
            "product_name": "EgrnObject"
        },
        {
            "order_item_id": "9ccbea20-02e2-4545-a22d-4d4e93dbe994",
            "price": "25",
            "product_name": "EgrnObject"
        }
    ],
    "total_amount": "25",
    "account_info": {
        "not_enough_money": False,
        "balance_current": "200",
        "balance_before": "225"
    }
}
```


#### [О переходе прав объектов недвижимости (оптовый заказ)](https://download.realtycloud.ru/static/doc.html#product-4)

```python
>>> realty_objects = [RealtyObject(key="77:04:0002010:1100", address="Москва, Рязанский пр-кт, д 74"), RealtyObject(key="77:04:0002010:1101")]
>>> realtycloud.order_multiple_right_lists(realty_objects)
{
    "id": "96d8909d-49d8-41ca-a4c5-25ca7d2fe0ae",
    "order_items": [
        {
            "order_item_id": "d1d29b4a-e281-434f-98b0-54c62af0494e",
            "price": "25",
            "product_name": "EgrnRightList"
        },
        {
            "order_item_id": "9ccbea20-02e2-4545-a22d-4d4e93dbe994",
            "price": "25",
            "product_name": "EgrnRightList"
        }
    ],
    "total_amount": "25",
    "account_info": {
        "not_enough_money": False,
        "balance_current": "200",
        "balance_before": "225"
    }
}
```


#### [О характеристиках и переходе прав объекта недвижимости (оптовый заказ)](https://download.realtycloud.ru/static/doc.html#product-4)

```python
>>> realty_objects = [RealtyObject(key="77:04:0002010:1100", address="Москва, Рязанский пр-кт, д 74"), RealtyObject(key="77:04:0002010:1101")]
>>> realtycloud.order_multiple_full_data(realty_objects)
{
    "id": "96d8909d-49d8-41ca-a4c5-25ca7d2fe0ae",
    "order_items": [
        {
            "order_item_id": "d1d29b4a-e281-434f-98b0-54c62af0494e",
            "price": "25",
            "product_name": "EgrnObject"
        },
        {
            "order_item_id": "9ccbea20-02e2-4545-a22d-4d4e93dbe994",
            "price": "25",
            "product_name": "EgrnRightList"
        },
        {
            "order_item_id": "d1d29b4a-e281-434f-98b0-54c62af04941",
            "price": "25",
            "product_name": "EgrnObject"
        },
        {
            "order_item_id": "9ccbea20-02e2-4545-a22d-4d4e93dbe991",
            "price": "25",
            "product_name": "EgrnRightList"
        }
    ],
    "total_amount": "25",
    "account_info": {
        "not_enough_money": False,
        "balance_current": "200",
        "balance_before": "225"
    }
}
```

### [Проверка на риски, связанных с объектом недвижимости](https://download.realtycloud.ru/static/doc.html#product-5)

```python
>>> realty_object = RealtyObject(key="77:04:0002010:1100", address="Москва, Рязанский пр-кт, д 74")
>>> owners = [RealtyOwner(last_name="Иванов", first_name="Иван", middle_name="Иванович", birthday="12.12.2000")]
>>> realtycloud.order_fulls(realty_object, owners)
{
    "data": {
        "id": "96d8909d-49d8-41ca-a4c5-25ca7d2fe0ae",
        "order_items": [
            {
                "order_item_id": "60243e4c-b102-42a1-a0bc-3c9c26234325",
                "product_name": "RiskAssessmentV2",
                "price": "25"
            }
        ],
        "total_amount": "25",
        "account_info": {
            "not_enough_money": false,
            "balance_current": "200",
            "balance_before": "225"
        }
    }
}
```

### [Проверка статусов заказов](https://download.realtycloud.ru/static/doc.html#product-9)

После создания заказа вы получите уникальные идентификаторы `order_item_id` для каждого продукта. Чтобы узнать текущий статус заказа, отправьте ваши `order_item_id` при помощи этого метода. 

Если заказ выполнен, статус будет `done`, и появится ссылка для скачивания. Пожалуйста, соблюдайте интервал между запросами: опрашивать статус чаще, чем раз в 3 минуты, не имеет смысла. Если вам требуется более быстрая обработка, свяжитесь с нами, и мы предоставим вебхук для автоматического обновления статусов.

**Виды статусов заказа:**
- done — заказ готов.
- refund — возврат средств произведен.
- deleted — заказ удален.
- waitingforpayment — заказ ожидает оплаты.
- actionrequired — если заказ находится в этом статусе более 3 рабочих дней, возможно оформление возврата.
- inprogress — заказ в работе, ожидайте его завершения.

В зависимости от продукта, поле data в ответе будет содержать различные данные. Например, для большинства продуктов доступны следующие поля:
- file_pdf_url — ссылка на отчет в формате PDF.
- file_signed_zip_url — ссылка на zip-архив с подписью.

```python
>>> order_item_ids = ["d1d29b4a-e281-434f-98b0-54c62af0494e", "9ccbea20-02e2-4545-a22d-4d4e93dbe994"]
>>> realtycloud.check_status(order_item_ids)
[
    {
        "order_item_id": "d1d29b4a-e281-434f-98b0-54c62af0494e",
        "product_name": "EgrnRightList",
        "status": "done",
        "data": {
            "file_pdf_url": "https://api.realtycloud.ru/download?orderID=d1d29b4a-e281-434f-98b0-54c62af0494e&fileType=pdf"
        }
    },
    {
        "order_item_id": "9ccbea20-02e2-4545-a22d-4d4e93dbe994",
        "product_name": "EgrnRightList",
        "status": "done",
        "data": {
            "file_pdf_url": "https://api.realtycloud.ru/download?orderID=9ccbea20-02e2-4545-a22d-4d4e93dbe994&fileType=pdf"
        }
    }
]
```


## Внесение своего вклада в проект

Вы можете помочь и сообщив о баге.


## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)
