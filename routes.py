from views import post_order, get_order, patch_order


def setup_routes(app):
    app.router.add_post('/api/v1/order', post_order)
    app.router.add_get('/api/v1/order/{id}', get_order)
    app.router.add_patch('/api/v1/order/{id}', patch_order)
