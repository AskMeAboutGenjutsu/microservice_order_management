from aiohttp import web
from aiohttp.web_request import Request

from database_interaction import DB_KEY
from models import Order


async def post_order(request: Request):
    data = await request.json()
    db = request.app[DB_KEY]
    order = Order(db, **data)
    order.validate()
    order_id = await order.create()
    return web.json_response(data={'order_id': order_id})
