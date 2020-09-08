import cv2 as cv
import numpy as np
import threading
import time
import random

import pyautogui
from pyautogui import press, typewrite, hotkey

letter_count = 4

global isSequence
isSequence = False

def check_frame(frame):
    img_rgb = frame

    height, width, _ = img_rgb.shape
    img_rgb = img_rgb[int(height/2):int(height*0.85), int(width/3):int(width*0.66)]
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    templates = []
    templ_shapes = []
    threshold = 0.99
    letters = []

    for i in range(letter_count):
        templates.append(cv.imread("src/letter{}.png".format(i+1), 0))
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
    global isSequence
    for letter in array:
        time.sleep(random.uniform(0.3, 0.9))
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
    waitRandom = random.uniform(8.5, 10.9)
    print("Klikam Z za sekund: "+str(waitRandom))
    time.sleep(waitRandom)
    press("z")
    isSequence=False

def capture_video():
    threading.Timer(1.0, capture_video).start()
    if not isSequence:
        print("Czekam na sekwencje...")
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        check_frame(frame)
        cv.destroyAllWindows()


if __name__ == '__main__':
    print('Rozpoczynam działanie programu...')
    capture_video()


