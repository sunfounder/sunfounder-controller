#!/usr/bin/env python3

# import asyncio
# from websockets.server import serve

# async def echo(websocket):
#     async for message in websocket:
#         await websocket.send(f'xxx: {message}')

# async def main():
#     # async with serve(echo, "localhost", 8765):
#     async with serve(echo, "0.0.0.0", 8765):
#         await asyncio.Future()  # run forever

# asyncio.run(main())

''''###########################################################
python -m websockets ws://localhost:8765/
###########################################################'''

#!/usr/bin/env python3

import asyncio

import websockets


async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())