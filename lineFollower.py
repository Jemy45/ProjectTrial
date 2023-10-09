import cv2 as cv
import numpy as np

url2 = 'http://192.168.128.173:8080/video'

cap2 = cv.VideoCapture(url2)
cap2.set(cv.CAP_PROP_FPS, 30)


lower_black = np.array([0, 0, 0])
upper_black = np.array([50, 50, 50])
while True:
    ret2, frame2 = cap2.read()
    # frame2_copy = frame2.copy()
    frame2 = cv.resize(frame2, (960, 540))

    BlackLine = cv.inRange(frame2, lower_black, upper_black) # create the mask
    kernel = np.ones((5,5), np.uint8)
    BlackLine = cv.erode(BlackLine, kernel, iterations=1) # apply some morophological operational
    BlackLine = cv.dilate(BlackLine, kernel, iterations=2)

    contoursBlk, hierarchyBlk = cv.findContours(BlackLine, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contoursBlk) > 0:
        biggest_contour = max(contoursBlk, key = cv.contourArea)
        blackbox = cv.minAreaRect(biggest_contour) 
        (x_min, y_min), (w_min, h_min), ang = blackbox
        setPoint = 480 # the set point is the half of the camera's resolution = 960/2
        error = int(x_min) - setPoint # center line of the black line -  set Point
        ang = int(ang)
        
        # send the values of error and angles here

        box = cv.boxPoints(blackbox)
        box = np.int0(box)
        cv.drawContours(frame2, [box], 0, (0,255,0), 2)
        cv.putText(frame2, str(ang), (10, 40), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        cv.putText(frame2, str(error), (10, 500), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        cv.line(frame2, (int(x_min), 200), (int(x_min), 250 ), (255,0,0), 3)
        cv.line(frame2, (int(x_min) , 200), (setPoint, 200), (0,255,0), 3)
        
        cv.imshow("mask", BlackLine)
        cv.imshow("result", frame2)

        if cv.waitKey(1) == 27:
            break

cap2.release()
cv.destroyAllWindows()