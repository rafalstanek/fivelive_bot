# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2 as cv
import numpy as np
import keyboard
import threading
import time

import pyautogui
from pyautogui import press, typewrite, hotkey

letter_count = 4

global isSequence
isSequence = False

def check_frame(frame):
    #img_rgb = cv.imread(frame)
    img_rgb = frame

    height, width, _ = img_rgb.shape
    img_rgb = img_rgb[int(height/2):int(height*0.85), int(width/3):int(width*0.66)]
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    templates = []
    templ_shapes = []
    threshold = 0.99
    letters = [] #lista wszystkich liter w sekwencji

    for i in range(letter_count):
        templates.append(cv.imread("src/letter{}.png".format(i+1), 0))
        templ_shapes.append(templates[i].shape[::-1])

    a = 1
    for template in templates:
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        w, h = template.shape[::-1]
        #print("***nowy template***")
        for pt in zip(*loc[::-1]):
            print(pt[0])
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 0)
            letters.append([pt[0],a])
        a=a+1

    show_sequence(letters)
    #cv.imwrite('res.png', img_rgb)
    #print("Zakończono...")

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
    time.sleep(6.858)
    isSequence=False

def capture_video():
    threading.Timer(1.0, capture_video).start()
    if not isSequence:
        print("Czekam na sekwencje...")
        SCREEN_SIZE = (1920, 1080)
        fourcc = cv.VideoWriter_fourcc(*"XVID")
        # make a screenshot
        img = pyautogui.screenshot()
        # img = pyautogui.screenshot(region=(0, 0, 300, 400))
        # convert these pixels to a proper numpy array to work with OpenCV
        frame = np.array(img)
        # convert colors from BGR to RGB
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # write the frame
        # show the frame
        # cv.imshow("screenshot", frame)
        check_frame(frame)
        # if the user clicks q, it exits

        # make sure everything is closed when exited
        cv.destroyAllWindows()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Rozpoczynam działanie programu...')
    capture_video()


