import cv2 as cv
from PyQt5.QtCore import pyqtSignal, QObject
import numpy as np
import gemy


lower_black = np.array([0, 0, 0])
upper_black = np.array([50, 50, 50])
kernel = np.ones((5,5), np.uint8)

def empty(img):
    pass

cv.namedWindow("TrackBar")
cv.resizeWindow("TrackBar", 600, 300)
cv.createTrackbar("thresh1", "TrackBar", 0, 255, empty)
cv.createTrackbar("thresh2", "TrackBar", 255, 255, empty)
cv.createTrackbar("Area", "TrackBar", 200, 10000, empty)


class FrameProcessor(QObject):

    frame_processed = pyqtSignal(object)
    # this is the counter that can be control the autonomous mode and can be conrolled using line follower's button 
    mode = 0  # 0 -> normal mode |  1 -> line follower |  2 -> detection mode

    def __init__(self, url):
        super().__init__()
        self.camera = cv.VideoCapture(url)



    def line_follower(self, frame):
        """line follower function turn the auto mode and let the rover track the black line"""
        gemy.sendCommand(error)
        gemy.lineFollower_auto()
        frame_crop = frame[480:, :]
        BlackLine = cv.inRange(frame_crop, lower_black, upper_black) # create the mask
        BlackLine = cv.erode(BlackLine, kernel, iterations=1) # apply some morophological operational
        BlackLine = cv.dilate(BlackLine, kernel, iterations=2)

        contoursBlk, _ = cv.findContours(BlackLine, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(contoursBlk) > 0:
            biggest_contour = max(contoursBlk, key = cv.contourArea)
            blackbox = cv.minAreaRect(biggest_contour) 
            (x_min, y_min), (w_min, h_min), ang = blackbox
            setPoint = 270 # the set point is the half of the camera's resolution = 540/2
            error = int(x_min) - setPoint # center line of the black line -  set Point
            ang = int(ang)
            
            # send the values of error and angles here

            box = cv.boxPoints(blackbox)
            box = np.int0(box)
            cv.drawContours(frame, [box], 0, (0,255,0), 2)
            cv.putText(frame, str(ang), (10, 200), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            cv.putText(frame, str(error), (10, 750), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            cv.line(frame, (int(x_min), 600), (int(x_min), 650 ), (255,0,0), 3)
            cv.line(frame, (int(x_min) , 600), (setPoint, 600), (0,255,0), 3)
    
    def get_contours(self, img, imgContour):
        """ this is a function that takes the mask and the frame and it extracts the contours from the mask and draw it in the frame"""
        contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Loop through detected contours
        for cnt in contours:
            area = cv.contourArea(cnt)
            minArea = cv.getTrackbarPos("Area", "TrackBar")
            if area > minArea:
                cv.drawContours(imgContour, cnt, -1, (0,255,0), 1)
                # Approximate the contour to a polygon
                epsilon = 0.04 * cv.arcLength(cnt, True)
                approx = cv.approxPolyDP(cnt, epsilon, True)
                print(len(approx))
                x, y, w, h = cv.boundingRect(cnt)

                if len(approx) == 4: 
                    aspect_ratio = float(w) / h
                    cv.rectangle(imgContour, (x, y), (x+w, y+h), (0,255,0), 5)
                    # cv.putText(imgContour, f"points: {approx}" ,(x+w+20, y+20), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 3)
                    cv.putText(imgContour, f"area: {cv.contourArea(cnt)}" ,(x+w+20, y+30), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 3)
                    if aspect_ratio >= 0.9 and aspect_ratio <= 1.1:
                        cv.putText(imgContour, f"Shape: Square" ,(x+w+20, y+60), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 3)
                    else:
                        cv.putText(imgContour, f"Shape: Rectangle" ,(x+w+20, y+60), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 3)

                if len(approx) == 3:
                    cv.rectangle(imgContour, (x, y), (x+w, y+h), (0,255,0), 5)
                    # cv.putText(imgContour, f"points: {approx}" ,(x+w+20, y+20), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 3)
                    cv.putText(imgContour, f"area: {cv.contourArea(cnt)}" ,(x+w+20, y+30), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 3)
                    cv.putText(imgContour, f"Shape: Triangle" ,(x+w+20, y+60), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 3)

                if len(approx) >= 7 and len(approx) <= 16:
                    cv.rectangle(imgContour, (x, y), (x+w, y+h), (0,255,0), 5)
                    cv.putText(imgContour, f"area: {cv.contourArea(cnt)}" ,(x+w+20, y+30), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 3)
                    cv.putText(imgContour, f"Shape: Circle" ,(x+w+20, y+60), cv.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 3)

    def shape_detection(self, frame):
        blur_img = cv.GaussianBlur(frame, (7,7), 2)
        gray_img = cv.cvtColor(blur_img, cv.COLOR_BGR2GRAY)

        threshold1 = cv.getTrackbarPos("thresh1", "TrackBar")
        thershold2 = cv.getTrackbarPos("thresh2", "TrackBar")
        ret, thresh = cv.threshold(gray_img, threshold1, thershold2, cv.THRESH_BINARY_INV)

        canny_img = cv.Canny(thresh, threshold1, thershold2)
        dilate = cv.dilate(canny_img, kernel, iterations=1)
        self.get_contours(dilate, frame)


    def process_frame_1(self):
        ret, frame = self.camera.read()
        if ret:
            processed_frame = cv.resize(frame, (540, 960))
            if self.mode == 1: # turn line follower mode
                self.line_follower(processed_frame)

            if self.mode == 2: # turn shape detection mode
                self.shape_detection(processed_frame)

            self.frame_processed.emit(processed_frame)

        else:
            print("there is some error happend in reading the frames")    

    # def process_frame_2(self):
    #     ret, frame = self.camera.read()
    #     if ret:
    #         processed_frame = cv.resize(frame, (540, 960))
    #         if self.mode:
    #             self.line_follower(processed_frame)

    #         self.frame_processed.emit(processed_frame)
