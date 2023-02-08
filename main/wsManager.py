import websockets
import multiprocessing
import asyncio
from DBworcker import addData

async def socketHandler(websocket):
    while True:
        message = await websocket.recv()
        message = message.split("|")
        print(message)
        wsTask(message)

async def main():
    async with websockets.serve(socketHandler, "127.0.0.1", 8081):
        await asyncio.Future()

def process():
    process = multiprocessing.Process(target = lambda: asyncio.run(main()))
    process.start()
    print("ws - start")

def wsTask(message):
    match message[0]:
        case "ADD":
            addData("users.db", message)
            print("add", message)
        case "STREAM":
            print("stream")

def addToDataBase():
    ...
