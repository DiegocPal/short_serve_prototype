import cv2
import numpy as np
import os
import glob
from hsv import *
import tkinter as tk
from tkinter import filedialog
from messages import *
from line import *

def file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def main(path_lateral, path_up, l_limit, h_limit):
    if os.path.exists('./images/img_up_alt.png'):
        os.remove('./images/img_up_alt.png')

    if os.path.exists('./images/line_up.png'):
        os.remove('./images/line_up.png')

    if os.path.exists('./images/line_lateral.png'):
        os.remove('./images/line_lateral.png')

    if os.path.exists('./images/img_lateral.png'):
        os.remove('./images/img_lateral.png')

    if os.path.exists('./images/img_up.png'):
        os.remove('./images/img_up.png')

    paths = glob.glob('./images/f*.png')
    for path in paths:
        os.remove(path)

    output = hsv(path_lateral, l_limit, h_limit)

    x = output[0]
    y = output[1]
    p_frame = output[2]
    img_frames = output[3]

    if len(x) == 0:
        warn4()
        img = './images/error.png'
        output = np.array([img, img, 0, 0, 0, 0, 0, 0], dtype=object)
        return output
    else:
        #Se determina la posición del punto más bajo detectado en el array de numpy y
        ymin_pos = np.where(y == np.amax(y))
        xmin = int(x[ymin_pos])
        ymin = int(y[ymin_pos])
        i_frame = int(p_frame[ymin_pos])
        #Se extrae el frame de impacto de la camara lateral
        frame_path = str(img_frames[ymin_pos][0])
        img_lateral = cv2.imread(frame_path)

        cv2.imwrite('./images/img_lateral.png', img_lateral)
        img_lateral = './images/img_lateral.png'
        img_lateral = cv2.imread(img_lateral)

        # Se extrae el frame del punto de impacto de la camara superior
        cap = cv2.VideoCapture(path_up)
        up_frame = i_frame - 1
        cap.set(1, up_frame)
        ret, superior_frame = cap.read()

        cv2.imwrite('./images/img_up.png', superior_frame)
        img_up_path = './images/img_up.png'
        img_up = cv2.imread(img_up_path)
        cap.release()

        #Se extrae el frame lateral para determinar las coordenadas de la línea
        cap = cv2.VideoCapture(path_lateral)
        cap.set(1, 5)
        ret, line_lateral_img = cap.read()
        cv2.imwrite('./images/line_lateral.png', line_lateral_img)
        line_lateral_img = './images/line_lateral.png'
        line_lateral_img = cv2.imread(line_lateral_img)
        cap.release()

        #Evaluar la falta a traves de la imagen lateral
        line_lateral = line_segmentation_lateral(line_lateral_img)

        points_lateral = points_detection_lateral(line_lateral)

        x1l = points_lateral[0]
        y1l = points_lateral[1]
        x2l = points_lateral[2]
        y2l = points_lateral[3]

        m = (y2l - y1l) / (x2l - x1l)
        xline = int((y[ymin_pos] - y1l) / m + x1l)

        x1show = int((0 - y1l) / m + x1l)
        height = img_lateral.shape[0]
        x2show = int((height - y1l)/m + x1l)

        des = None
        if xline > xmin:
            des = str('NO FAULT')
        elif xline < xmin:
            des = str('FAULT')

        points = [x1l, y1l, x2l, y2l]

        # Se dibuja la línea y la pelota en la imagen lateral
        img_lateral = cv2.line(img_lateral, (x1show, 0), (x2show, height), (0, 255, 0), 2)
        img_lateral = cv2.circle(img_lateral, (xmin, ymin), 50, (0, 0, 255), 2)

        cv2.imwrite('./images/img_lateral.png', img_lateral)
        img_lateral = './images/img_lateral.png'

        # Se extrae el frame superior para determinar las coordenadas de la línea
        cap = cv2.VideoCapture(path_up)
        cap.set(1, 5)
        ret, line_up_img = cap.read()
        cv2.imwrite('./images/line_up.png', line_up_img)
        line_up_img = './images/line_up.png'
        line_up_img = cv2.imread(line_up_img)
        cap.release()

        if des == None:
            ball_point = hsv_up(img_up, l_limit, h_limit)

            xmin = ball_point[0]

            line = line_segmentation_up(img_up)
            points = points_detection_up(line)

            x1 = points[0]
            y1 = points[1]

            x2 = points[2]
            y2 = points[3]

            m = (y2 - y1) / (x2 - x1)
            xline = int((y[ymin_pos]-y1)/m + x1)

            if xline > xmin:
                des = str('NO FAULT')
            elif xline < xmin:
                des = str('FAULT')

            points = [x1, y1, x2, y2]


        # Se extrae el frame superior para determinar las coordenadas de la línea
        cap = cv2.VideoCapture(path_up)
        cap.set(1, 5)
        ret, line_up_img = cap.read()
        cv2.imwrite('./images/line_up.png', line_up_img)
        line_up_img = './images/line_up.png'
        line_up_img = cv2.imread(line_up_img)
        cap.release()

        # Se extraen las coordenadas de la línea superior
        line_up = line_segmentation_up(line_up_img)

        points_up = points_detection_up(line_up)

        x1u = points_up[0]
        y1u = points_up[1]
        x2u = points_up[2]
        y2u = points_up[3]

        m = (y2u - y1u) / (x2u - x1u)
        xline = int((y[ymin_pos] - y1u) / m + x1u)

        x1show_up = int((0 - y1u) / m + x1u)
        height_up = line_up_img.shape[0]
        x2show_up = int((height - y1u) / m + x1u)

        #Se determinan las coordenadas de la pelota en la imagen superior
        #coordinates_up = hsv_up(path_up, l_limit, h_limit, i_frame)
        #x_up = coordinates_up[0]
        #y_up = coordinates_up[1]

        img_up = cv2.line(img_up, (x1show_up, 0), (x2show_up, height_up), (0, 255, 0), 2)
        #if coordinates_up != [0, 0]:
            #img_up = cv2.circle(img_up, (x_up, y_up), 50, (0, 0, 255), 2)

        cv2.imwrite('./images/img_up.png', img_up)
        img_up = './images/img_up.png'

        output = np.array([img_up, img_lateral, des, points], dtype = object)
        return output