import websockets
import multiprocessing
import threading
import asyncio
from DBworcker import addData
from pynput import mouse, keyboard

stream = False

async def socketHandler(websocket):
    while True:
        message = await websocket.recv()
        message = message.split("|")
        print(message)
        await wsTask(message, websocket)

async def main():
    async with websockets.serve(socketHandler, "127.0.0.1", 8081):
        await asyncio.Future()

def process():
    process = multiprocessing.Process(target = lambda: asyncio.run(main()))
    process.start()
    print("ws - start")

async def wsTask(message, websocket):
    match message[0]:
        case "ADD":
            addData("users.db", message)
            print("add", message)
        case "STREAM":
            global stream
            stream = int(message[1])

            async with websockets.connect("ws://localhost:8765") as serverConnection:
                listenInput(serverConnection)
                stream = await websocket.recv()
                print("STOP STREAM")

def listenInput(websocket):
    treads = []
    treads.append(threading.Thread(target = lambda: asyncio.run(mouseControle(websocket))))
    treads.append(threading.Thread(target = lambda: asyncio.run(keyboardControle(websocket))))
    for tread in treads:
        tread.start()

async def mouseControle(websocket):
    global stream
    while stream == 1:
        with mouse.Events() as events:
            event = events.get(1)
            if event is None:
                print('You did not interact with the mouse within one second')
            else:
                if isinstance(event, mouse.Events.Move):
                    move = "Move " + str(event.x) + " " + str(event.y)
                    await websocket.send(move)
                elif isinstance(event, mouse.Events.Click):
                    click = "Click " + str(event.button) + " " + str(event.pressed)
                    await websocket.send(click)
                elif isinstance(event, mouse.Events.Scroll):
                    scroll = "Scroll " + str(event.dx) + " " + str(event.dy)
                    await websocket.send(scroll)  

async def keyboardControle(websocket):
    global stream
    while stream == 1:
        with keyboard.Events() as events:
            event = events.get(1)
            if event is None:
                print('None click keyboard')
            else:
                key = str(event.key)
                try:
                    key = key.replace("'", "")
                finally:
                    if str(event)[0] == "P":
                        button = "Press " + key
                        await websocket.send(button)
                    else:
                        button = "Release " + key
                        await websocket.send(button)