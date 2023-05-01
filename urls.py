from aiohttp import web
from views import UserView, AdvertisementView, hello, login, get_users


def setup_routes(app):
    app.add_routes([
        web.view('/users/{user_id:\d+}', UserView),
        web.post('/users/', UserView),
        web.get('/users', get_users),

        web.view('/advertisements/{adv_id:\d+}', AdvertisementView),
        web.post('/advertisements/', AdvertisementView),

        web.get('/', hello),
        web.post('/login/', login)
    ])
