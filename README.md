# Простой микросервис на *aiohttp*
Небольшой Pet-проект, реализация микросервиса по менеджменту заказов.\
Можно создать, посмотреть заказ и изменить его статус.
## API Endpoints
Контроллеры обрабатывающие endpointы находятся в **views.py**.\
URL адреса endpointов находятся в **routes.py**.\
Реализовано 3 API Endpointa:
* post_order - создает заказ по POST запросу, URL - '/api/v1/order';\
Пример запроса:
```shell
curl -X POST http://localhost:8080/api/v1/order -d
'{"user_id": 1, "product_ids": [1, 2, 3, 4]}'
```
* get_order - выдает заказ по GET запросу, URL - '/api/v1/order/{id}';\
Пример запроса:
```shell
curl -X GET http://localhost:8080/api/v1/order/1
```
* patch_order - меняет статус заказа по PATCH запросу, URL - '/api/v1/order/{id}'.\
Пример запроса:
```shell
curl -X PATCH http://localhost:8080/api/v1/order/1 -d 
'{"status": "shipped"}'
```
Чтобы запустить микросервис:
```shell
python3 manage.py
```
## Database
В проекте используется *sqlite*. Для подключения к БД используется *aiosqlite*.\
В БД хранится 2 таблицы:
* orders - таблица с информацией о заказах
* order_product_relationship - таблица, которая хранит привязку id заказа к id продукта
## Tests
В файле *test.py* реализованы простые тесты для каждого endpointa.\
Они помогали понять не сломался ли функционал в процессе разработки.\
Реализованы с помощью *pytest*.\
Чтобы запустить тесты:
```shell
pytest test.py
```