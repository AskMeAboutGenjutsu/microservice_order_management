import functools

from aiohttp import web

from routes import setup_routes
from database_interaction import create_database_connection, destroy_database_connection


async def make_app():
    app = web.Application()
    app.on_startup.append(functools.partial(create_database_connection, db_name='orders_data.db'))
    app.on_cleanup.append(destroy_database_connection)
    setup_routes(app)
    return app

web.run_app(make_app(), host='localhost', port=8080)