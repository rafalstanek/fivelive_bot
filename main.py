# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def check_frame():
    img_rgb = cv.imread('long.png')
    height, width, _ = img_rgb.shape
    img_rgb = img_rgb[int(height/2):int(height*0.85), int(width/3):int(width*0.66)]
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('src/w.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    cv.imwrite('res.png', img_rgb)
    print("Znaleziono...")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    check_frame()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
