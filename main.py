import json
import cv2 as cv
import numpy as np
import threading
import time
import sys
import keyboard
import random
from datetime import datetime
from playsound import playsound

import pyautogui
from pyautogui import press

LETTER_COUNT = 4
DIGITS_COUNT = 12
FISH_COUNT = 3

#sprawdzic przy otwarciu bagaznika ile zostalo pojemnosci, jesli mniej niż ileś to go nie otwierać

global isSequence, isMouseMove, thread, isTrunk, trunkCounter, isProgramRun
isSequence = False
isMouseMove = False
isTrunk = False
isProgramRun = True
trunkCounter = 0

def check_frame(frame):
    img_rgb = frame

    height, width, _ = img_rgb.shape
    img_rgb = img_rgb[int(height/2):int(height*0.85), int(width/3):int(width*0.66)]
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    templates = []
    templ_shapes = []
    threshold = 0.99
    letters = []

    for i in range(LETTER_COUNT):
        templates.append(cv.imread("img/letter{}.png".format(i+1), 0))
        templ_shapes.append(templates[i].shape[::-1])

    a = 1
    for template in templates:
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        w, h = template.shape[::-1]
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 0)
            letters.append([pt[0],a])
        a=a+1

    show_sequence(letters)

def show_sequence(array):
    array.sort()
    sequence_size = len(array)
    if(sequence_size>0):
        print(str(datetime.now())+"    Znaleziono sekwencję o dlugosci: "+str(sequence_size)+" znaków")
        global isSequence
        isSequence = True
        press_sequence(array)


def press_sequence(array):
    waitRandom = random.uniform(0.800, 1.90)
    time.sleep(waitRandom)
    print(str(datetime.now())+"    Wciskam sekwencje...")
    global isSequence, isTrunk, trunkCounter
    sequence_str = ""
    for letter in array:
        time.sleep(random.uniform(TIME_MIN, TIME_MAX))
        if letter[1]==1:
            press("a")
            sequence_str+="a "
        elif letter[1]==2:
            press("w")
            sequence_str += "w "
        elif letter[1]==3:
            press("d")
            sequence_str += "d "
        elif letter[1]==4:
            press("s")
            sequence_str += "s "
    print(str(datetime.now())+"    Wpisano sekwencje: "+str(sequence_str))
    waitRandom = random.uniform(TIME_Z_MIN, TIME_Z_MAX)
    print(str(datetime.now())+"    Rozpoczynam kolejny połów za: "+str(waitRandom)+" sekund")
    time.sleep(waitRandom)
    trunkCounter = trunkCounter - 1
    if(trunkCounter==0):
        press("e")
        print(str(datetime.now())+"    Otwieram bagażnik")
        time.sleep(2)
        isTrunk = True
    elif(trunkCounter<0):
        press("z")
        time.sleep(random.uniform(1.3, 3.7))
        isSequence = False
        print(str(datetime.now()) + "    Otwieranie bagażnika zostało wyłączone")
    else:
        press("z")
        time.sleep(random.uniform(1.3, 3.7))
        isSequence = False
        print(str(datetime.now()) + "    Bagażnik otworzy się za "+str(trunkCounter)+" połowów")

def find_fish(frame):
    img_rgb = frame
    height, width, _ = img_rgb.shape
    cv.rectangle(img_rgb, (0, 0), (int(width/4), height), (255, 255, 255), -1)
    cv.rectangle(img_rgb, (int(width/2), 0), (width,height), (255, 255, 255), -1)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    templates = []
    templ_shapes = []
    threshold = 0.99
    fish_point = []

    for i in range(FISH_COUNT):
        templates.append(cv.imread("img/fishes/{}.png".format(i+1), 0))
        templ_shapes.append(templates[i].shape[::-1])

    for template in templates:
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        w, h = template.shape[::-1]
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 0)
            fish_point.append((pt[0], pt[1]))

    cv.destroyAllWindows()
    if fish_point:
        fish_point.sort()
        return fish_point
    else:
        return None

def drag_drop(fishes, screen_width):
    global isMouseMove, isTrunk, trunkCounter, isSequence
    for index, fish in enumerate(fishes):
        cv.destroyAllWindows()
        pyautogui.moveTo(fish[0], fish[1], random.uniform(0.100, 0.150))
        time.sleep(random.uniform(0.1, 0.150))
        pyautogui.dragTo(screen_width - fish[0], fish[1], random.uniform(DRAG_INTERVAL_MIN, DRAG_INTERVAL_MAX))
        time.sleep(random.uniform(0.1, 0.150))
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        fish_array = find_fish(frame)
        if fish_array == None:
            print(str(datetime.now())+"    Nie ma wiecej ryb w bagażniku")
            press("e")
            print(str(datetime.now()) + "  Zamykam bagażnik, bo jesty pusty (drag_drop)")
            time.sleep(0.2)
            isMouseMove = False
            isTrunk = False
            trunkCounter = random.randint(TRUNK_MOVE_MIN, TRUNK_MOVE_MAX)
            print(str(datetime.now())+"    Kolejne otwarcie bagażnika nastąpi po " + str(trunkCounter)+" połowach ryba")
            time.sleep(random.uniform(0.8, 1.3))
            press("z")
            isSequence = False
            break
        elif(len(fish_array) == len(fishes)):
            cv.destroyAllWindows()
            print(str(datetime.now())+"    Ryba nie zmiesci sie do bagaznika")
            playsound("sounds/sound.mp3")
            if(len(fish_array)-1 == index):
                press("e")
                print(str(datetime.now()) + "  Zamykam bagażnik, bo nie ma miejsca w samochodzie")
                time.sleep(0.2)
                isMouseMove = False
                isTrunk = False
                trunkCounter = random.randint(TRUNK_MOVE_MIN, TRUNK_MOVE_MAX)
                print(str(datetime.now()) + "    Kolejne otwarcie bagażnika nastąpi po " + str(
                    trunkCounter) + " połowach ryba")
                time.sleep(random.uniform(0.8, 1.3))
                press("z")
                isSequence = False
                break
        else:
            print(str(datetime.now())+"    Przeniesiono rybę do bagażnika")
            drag_drop(fish_array, screen_width)
            break


def capture_video():
    global thread, isMouseMove, isTrunk, trunkCounter, isSequence
    thread = threading.Timer(1.0, capture_video)
    thread.start()
    if not isSequence and not isMouseMove and not isTrunk:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        check_frame(frame)

    if isTrunk and not isMouseMove:
        isMouseMove = True
        print(str(datetime.now())+"    Szukam ryby w bagażniku...")
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        fish = find_fish(frame)
        if fish:
            print(str(datetime.now())+"    Znaleziono rybe/y: "+str(len(fish)))
            drag_drop(fish, width)
        else:
            if isTrunk:
                press("e")
                print(str(datetime.now())+"    Zamykam bagażnik, bo jest pusty")
                time.sleep(0.2)
                isMouseMove = False
                isTrunk = False
                trunkCounter = random.randint(TRUNK_MOVE_MIN, TRUNK_MOVE_MAX)
                print(str(datetime.now()) + "   Kolejne otwarcie bagażnika nastąpi po " + str(
                    trunkCounter) + " połowach ryba")
                time.sleep(random.uniform(0.8, 1.3))
                press("z")
                isSequence = False

        cv.destroyAllWindows()
    cv.destroyAllWindows()

def open_settings():
    print(str(datetime.now()) + "    Ładowanie ustawień użytkownika")
    with open('settings.json') as f:
        data = json.load(f)
    global TRUNK_MOVE_MAX, TRUNK_MOVE_MIN, TIME_Z_MIN, TIME_Z_MAX, TIME_MIN, TIME_MAX, KEY_STOP, KEY_TRUNK, KEY_STOP_OPEN_TRUNK, DRAG_INTERVAL_MIN, DRAG_INTERVAL_MAX
    TIME_MIN = float(data["time_interval_min"])
    TIME_MAX = float(data["time_interval_max"])
    TIME_Z_MIN = float(data["press_z_min"])
    TIME_Z_MAX = float(data["press_z_max"])
    TRUNK_MOVE_MIN = int(data["open_trunk_min"])
    TRUNK_MOVE_MAX = int(data["open_trunk_max"])
    KEY_STOP = data["resume_program_key"]
    KEY_TRUNK = data["open_trunk_after_next_fishing"]
    KEY_STOP_OPEN_TRUNK = data["stop_open_trunk"]
    DRAG_INTERVAL_MIN = float(data["drag_interval_min"])
    DRAG_INTERVAL_MAX = float(data["drag_interval_max"])

if __name__ == '__main__':
    print(str(datetime.now())+"    Rozpoczynam działanie programu")
    try:
        open_settings()
    except:
        print(str(datetime.now()) + "    Nie udało się załadować ustawień użytkownika. Wczytano ustawienia domyślne.")
        TIME_MIN = 0.120
        TIME_MAX = 0.300
        TIME_Z_MIN = 7.5
        TIME_Z_MAX = 10.5
        TRUNK_MOVE_MIN = 4
        TRUNK_MOVE_MAX = 7
        KEY_STOP = "f9"
        KEY_TRUNK = "f10"
        KEY_STOP_OPEN_TRUNK = "f11"
        DRAG_INTERVAL_MIN = 0.100
        DRAG_INTERVAL_MAX = 0.150
    else:
        print(str(datetime.now()) + "    Załadowano ustawienia")

    trunkCounter = random.randint(TRUNK_MOVE_MIN,TRUNK_MOVE_MAX)
    print(str(datetime.now())+"    Pierwsze użycie bagażnika nastąpi po "+str(trunkCounter)+" połowach ryb")
    capture_video()
    while True:
        if keyboard.is_pressed(KEY_STOP):
            if isProgramRun:
                isProgramRun = False
                if(not isSequence):
                    global thread
                    thread.cancel()
                    if not isSequence and not isMouseMove and not isTrunk:
                        press("z")
                    if isTrunk:
                        press("e")

                    isMouseMove = False
                    isTrunk = False
                    isSequence = False
                    print(str(datetime.now()) + "    Wstrzymano działanie programu")
                    isProgramRun=False
                else:
                    isProgramRun = True
            else:
                print(str(datetime.now()) + "    Wznawiono działanie programu")
                trunkCounter = random.randint(TRUNK_MOVE_MIN, TRUNK_MOVE_MAX)
                print(str(datetime.now()) + "    Pierwsze użycie bagażnika nastąpi po " + str(
                    trunkCounter) + " połowach ryb")
                press("z")
                capture_video()
                isProgramRun=True
                isSequence = False
                isMouseMove = False
                isTrunk = False
            time.sleep(0.1)
        if keyboard.is_pressed(KEY_TRUNK) and not trunkCounter==1:
            trunkCounter=1
            print(str(datetime.now()) + "    Aktywowano uruchomienie bagażnika po kolejnym połowie")
        if keyboard.is_pressed(KEY_STOP_OPEN_TRUNK) and trunkCounter>=0:
            trunkCounter=-1
            print(str(datetime.now()) + "    Przerwano automatyczne otwieranie bagażnika")




