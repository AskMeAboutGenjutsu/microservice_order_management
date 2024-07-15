import functools
import logging

from aiohttp import web

from logger import AccessLogger
from routes import setup_routes
from database_interaction import create_database_connection, destroy_database_connection


# создание приложения
async def make_app():
    app = web.Application()
    # настройка логов
    logging.basicConfig(level=logging.INFO)
    # при запуске подключается к sqlite
    app.on_startup.append(functools.partial(create_database_connection, db_name='orders_data.db'))
    # при завершении отключается от sqlite
    app.on_cleanup.append(destroy_database_connection)
    # добавление эндпоинтов
    setup_routes(app)
    return app

web.run_app(make_app(), host='localhost', port=8080, access_log_class=AccessLogger)