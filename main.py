import cv2
import cvzone
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(detectionCon=0.8, maxHands=1)

imgBackground = cv2.imread("resources/background.png")

ModeList = []
ModeDir = "resources/Modes"

arrModeList = os.listdir(ModeDir)
for listM in arrModeList:
    img = cv2.imread(f'{ModeDir}/{listM}')
    ModeList.append(img)


listImgIcons = []
dirIcon = "resources/icons"

arriconList = os.listdir(dirIcon)
for icon in arriconList:
    img = cv2.imread(f'{dirIcon}/{icon}')
    listImgIcons.append(img)


modeType = 0
counter = 0
speed = 10
selection = -1
modePosition = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0
selectionList = [-1, -1, -1]


while True:
    _, img = cap.read()
#     img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    imgBackground[139:139+480, 50:50+640] = img
    imgBackground[0:720, 845:845+433] = ModeList[modeType]

    if hands and counterPause == 0 and modeType < 3:
        hand1 = hands[0]
        fingers = detector.fingersUp(hand1)

        if fingers == [0, 1, 0, 0, 0]:
            selection = 1
            counter += 1

        elif fingers == [0, 1, 1, 0, 0]:
            selection = 2
            counter += 1

        elif fingers == [0, 1, 1, 1, 0]:
            selection = 3
            counter += 1

        else:
            counter = 0
            selection = -1

        if selection != -1:
            cv2.ellipse(imgBackground, modePosition[selection-1],
                        (100, 100), 0, 0, counter*speed, (0, 255, 0), 10)

        if counter*speed > 360:
            selectionList[modeType] = selection

            modeType += 1
            counter = 0
            selection = -1
            counterPause = 1

    if counterPause > 0:
        # print(counterPause)
        counterPause += 1
        if counterPause > 50:
            counterPause = 0

    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 +
                      65] = listImgIcons[selectionList[0] - 1]
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 +
                      65] = listImgIcons[2+selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 +
                      65] = listImgIcons[5+selectionList[2]]

#     if selectionList[0] != -1 and selectionList[1] != -1 and selectionList[2] != -1:

#         for x, i in enumerate(range(0, 9, 3)):

#             imgBackground[636:636 + 65,
#                           (133+x*205):(133+x*205) + 65] = listImgIcons[i:][selectionList[x] - 1]


#     print(selctionChoise)

    cv2.imshow("imgBackground", imgBackground)
#     cv2.imshow("img", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
