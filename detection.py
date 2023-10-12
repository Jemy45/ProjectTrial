import cv2 as cv
from PyQt5.QtCore import pyqtSignal, QObject
url1 = 'http://192.168.220.244:8080/video'

class FrameProcessor(QObject):

    frame_processed = pyqtSignal(object)

    def __init__(self, url):
        super().__init__()
        self.camera = cv.VideoCapture(url)

    def process_frame_1(self):
        ret, frame = self.camera.read()
        
        if ret:
            # Perform some processing operations here
            processed_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # processed_frame = cv.resize(processed_frame, (381, 640))
            # print(f" 1 - {frame.shape}")
            self.frame_processed.emit(processed_frame)

    def process_frame_2(self):
        ret, frame = self.camera.read()
        
        if ret:
            # Perform some processing operations here
            processed_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            # processed_frame = cv.resize(processed_frame, (381, 640))
            # print(f" 2 - {frame.shape}")
            self.frame_processed.emit(processed_frame)
            