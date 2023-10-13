import cv2
import numpy as np

def line_segmentation_lateral(img):
    f_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    l_red = (170, 30, 30)
    h_red = (190, 255, 255)

    mask = cv2.inRange(f_hsv, l_red, h_red)
    #mask = cv2.GaussianBlur(mask, (15, 15), cv2.BORDER_DEFAULT)

    return mask

def line_segmentation_up(img):
    f_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    l_red = (170, 100, 100)
    h_red = (190, 255, 255)

    mask = cv2.inRange(f_hsv, l_red, h_red)
    #mask = cv2.GaussianBlur(mask, (15, 15), cv2.BORDER_DEFAULT)

    return mask


def points_detection_lateral(img):
    height = img.shape[0]
    width =  img.shape[1]

    i = height - 200
    j = 0
    sw = True
    while(sw):
        while(i < height):
            while(j < width):
                if img[i][j] == 255:
                    sw = False
                    x1 = j
                    y1 = i
                    break
                j = j + 1
            if sw == False:
                break
            i = i - 1
            j = 0

    i = height - 50
    j = 0
    sw = True
    while (sw):
        while (i > 0):
            while (j < width):
                #print(str(j) + ':' + str(i))
                if img[i][j] == 255:
                    sw = False
                    x2 = j
                    y2 = i
                    break
                j = j + 1
            if sw == False:
                break
            i = i - 1
            j = 0

    output = np.array([x1, y1, x2, y2], dtype=object)
    return output


def points_detection_up(img):
    height = img.shape[0]
    width =  img.shape[1]

    i = 10
    j = 0
    sw = True
    while(sw):
        while(i < height):
            while(j < width):
                if img[i][j] == 255:
                    sw = False
                    x1 = j
                    y1 = i
                    break
                j = j + 1
            if sw == False:
                break
            i = i + 1
            j = 0

    i = height - 10
    j = 0
    sw = True
    while (sw):
        while (i > 0):
            while (j < width):
                #print(str(j) + ':' + str(i))
                if img[i][j] == 255:
                    sw = False
                    x2 = j
                    y2 = i
                    break
                j = j + 1
            if sw == False:
                break
            i = i - 1
            j = 0

    output = np.array([x1, y1, x2, y2], dtype=object)
    return output