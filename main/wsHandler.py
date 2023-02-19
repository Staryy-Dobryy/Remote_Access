import websockets
import multiprocessing
import threading
import asyncio
import pyautogui
import os
from gtts import gTTS
from playsound import playsound
from pynput import mouse
from pynput.keyboard import Key,Controller
from random import randint

async def socketHandler(websocket):
    threading.Thread(target = lambda: asyncio.run(stream(websocket))).start()
    while True:
        message = await websocket.recv()
        message = message.split("|")
        print(message)
        tasks(message)
        

async def main():
    asyncio.create_task(ping())
    async with websockets.serve(socketHandler, "192.168.56.101", 8081):
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
        await websocket.send(f"url('http://192.168.56.101:8080/static/image.jpg?r={x}')")

async def ping():
    nameOS = os.uname()
    oSys = nameOS.sysname + " " + nameOS.release
    ip = getIp()
    connection = False
    while connection == False:
        # Try change status on client app
        # If not in the database, adds in
        try:
            async with websockets.connect("ws://192.168.56.102:8081") as serverConnection:
                connection = True
                await serverConnection.send(f"ADD|{oSys}|{ip}")
        except ConnectionRefusedError as error:
            print(error)
            await asyncio.sleep(5)

def getIp():
    os.system("ifconfig enp0s8 > .ifconfig.txt")
    with open(".ifconfig.txt", "r") as config:
        line = config.readlines()[1]
        ip = line.split(" ")
        for item in range(len(ip)):
            if ip[item] == "inet": return ip[item + 1]

def tasks(task):
    keyboard = Controller()
    match task[0]:
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
            s = gTTS(task[1])
            s.save('sample.mp3')
            playsound('sample.mp3')
        case "ALERT":
            pyautogui.alert(task[1])
        case "pcOFF":
            os.system("poweroff")
        case "pcREBOOT":
            os.system("reboot")
        case "pcBLOCK":
            os.system("dm-tool lock")
        case "MONITOR":
            multiprocessing.Process(target = lambda: asyncio.run(os.system('mate-system-monitor'))).start()
        case "OPEN-FIREFOX":
            multiprocessing.Process(target = lambda: asyncio.run(os.system('firefox'))).start()
        case "OPEN-CALC":
            multiprocessing.Process(target = lambda: asyncio.run(os.system('gnome-calculator'))).start()
        case "OPEN-FILES":
            multiprocessing.Process(target = lambda: asyncio.run(os.system('/usr/bin/caja --no-desktop --browser'))).start()
        case "OPEN-TERMINAL":
            multiprocessing.Process(target = lambda: asyncio.run(os.system('mate-terminal'))).start()
        
        # YouTube

        case "TUBE":
            link = task[1].replace(" ", "+")
            os.system(f'firefox https://www.youtube.com/results?search_query={link} ')
        case "PAUSE":
            keyboard.press("k")
            keyboard.release("k")
        case "NEXT":
            keyboard.press(Key.shift)
            keyboard.press("n")
            keyboard.release("n")
            keyboard.release(Key.shift)
        case "SUBTTL":
            keyboard.press("c")
            keyboard.release("c")
        case "FULL":
            keyboard.press("f")
            keyboard.release("f")