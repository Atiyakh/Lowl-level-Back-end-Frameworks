import asyncio
import copy

async def bar():
    print('bar ran correctly')

async def foo():
    b = bar()
    await b
    asyncio.run(b)

asyncio.run(foo())
