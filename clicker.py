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

global WEED_COUNT, KEY_START_PROGRAM, KEY_STOP_PROGRAM

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

    global isProgramStarted
    if(posX > -1 and posY >-1):
        isProgramStarted = True
        click_button(posX, posY, WEED_COUNT)
    else:
        isProgramStarted=False
        print(str(datetime.now()) + "    Wejdź w pole 'Tworzenie' i uruchom program")
        time.sleep(0.500)

def click_button(posX, posY, weed_count):
    counter = int(weed_count/2)
    print(str(datetime.now()) + "    Rozpoczęto proces suszenia, po którym otrzymasz "+str(counter)+" suszu...")
    global WEED_COUNT, isProgramStarted
    start = time.perf_counter()
    time_interval = random.uniform(5.5, 5.9)
    isProgramEndedByUser = False
    while(isProgramStarted and counter > 0):
        if (time.perf_counter()-start>time_interval):
            print("CLICK")
            posX_offset = random.randint(-5,5)
            posY_offset = random.randint(-3,3)
            pyautogui.moveTo(posX+posX_offset,posY+posY_offset,0)
            pyautogui.click()
            start = time.perf_counter()
            counter-=1
            WEED_COUNT = counter
            if(counter==2): #w settingsach kiedy warning
                playsound("sounds/sound.mp3")
        if (keyboard.is_pressed("f10")):
            isProgramEndedByUser=True
            break
    isProgramStarted = False
    if(isProgramEndedByUser):
        print(str(datetime.now()) + "    Zatrzymano program, aby uruchomić ponownie kliknij F9")
    else:
        print(str(datetime.now()) + "    Wysuszono wszystkie plony, aby rozpocząć ponownie klknij F9.")

def open_settings():
    try:
        print(str(datetime.now()) + "    Ładowanie ustawień użytkownika...")
        with open('settings.json') as f:
            data = json.load(f)
        global WEED_COUNT, KEY_START_PROGRAM, KEY_STOP_PROGRAM
        WEED_COUNT = float(data["weed"])
        KEY_START_PROGRAM = data["resume_program_key"]
        KEY_STOP_PROGRAM = data["open_trunk_after_next_fishing"]
    except:
        print(str(
            datetime.now()) + "    Nie udało się załadować ustawień użytkownika. Sprawdź, czy posiadasz plik 'settings.json'.")
    else:
        print(str(datetime.now()) + "    Załadowano ustawienia")

if __name__ == '__main__':
    print(str(datetime.now()) + "    Rozpoczynam działanie programu...")
    pyautogui.FAILSAFE = False
    global isProgramStarted
    isProgramStarted=False
    open_settings()
    while True:
        if (keyboard.is_pressed(KEY_START_PROGRAM)) and (not isProgramStarted):
            isProgramStarted = True
            open_settings()
            find_button_position()






