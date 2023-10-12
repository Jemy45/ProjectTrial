import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from os import path
import cv2 as cv
from detection import FrameProcessor

url1 = 'http://192.168.220.244:8080/video'
url2 = 'http://192.168.220.220:8080/video'

class MYGUI(QMainWindow):
    
    def __init__(self):
        super(MYGUI, self).__init__()

        self.setWindowTitle("Rover_GUI")

        loadUi(path.join(path.dirname(__file__), "Rover_GUI.ui"), self)
        # loadUi("Rover_GUI.ui", self)

        # Find the QLabel widgets created in Qt Designer 
        self.video_label_1 = self.findChild(QLabel, "camera1_label")
        self.video_label_2 = self.findChild(QLabel, "camera2_label")
        
        # Create FrameProcessor instances for each camera
        # self.frame_processor_1 = FrameProcessor()
        self.frame_processor_2 = FrameProcessor(0)

        # Connect the frame_processed signals to update methods
        # self.frame_processor_1.frame_processed.connect(self.update_frame_1)
        self.frame_processor_2.frame_processed.connect(self.update_frame_2)
        
        # Create timers to start processing frames for each camer
        # self.timer_camera1 = QTimer(self)
        self.timer_camera2 = QTimer(self)

        # self.timer_camera1.timeout.connect(self.frame_processor_1.process_frame_1)
        self.timer_camera2.timeout.connect(self.frame_processor_2.process_frame_2)
        
        # self.timer_camera1.start(30)  # Update the frame every 30 milliseconds for camera 1
        self.timer_camera2.start(30)  # Update the frame every 30 milliseconds for camera 2

        self.show()

        # self.pushButton.clicked.connect(self.send)
        self.actionclose.triggered.connect(exit)

    def update_frame_1(self, processed_frame):

        # Display the processed frame from camera 1 on the label camera1_label

        if processed_frame.shape == (0, 0, 0):
            return
        
        processed_frame = cv.cvtColor(processed_frame, cv.COLOR_BGR2RGB)
        height, width, channel = processed_frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(processed_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.video_label_1.setPixmap(pixmap)      

    def update_frame_2(self, processed_frame):

        # Display the processed frame from camera 2 on the label camera2_label

        if processed_frame.shape == (0, 0, 0):
            return
        
        processed_frame = cv.cvtColor(processed_frame, cv.COLOR_BGR2RGB)
        height, width, channel = processed_frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(processed_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.video_label_2.setPixmap(pixmap)           

    def closeEvent(self, event):
        # Release the cameras and perform cleanup for both processors
        # self.frame_processor_1.camera.release()
        self.frame_processor_2.camera.release()
        event.accept()    

def main():
    app = QApplication(sys.argv)
    window = MYGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
