from aio_pika import connect_robust, Message
import asyncio


async def main(loop):
    connection = await connect_robust("amqp://guest:guest@localhost:5672/", loop=loop)

    queue_name = "test_queue"
    routing_key = "test_key"
    exchange = 'messages'

    # Создаем канал
    channel = await connection.channel()

    # Декларируем обработчик
    exchange = await channel.declare_exchange(exchange, durable=True)

    # Декларируем очередь
    queue = await channel.declare_queue(queue_name)

    # Связь между очередбю и обработчиком
    await queue.bind(exchange, routing_key)

    await exchange.publish(
        Message(
            bytes("Hello, World!", 'utf-8'),
            type="text",
            content_type='text/plan',
            headers={'foo': 'bar'}
        ),
        routing_key
     )

    # Получение
    incoming_message = await queue.get(timeout=5)
    print(incoming_message)
    # Подтвердить получение
    await incoming_message.ack()
    await queue.unbind(exchange, routing_key)
    await queue.delete()
    await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
