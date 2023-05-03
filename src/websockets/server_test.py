import asyncio
from websockets.server import serve
from websockets.exceptions import ConnectionClosedOK


async def echo(websocket):
    async for message in websocket:
        print(len(message))
        try:
            await websocket.send(':D')
        except ConnectionClosedOK:
            print('Connection closed')


async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
