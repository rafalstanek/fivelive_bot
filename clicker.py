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

global WEED_COUNT, KEY_START_PROGRAM, KEY_STOP_PROGRAM, isProgramStarted

def find_button_position():
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    height, width, _ = frame.shape
    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    threshold = 0.99
    template = cv.imread("img/weed.png",0)
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    w, h = template.shape[::-1]
    posX = -1
    posY = -1
    for pt in zip(*loc[::-1]):
        cv.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 0)
        posX = pt[0]+int(w/2)
        posY = pt[1]+int(h/2)

    global isProgramStared

    if(posX > -1 and posY >-1):
        click_button(posX, posY, WEED_COUNT)
        isProgramStared = True
    else:
        isProgramStared=False
        print("Wejdź w pole 'Tworzenie' i uruchom program")

def click_button(posX, posY, weed_count):
    counter = int(weed_count/2)
    global WEED_COUNT
    while(isProgramStared and counter>0):
        posX_offset = random.randint(-5,5)
        posY_offset = random.randint(-3,3)
        pyautogui.moveTo(posX+posX_offset,posY+posY_offset,0)
        pyautogui.click()
        time.sleep(random.uniform(5.5, 5.9))
        counter-=1
        WEED_COUNT = counter

def open_settings():
    print(str(datetime.now()) + "    Ładowanie ustawień użytkownika...")
    with open('settings.json') as f:
        data = json.load(f)
    global WEED_COUNT, KEY_START_PROGRAM, KEY_STOP_PROGRAM
    WEED_COUNT = float(data["weed"])
    KEY_START_PROGRAM = data["stop_program_key"]
    KEY_STOP_PROGRAM = data["open_trunk_after_next_fishing"]
    print(str(datetime.now()) + "    Załadowano ustawienia")

if __name__ == '__main__':
    print(str(datetime.now()) + "    Rozpoczynam działanie programu...")
    global isProgramStarted
    isProgramStared=False
    open_settings()
    while True:
        if keyboard.is_pressed(KEY_START_PROGRAM) and not isProgramStared:
            isProgramStared = True
            print("Włączam clickera...")
            find_button_position()
        if isProgramStared and keyboard.is_pressed("]"):
            print("Wyłączam clickera...")
            isProgramStared = False



