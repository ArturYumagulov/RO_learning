import asyncio

async def my_coro(delay):
    loop = asyncio.get_running_loop()
    end_time = loop.time() + delay
    while True:
        print("Blocking...")
        await asyncio.sleep(3)
        if loop.time() > end_time:
            print("Done.")
            break

async def main():
    "Основная"
    await my_coro(9.0)

asyncio.run(main())
