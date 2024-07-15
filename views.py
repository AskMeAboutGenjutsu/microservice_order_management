from aiohttp import web
from aiohttp.web_request import Request

from database_interaction import DB_KEY
from models import Order


async def post_order(request: Request):
    data = await request.json()
    db = request.app[DB_KEY]
    order = Order(db, **data)
    order.validate()
    await order.create()
    return web.json_response(data=order.to_dict())


async def get_order(request: Request):
    order_id = int(request.match_info['id'])
    db = request.app[DB_KEY]
    order = Order(db, order_id=order_id)
    await order.get()
    return web.json_response(data=order.to_dict())