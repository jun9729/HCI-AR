import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
def virtual_Painter():

    brushThickness = 25
    eraserThickness = 100

    drawColor = (0, 0, 255)
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = htm.handDetector(detectionCon=0.85, maxHands=1)
    xp, yp = 0, 0
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
    while True:

        # 1. Import image
        success, img = cap.read()
        img = cv2.flip(img, 1)

        cv2.rectangle(img, (250, 0), (450, 125), (255,50,0), cv2.FILLED)
        cv2.rectangle(img, (550, 0), (750, 125), (0,0,255), cv2.FILLED)
        cv2.rectangle(img, (850, 0), (1050, 125), (0,255,0), cv2.FILLED)
        cv2.rectangle(img, (1150, 0), (1300, 125), (0,0,0), cv2.FILLED)

        # 2. Find Hand Landmarks
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            fingers = detector.fingersUp()

            if fingers[1] and fingers[2]:

                print("Selection Mode")
                if y1 < 125:
                    if 250 < x1 < 450:
                        drawColor = (255, 50, 0)
                    elif 550 < x1 < 750:
                        drawColor = (0, 0, 255)
                    elif 800 < x1 < 1050:
                        drawColor = (0, 255, 0)
                    elif 1150 < x1:
                        drawColor = (0, 0, 0)
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

            if fingers[1] and fingers[2] == False:
                print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if drawColor == (0, 0, 0):
                    cv2.circle(imgCanvas, (x1, y1), 50, drawColor,-1)
                    cv2.circle(img, (x1, y1), 50, drawColor,-1)
              
                else:
                    cv2.circle(img, (x1, y1), 15, drawColor)
                    cv2.circle(imgCanvas, (x1, y1), 15, drawColor,cv2.FILLED)

                xp, yp = x1, y1

           

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)


        cv2.imshow("Image", img)
        cv2.waitKey(1)

virtual_Painter()