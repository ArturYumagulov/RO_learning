from gino import Gino
import asyncio

db = Gino()


class DB(db.Model):
    __tablename__ = "Messages"

    id = db.Column(db.Integer(), primary_key=False)
    status = db.Column(db.Unicode(), default='noname')
    message_text = db.Column(db.Unicode(), default='noname')


# Подключаемся к БД
async def connect_db():
    await db.set_bind('postgresql://postgres:postgres@localhost:5432/')
    await db.gino.create_all()
    await db.pop_bind().close()
    # all_user = await db.all()
    # print(all_user)


asyncio.get_event_loop().run_until_complete(connect_db())
