import asyncio
from aiohttp import ClientSession

async def main():

    async with ClientSession() as session:

        response = await session.post('http://127.0.0.1:8080/advertisements/', json={'header': 'job2', 'description': 'super',
                                                                      'owner': 2})

        print(response.status)
        print(await response.json())


        response = await session.get('http://127.0.0.1:8080/advertisements/3/'
                                     )

        print(response.status)
        print(await response.json())


        response = await session.patch('http://127.0.0.1:8080/advertisements/3/', json={'description': 'Oleg'})


        print(response.status)
        print(await response.json())

        response = await session.get('http://127.0.0.1:8080/advertisements/3/'
                                     )

        print(response.status)
        print(await response.json())

        response = await session.delete('http://127.0.0.1:8080/advertisements/3/'
                                        )

        print(response.status)
        print(await response.json())

        response = await session.get('http://127.0.0.1:8080/advertisements/3/'
                                     )
        print(response.status)
        print(await response.json())


asyncio.run(main())
