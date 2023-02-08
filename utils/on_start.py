import asyncio

from base.base_connectors import test_connection


async def loop_test():
    while True:
        await asyncio.sleep(2)
        print("fuck")






async def run():
    test_connection()
    await loop_test()