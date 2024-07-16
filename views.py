from aiohttp import web
from aiohttp.web_request import Request

from database_interaction import DB_KEY
from models import Order
from order_api_exception import OrderAPIException


# контроллер, обработка POST запроса
async def post_order(request: Request):
    try:
        data = await request.json()
        db = request.app[DB_KEY]
        order = Order(db, **data)
        order.validate()
        await order.create()
        return web.json_response(data=order.to_dict(), status=201)
    except OrderAPIException as e:
        raise web.HTTPBadRequest(text=e.message)


# контроллер, обработка GET запроса
async def get_order(request: Request):
    try:
        order_id = int(request.match_info['id'])
        db = request.app[DB_KEY]
        order = Order(db, order_id=order_id)
        await order.read()
        return web.json_response(data=order.to_dict())
    except OrderAPIException as e:
        raise web.HTTPBadRequest(text=e.message)
    except ValueError as e:
        raise web.HTTPBadRequest(text=e.args[0])


# контроллер, обработка PATCH запроса
async def patch_order(request: Request):
    try:
        order_id = int(request.match_info['id'])
        data = await request.json()
        db = request.app[DB_KEY]
        order = Order(db, order_id=order_id, **data)
        order.validate_before_update()
        await order.update()
        return web.json_response(data=order.to_dict())
    except OrderAPIException as e:
        raise web.HTTPBadRequest(text=e.message)
    except ValueError as e:
        raise web.HTTPBadRequest(text=e.args[0])
