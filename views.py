from aiohttp import web
from aiohttp.web_request import Request

from database_interaction import DB_KEY
from models import Order
from order_api_exception import OrderAPIException


async def post_order(request: Request):
    try:
        data = await request.json()
        db = request.app[DB_KEY]
        order = Order(db, **data)
        order.validate()
        await order.create()
        return web.json_response(data=order.to_dict())
    except OrderAPIException as e:
        raise web.HTTPBadRequest(body=e.message)


async def get_order(request: Request):
    order_id = int(request.match_info['id'])
    db = request.app[DB_KEY]
    order = Order(db, order_id=order_id)
    await order.read()
    return web.json_response(data=order.to_dict())


async def patch_order(request: Request):
    order_id = int(request.match_info['id'])
    data = await request.json()
    db = request.app[DB_KEY]
    order = Order(db, order_id=order_id, **data)
    order.validate_before_update()
    await order.update()
    return web.json_response(data=order.to_dict())
