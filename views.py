import json
from aiohttp import web
from bcrypt import hashpw, checkpw, gensalt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
import pydantic

from models import User, Advertisement
from validators import CreateUserValidationModel, PatchUserValidationModel, \
    CreateAdvValidationModel, PatchAdvValidationModel


async def hello(request: web.Request):
    return web.json_response({'data': 'hello'})


async def login(request: web.Request):
    json_data = await request.json()
    query = select(User).where(User.username == json_data['username'])
    result = await request['session'].execute(query)
    user = result.scalar()
    if user:
        is_passwd_correct = checkpw(json_data['password'].encode(), user.password.encode())
        if is_passwd_correct:
            return web.json_response({'status': 'success'})
    raise web.HTTPUnauthorized(
        text=json.dumps({"error": "user's password is incorrect"}),
        content_type='application/json'
    )


async def get_users(request: web.Request):
    response = web.StreamResponse()
    await response.prepare(request)
    query = select(User)
    users = await request['session'].execute(query)
    for user in users.scalars():
        await response.write(json.dumps(
            {'user_id': user.id,
             'username': user.username}
        ).encode()
                             )
    return response


class UserView(web.View):
    async def _get_item(self, user_id: int):
        user = await self.request['session'].get(User, user_id)
        if user is None:
            raise web.HTTPNotFound(
                text=json.dumps({'error': 'User not found'}),
                content_type='application/json'
            )
        return user

    @staticmethod
    async def _add_item_to_db(obj, session):
        try:
            session.add(obj)
            await session.commit()
            return web.json_response({'user_id': obj.id})
        except IntegrityError:
            await session.rollback()
            raise web.HTTPConflict(
                text=json.dumps({'error': 'User already exists'}),
                content_type='application/json'
            )

    async def get(self):
        user = await self._get_item(int(self.request.match_info['user_id']))
        return web.json_response({
            'id': user.id,
            'username': user.username
        })

    async def post(self):
        json_data = await self.request.json()
        # Валидация данных
        try:
            CreateUserValidationModel(**json_data)
        except pydantic.ValidationError as err:
            raise web.HTTPBadRequest(
                text=json.dumps({"error": err.errors()}),
                content_type='application/json'
            )
        # Хэшируем пароль
        json_data['password'] = hashpw(json_data['password'].encode(), gensalt()).decode()
        obj = User(**json_data)
        # Записываем объект в базу
        return await self._add_item_to_db(obj, self.request['session'])

    # optional
    async def patch(self):
        json_data = await self.request.json()
        # Валидация данных
        try:
            PatchUserValidationModel(**json_data)
        except pydantic.ValidationError as err:
            raise web.HTTPBadRequest(
                text=json.dumps({"error": err.errors()}),
                content_type='application/json'
            )
        user = await self._get_item(int(self.request.match_info['user_id']))
        # Устанавливаем ("патчим") атрибуты объекта
        for field, value in json_data.items():
            setattr(user, field, value)
        # Записываем объект в базу
        return await self._add_item_to_db(user, self.request['session'])

    async def delete(self):
        user = await self._get_item(int(self.request.match_info['user_id']))
        await self.request['session'].delete(user)
        await self.request['session'].commit()
        return web.json_response({'status': 'success'})


class AdvertisementView(web.View):
    async def _get_item(self, adv_id: int):
        adv = await self.request['session'].get(Advertisement, adv_id)
        if adv is None:
            raise web.HTTPNotFound(
                text=json.dumps({'error': 'Advertisement not found'}),
                content_type='application/json'
            )
        return adv

    @staticmethod
    async def _add_item_to_db(obj, session):
        try:
            session.add(obj)
            await session.commit()
            return web.json_response({'adv_id': obj.id})
        except IntegrityError:
            await session.rollback()
            raise web.HTTPConflict(
                text=json.dumps({'error': 'Integrity error'}),
                content_type='application/json'
            )

    async def get(self):
        adv = await self._get_item(int(self.request.match_info['adv_id']))
        return web.json_response({
            'id': adv.id,
            'title': adv.title,
            'description': adv.description,
            'date_created': adv.date_created.strftime("%d.%m.%Y, %H:%M:%S"),
            'owner_id': adv.owner_id
        })

    async def post(self):
        json_data = await self.request.json()
        # Валидация данных
        try:
            CreateAdvValidationModel(**json_data)
        except pydantic.ValidationError as err:
            raise web.HTTPBadRequest(
                text=json.dumps({"error": err.errors()}),
                content_type='application/json'
            )
        # Создаем объект
        obj = Advertisement(**json_data)
        # Записываем объект в базу
        return await self._add_item_to_db(obj, self.request['session'])

    # optional
    async def patch(self):
        json_data = await self.request.json()
        # Валидация данных
        try:
            PatchAdvValidationModel(**json_data)
        except pydantic.ValidationError as err:
            raise web.HTTPBadRequest(
                text=json.dumps({"error": err.errors()}),
                content_type='application/json'
            )
        adv = await self._get_item(int(self.request.match_info['adv_id']))
        if adv.owner_id != json_data.get('owner_id', adv.owner_id):
            raise web.HTTPBadRequest(
                text=json.dumps({"error": "Not allowed to change owner_id"}),
                content_type='application/json'
            )
        # Устанавливаем ("патчим") атрибуты объекта
        for field, value in json_data.items():
            setattr(adv, field, value)
        # Записываем объект в базу
        return await self._add_item_to_db(adv, self.request['session'])

    async def delete(self):
        adv = await self._get_item(int(self.request.match_info['adv_id']))
        await self.request['session'].delete(adv)
        await self.request['session'].commit()
        return web.json_response({'status': 'success'})
