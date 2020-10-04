import json
import cv2 as cv
import numpy as np
import threading
import time
import sys
import keyboard
import random
from datetime import datetime
import pyautogui
from playsound import playsound
from pyautogui import press

global WEED_COUNT, KEY_START_PROGRAM, KEY_STOP_PROGRAM, isProgramStarted

def find_isTunner():
    try:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        threshold = 0.99
        template = cv.imread("img/tunner.png",0)
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        w, h = template.shape[::-1]
        isTunner = False
        for pt in zip(*loc[::-1]):
            cv.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 0)
            isTunner = True
            break

        if(not isTunner):
            print("JEST TUNNER!")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
        else:
            cv.destroyAllWindows()
            print("Nie ma tunera")
            waitRandom = random.uniform(3.800, 5.50)
            time.sleep(waitRandom)
            press("e")
            time.sleep(0.7)
            find_isTunner()
    except:
        print("Wystąpił jakiś błąd, ponawiam...")
        find_isTunner()


def open_settings():
    print(str(datetime.now()) + "    Ładowanie ustawień użytkownika...")
    with open('settings.json') as f:
        data = json.load(f)
    global WEED_COUNT, KEY_START_PROGRAM, KEY_STOP_PROGRAM
    WEED_COUNT = float(data["weed"])
    KEY_START_PROGRAM = data["resume_program_key"]
    KEY_STOP_PROGRAM = data["open_trunk_after_next_fishing"]
    print(str(datetime.now()) + "    Załadowano ustawienia")

if __name__ == '__main__':
    print(str(datetime.now()) + "    Rozpoczynam działanie programu...")
    global isProgramStarted
    isProgramStarted=False
    open_settings()
    while True:
        if keyboard.is_pressed(KEY_START_PROGRAM) and not isProgramStarted:
            isProgramStarted = True
            print("Włączam clickera...")
            find_isTunner()



