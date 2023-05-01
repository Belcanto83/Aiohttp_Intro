from aiohttp import web

from db_schema import engine
from middleware import session_middleware
from models import Base
from urls import setup_routes

app = web.Application()
setup_routes(app)


async def app_context(app):
    print('Start')
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    yield
    print('Finish')


app.cleanup_ctx.append(app_context)
app.middlewares.append(session_middleware)


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8081)
