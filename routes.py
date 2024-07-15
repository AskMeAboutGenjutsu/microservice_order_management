from views import post_order


def setup_routes(app):
    app.router.add_post('/api/v1/order', post_order)