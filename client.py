import asyncio
import aiohttp


async def get_data():
    async with aiohttp.ClientSession() as session:
        # async with session.get('http://127.0.0.1:8081/') as response:
        #     print(response.status)
        #     json_data = await response.json()
        #     print(json_data)

        async with session.get('http://127.0.0.1:8081/users/10') as response:
            print(response.status)
            json_data = await response.json()
            print(json_data)

        async with session.get('http://127.0.0.1:8081/advertisements/11') as response:
            print(response.status)
            json_data = await response.json()
            print(json_data)

        # async with session.post('http://127.0.0.1:8081/users/', json={
        #     'username': 'Arthur',
        #     'password': '1234567www'
        # }) as response:
        #     print(response.status)
        #     json_data = await response.json()
        #     print(json_data)

        # async with session.post('http://127.0.0.1:8081/advertisements/', json={
        #     'title': 'Broom',
        #     'description': 'Old broom, but super fast',
        #     'owner_id': 11
        # }) as response:
        #     print(response.status)
        #     json_data = await response.json()
        #     print(json_data)

        # async with session.post('http://127.0.0.1:8081/advertisements/', json={
        #     'title': 'Luck potion',
        #     'description': 'Luck potion, 150 mg',
        #     'owner_id': 1
        # }) as response:
        #     print(response.status)
        #     json_data = await response.json()
        #     print(json_data)

        # async with session.patch('http://127.0.0.1:8081/users/11', json={
        #     'username': 'McGonagall',
        # }) as response:
        #     print(response.status)
        #     json_data = await response.json()
        #     print(json_data)

        async with session.patch('http://127.0.0.1:8081/advertisements/11', json={
            'description': 'My old broom, but super fast',
            # 'owner_id': 3
        }) as response:
            print(response.status)
            json_data = await response.json()
            print(json_data)

        # async with session.post('http://127.0.0.1:8081/login/', json={
        #     'username': 'Lyupin',
        #     'password': 'Ob1yuu7t'
        # }) as response:
        #     print(response.status)
        #     json_data = await response.json()
        #     print(json_data)

        # async with session.delete('http://127.0.0.1:8081/users/11') as response:
        #     print(response.status)
        #     json_data = await response.json()
        #     print(json_data)

        # async with session.delete('http://127.0.0.1:8081/advertisements/1') as response:
        #     print(response.status)
        #     json_data = await response.json()
        #     print(json_data)


if __name__ == '__main__':
    asyncio.run(get_data())
