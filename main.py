#press Z po przeniesieniu w bagazniku
#otwieranie bagaznika co losowy połów
#settings

import cv2 as cv
import numpy as np
import threading
import time
import sys
import keyboard
import random
from datetime import datetime

import pyautogui
from pyautogui import press

LETTER_COUNT = 4
DIGITS_COUNT = 12
FISH_COUNT = 3

TIME_MIN = 0.120
TIME_MAX = 0.300
TIME_Z_MIN = 7.5
TIME_Z_MAX = 10.5


global isSequence, isMouseMove, thread, isTrunk, useAutoTrunk
isSequence = False
isMouseMove = False
isTrunk = False
useAutoTrunk = False

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
        print("Znaleziono ciag o dlugosci: "+str(sequence_size))
        global isSequence
        isSequence = True
        press_sequence(array)


def press_sequence(array):
    print("Wciskam sekwencje")
    global isSequence, isTrunk
    for letter in array:
        time.sleep(random.uniform(TIME_MIN, TIME_MAX))
        if letter[1]==1:
            press("a")
            print("a")
        elif letter[1]==2:
            press("w")
            print("w")
        elif letter[1]==3:
            press("d")
            print("d")
        elif letter[1]==4:
            press("s")
            print("s")
    waitRandom = random.uniform(TIME_Z_MIN, TIME_Z_MAX)
    print("Klikam Z za sekund: "+str(waitRandom))
    time.sleep(waitRandom)
    press("z")
    time.sleep(random.uniform(1.3, 3.7))
    isSequence=False
    press("e")
    print("Otwieram bagażnik")
    time.sleep(2)
    isTrunk = True

def find_fish(frame):
    img_rgb = frame
    height, width, _ = img_rgb.shape
    cv.rectangle(img_rgb, (0, 0), (width, int(height / 4)), (255, 255, 255), -1)
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
    #time_random = random.uniform(2.0, 2.5)
    #time.sleep(time_random)
    #print("wchodze do drag_drop po sekundach: "+str(time_random))
    global isMouseMove, isTrunk
    for fish in fishes:
        cv.destroyAllWindows()
        #time.sleep(random.uniform(0.1, 0.15))
        pyautogui.moveTo(fish[0], fish[1], random.uniform(0.100, 0.150))
        time.sleep(random.uniform(0.1, 0.150))
        pyautogui.dragTo(screen_width - fish[0], fish[1], random.uniform(0.100, 0.150))
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        fish_array = find_fish(frame)
        if fish_array == None:
            print(str(datetime.now())+"|Nie ma wiecej ryb")
            press("e")
            print(str(datetime.now()) + "|Zamykam bagażnik, bo jesty pusty (drag_drop)")
            time.sleep(0.2)
            isMouseMove = False
            isTrunk = False
            break
        elif(len(fish_array) == len(fishes)):
            cv.destroyAllWindows()
            print("Ta ryba nie zmiesci sie do bagaznika")
        else:
            print(str(datetime.now())+"|Ryba przeniesiona do bagaznika")
            drag_drop(fish_array, screen_width)
            break


def capture_video():
    global thread, isMouseMove, isTrunk
    thread = threading.Timer(1.0, capture_video)
    thread.start()
    if not isSequence and not isMouseMove and not isTrunk:
        #print("Czekam na sekwencje...")
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        check_frame(frame)

    if isTrunk and not isMouseMove:
        isMouseMove = True
        print(str(datetime.now())+"|Szukam ryby...")
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        fish = find_fish(frame)
        if fish:
            print(str(datetime.now())+"|Znaleziono rybe/y: "+str(len(fish)))
            drag_drop(fish, width)
        else:
            if isTrunk:
                press("e")
                print(str(datetime.now())+"|Zamykam bagażnik, bo jest pusty")
                isMouseMove = False
                isTrunk = False

        cv.destroyAllWindows()
    cv.destroyAllWindows()

if __name__ == '__main__':
    print(str(datetime.now())+"|Rozpoczynam działanie programu...")
    capture_video()
    while True:
        if keyboard.is_pressed('f9'):
            global thread
            thread.cancel()
            sys.exit(0)
            quit()



