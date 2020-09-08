import cv2 as cv
import numpy as np

DIGITS_COUNT = 11

def check_frame():
    img_rgb = cv.imread('img/eq1.png')
    height, width, _ = img_rgb.shape
    img_rgb = img_rgb[int(height / 2):int(height), int(width / 4):int(width * 0.66)]

    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    templates = []
    templ_shapes = []
    threshold = 0.8
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
            if(a==10):
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
    if(sequence_size>0):
        print("Znaleziono ciag o dlugosci: "+str(sequence_size))

    string_digit = ""
    for digit in list_of_digits:
        string_digit+=str(digit)

    print(string_digit)

if __name__ == '__main__':
    check_frame()
