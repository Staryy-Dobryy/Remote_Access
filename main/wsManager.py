import websockets
import multiprocessing
import asyncio
from DBworcker import addData
from pynput import mouse

async def socketHandler(websocket):
    while True:
        message = await websocket.recv()
        message = message.split("|")
        print(message)
        await wsTask(message)

async def main():
    async with websockets.serve(socketHandler, "127.0.0.1", 8081):
        await asyncio.Future()

def process():
    process = multiprocessing.Process(target = lambda: asyncio.run(main()))
    process.start()
    print("ws - start")

async def wsTask(message):
    match message[0]:
        case "ADD":
            addData("users.db", message)
            print("add", message)
        case "STREAM":
            print("stream")
            while True:
                mouseControle()

def mouseControle():
    with mouse.Events() as events:
        event = events.get(1.0)
        if event is None:
            print('You did not interact with the mouse within one second')
        else:
            print (event)
