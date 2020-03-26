import aiohttp
from gino import Gino
from aiohttp import web
from aio_pika import connect_robust, Message
from aiohttp.web_app import Application

db = Gino()


class Server(web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_routes([
            web.get('/messages/{id}', self.send_rabbit)
        ])

    async def send_rabbit(self, request):

        connection = connect_robust("amqp://guest:guest@localhost:5672/")

        routing_key = "test_key"

        channel = await connection.channel()
        exchange = await channel.declare_exchange('message', durable=True)
        queue = await channel.declare_queue("test_queue")
        await queue.bind(exchange, routing_key)
        await exchange.publish(
            Message(
                bytes("Hello, World!", 'utf-8'),
                type="text",
                content_type='application/json',
                headers={'foo': 'bar'}
            ),
            routing_key
        )
        # incoming_message = await queue.get(timeout=5)
        # print(incoming_message)
        # Подтвердить получение
        # await incoming_message.ack()
        # await queue.unbind(exchange, routing_key)
        # await queue.delete()
        await connection.close()


server = Server()
web.run_app(server)
