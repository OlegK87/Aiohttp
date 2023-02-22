import json
from aiohttp import web
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

PG_DSN = "postgresql+asyncpg://app:secret@127.0.0.1:5431"
engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class Advertisement(Base):

    __tablename__ = 'advertisement'

    id = Column(Integer, primary_key=True, autoincrement=True)
    header = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    owner = Column(Integer, nullable=False)

@web.middleware
async def session_middleware(requests: web.Request, handler):
    async with Session() as session:
        requests['session'] = session
        return await handler(requests)

app = web.Application()

async def orm_context(app: web.Application):
    print('START')
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print('SHUTDOWN')

app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)

async def get_advertisement(advertisement_id: int, session: Session):

    advertisement = await session.get(Advertisement, advertisement_id)

    if advertisement is None:
        raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'message': 'advertisement not found'}),
                               content_type='application/json')
    return advertisement

class AdvertisementView(web.View):

    async def get(self):
        session = self.request['session']
        advertisement_id = int(self.request.match_info['advertisement_id'])
        advertisement = await get_advertisement(advertisement_id, session)
        return web.json_response({
                'id': advertisement.id,
                'header': advertisement.header,
                'description': advertisement.description,
                'creation_time': advertisement.creation_time.isoformat(),
                'owner': advertisement.owner
            })

    async def post(self):
        session = self.request['session']
        json_data = await self.request.json()
        advertisement = Advertisement(**json_data)
        session.add(advertisement)
        try:
            await session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(text=json.dumps({'status': 'error', 'message': 'advertisement already exists'}),
                                   content_type='application/json')

        return web.json_response(
            {'id': advertisement.id}
        )

    async def patch(self):
        advertisement_id = int(self.request.match_info['advertisement_id'])
        advertisement = await get_advertisement(advertisement_id, self.request['session'])
        json_data = await self.request.json()
        for field, value in json_data.items():
            setattr(advertisement, field, value)
        self.request['session'].add(advertisement)
        await self.request['session'].commit()
        return web.json_response({'status': 'success'})

    async def delete(self):
        advertisement_id = int(self.request.match_info['advertisement_id'])
        advertisement = await get_advertisement(advertisement_id, self.request['session'])
        await self.request['session'].delete(advertisement)
        await self.request['session'].commit()
        return web.json_response({'status': 'success'})


app.add_routes([
    web.get('/advertisements/{advertisement_id:\d+}/', AdvertisementView),
    web.post('/advertisements/', AdvertisementView),
    web.patch('/advertisements/{advertisement_id:\d+}/', AdvertisementView),
    web.delete('/advertisements/{advertisement_id:\d+}/', AdvertisementView),
])

if __name__ == '__main__':
    web.run_app(app)
