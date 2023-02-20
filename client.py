import asyncio
from aiohttp import ClientSession

async def main():

    async with ClientSession() as session:

        response = await session.post('http://127.0.0.1:8080/users/', json={'name': 'user_31',
                                                                             'password': '1234'},
                                       )
        print(response.status)
        print(await response.json())


        response = await session.get('http://127.0.0.1:8080/users/7'
                                     )

        print(response.status)
        print(await response.json())

        #
        # response = await session.patch('http://127.0.0.1:8080/users/1', json={'name': 'new_name'}
        #                                )
        #
        # print(response.status)
        # print(await response.json())
        #
        # response = await session.get('http://127.0.0.1:8080/users/1'
        #                              )
        #
        # print(response.status)
        # print(await response.json())
        #
        #
        # response = await session.delete('http://127.0.0.1:8080/users/1'
        #                                )
        #
        # print(response.status)
        # print(await response.json())
        #
        # response = await session.get('http://127.0.0.1:8080/users/1'
        #                              )
        #
        # print(response.status)
        # print(await response.json())


asyncio.run(main())
