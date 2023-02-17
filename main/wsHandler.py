import websockets
import multiprocessing
import threading
import asyncio
import pyautogui
import os
from pynput import mouse
from pynput.keyboard import Key,Controller
from random import randint


async def socketHandler(websocket):
    #threading.Thread(target = lambda: asyncio.run(stream(websocket))).start()
    while True:
        message = await websocket.recv()
        print(message)
        tasks(message)
        

async def main():
    asyncio.create_task(ping())
    async with websockets.serve(socketHandler, "10.0.2.15", 8081):
        await asyncio.Future()

def runSocket():
    process = multiprocessing.Process(target = lambda: asyncio.run(main()))
    process.start()
    print("ws - start")

async def stream(websocket):
    while True:
        x = str(randint(0, 1000000))
        screenshot = pyautogui.screenshot()
        screenshot.save("static/image.jpg")
        await websocket.send(f"url('http://10.0.2.15:8080/static/image.jpg?r={x}')")

async def ping():
    async with websockets.connect("ws://127.0.0.1:8081") as serverConnection:
        while True:
            await serverConnection.send("ADD|PC|10.0.2.15|ONLINE")
            await asyncio.sleep(3)

def tasks(task):
    keyboard = Controller()
    match task:
        case "JUMP+":
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
        case "JUMP-":
            keyboard.press(Key.shift)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            keyboard.release(Key.shift)
        case "ENTER":
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        case "V+":
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
        case "V-":
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
        case "SILENCE":
            keyboard.press(Key.media_volume_mute)
            keyboard.release(Key.media_volume_mute)
        case "SPEAK":
            ...
        case "ALERT":
            pyautogui.alert("hello")
        case "pcOFF":
            os.system("poweroff")
        case "pcREBOOT":
            os.system("reboot")
        case "pcBLOCK":
            os.system("dm-tool lock")
        case "MONITOR":
            multiprocessing.Process(target = lambda: os.system('mate-system-monitor')).start()