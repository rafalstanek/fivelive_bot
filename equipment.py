import cv2 as cv
import numpy as np
import threading
import pyautogui
from pyautogui import press

DIGITS_COUNT = 12
FISH_COUNT = 3

def check_frame():
    img_rgb = cv.imread('img/eq2.png')
    height, width, _ = img_rgb.shape
    img_rgb = img_rgb[int(height / 2):int(height), int(width / 4):int(width * 0.66)]

    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    templates = []
    templ_shapes = []
    threshold = 0.82
    letters = []

    for i in range(DIGITS_COUNT):
        templates.append(cv.imread("img/digits/{}.png".format(i), 0))
        templ_shapes.append(templates[i].shape[::-1])

    a = 0
    for template in templates:
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        w, h = template.shape[::-1]
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 0)
            if(a==10 or a==11):
                letters.append([pt[0], "/"])
            else:
                letters.append([pt[0],a])
        a=a+1

    show_sequence(letters)
    cv.imwrite('res.png', img_rgb)



def show_sequence(array):
    list_of_digits = []
    array.sort()
    index = 0
    for letter in array:
        if not(index+1<len(array) and array[index+1][0]-array[index][0] <= 5):
            list_of_digits.append(letter[1])
        index+=1
    sequence_size = len(list_of_digits)
    #if(sequence_size>0):
    #    print("Znaleziono ciag o dlugosci: "+str(sequence_size))

    string_digit = ""
    for digit in list_of_digits:
        string_digit+=str(digit)

    weights = string_digit.split("/")
    weights_array = []
    for weight in weights:
        if not weight == '':
            weight_float = 0.00
            weight_string = ""
            if len(weight) == 3:
                weight_string=weight[0]+"."+weight[1]+weight[2]
            else:
                weight_string = weight[0] + weight[1]+ "." + weight[2] + weight[3]
            weight_float = float(weight_string)
            weights_array.append(weight_float)

    if len(weights_array)==4:
        print(weights_array)
    else:
        print("[ERROR]Nie udalo sie odczytac pojemnosci przedmiotow")

def find_fish(frame):
    #img_rgb = cv.imread('img/eq1.png')
    img_rgb = frame
    height, width, _ = img_rgb.shape

    cv.rectangle(img_rgb, (0,0), (width, int(height / 4)), (255, 255, 255), -1)
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

    if fish_point:
        print("JEST RYBA DO PRZENIESIENIA "+str(len(fish_point))+str(fish_point))
    else:
        print("Nie ma ryby")

    cv.imwrite('fish.png', img_rgb)

def capture_video():
    threading.Timer(1.0, capture_video).start()
    print("Szukam ryby...")
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    find_fish(frame)
    cv.destroyAllWindows()

if __name__ == '__main__':
    #check_frame()
    #find_fish()
    capture_video()
