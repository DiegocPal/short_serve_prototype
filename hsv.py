import cv2
import numpy as np
from messages import *

def hsv(path, l_hsv, h_hsv):
    list = []
    x = np.array(list)
    y = np.array(list)
    p_frame = np.array(list)
    img_frame_path = np.array(list)

    cap = cv2.VideoCapture(path)
    t_frames = cap.get(7)

    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            i = i + 1

            f_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(f_hsv, l_hsv, h_hsv)
            mask = cv2.bitwise_not(mask)
            mask = cv2.GaussianBlur(mask, (15, 15), cv2.BORDER_DEFAULT)

            #Definir los parametros para el detector de blobs
            params = cv2.SimpleBlobDetector_Params()

            #Filtro por area
            params.filterByArea = True
            params.minArea = 1000
            params.maxArea = 100000

            # Filtro por circunferencia
            params.filterByCircularity = True
            params.minCircularity = 0.1

            params.filterByColor = True
            params.blobColor = 0

            params.filterByConvexity = True
            params.minConvexity = 0.01

            # Set up the detector with default parameters.
            detector = cv2.SimpleBlobDetector_create(params)

            # Detect blobs.
            keypoints = detector.detect(mask)

            if len(keypoints) == 1:
                x = np.append(x, keypoints[0].pt[0])
                y = np.append(y, keypoints[0].pt[1])
                p_frame = np.append(p_frame, i)
                path = './images/f' + str(i) + '.png'
                cv2.imwrite(path, frame)
                img_frame_path = np.append(img_frame_path, path)
        else:
            break

    cap.release()

    output = np.array([x, y, p_frame, img_frame_path], dtype=object)
    return output

def hsv_up(path_up, l_hsv, h_hsv, i_frame):
    cap = cv2.VideoCapture(path_up)
    cap.set(1, i_frame)
    ret, superior_frame = cap.read()

    cv2.imwrite('./images/img_up_alt.png', superior_frame)
    img_up_path = './images/img_up_alt.png'
    img_up = cv2.imread(img_up_path)
    cap.release()

    f_hsv = cv2.cvtColor(img_up, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(f_hsv, l_hsv, h_hsv)
    mask = cv2.bitwise_not(mask)
    mask = cv2.GaussianBlur(mask, (15, 15), cv2.BORDER_DEFAULT)

    # Definir los parametros para el detector de blobs
    params = cv2.SimpleBlobDetector_Params()

    # Filtro por area
    params.filterByArea = True
    params.minArea = 5000
    params.maxArea = 100000

    # Filtro por circunferencia
    params.filterByCircularity = True
    params.minCircularity = 0.1

    #Filtro por color
    params.filterByColor = True
    params.blobColor = 0

    #Filtro por grado de convexión
    params.filterByConvexity = True
    params.minConvexity = 0.01

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs
    keypoints = detector.detect(mask)

    x = 0
    y = 0

    if len(keypoints) == 1:
        x =  keypoints[0].pt[0]
        y =  keypoints[0].pt[1]

    output = [x, y]
    return output