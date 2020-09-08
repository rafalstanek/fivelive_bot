# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os, os.path

letter_count = 3

def check_frame():
    img_rgb = cv.imread('sekwencja.png')

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
            #print(pt[0])
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 0)
            letters.append([pt[0],a])
        a=a+1

    show_sequence(letters)
    cv.imwrite('res.png', img_rgb)
    print("Zakończono...")

def show_sequence(array):
    array.sort()
    for letter in array:

        print(letter[1])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    check_frame()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
