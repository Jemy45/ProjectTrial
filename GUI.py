import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from os import path
import cv2 as cv
from detection import FrameProcessor
import gemy 
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import matplotlib.pyplot as plt
# import serial

url = 'http://192.168.220.244:8080/video'
esp8266_ip = "192.168.4.1" 

class MYGUI(QMainWindow):

        def __init__(self):
                super(MYGUI, self).__init__()

                self.setWindowTitle("Rover_GUI")

                loadUi(path.join(path.dirname(__file__), "Rover_GUI.ui"), self)
                # loadUi("Rover_GUI.ui", self)
                
                # Find the QLabel widgets created in Qt Designer 
                self.video_label_1 = self.findChild(QLabel, "camera1_label")
                
                # Create FrameProcessor instances for each camera
                self.frame_processor_1 = FrameProcessor(url)

                # Connect the frame_processed signals to update methods
                self.frame_processor_1.frame_processed.connect(self.update_frame_1)
                
                # Create timers to start processing frames for each camera
                self.timer_camera1 = QTimer(self)

                self.timer_camera1.timeout.connect(self.frame_processor_1.process_frame_1)

                self.timer_camera1.start(10)  # Update the frame every 30 milliseconds for camera 1

                # adjust line follower button
                self.line_button = self.findChild(QPushButton, "lineFollower_button")
                self.line_button.clicked.connect(lambda: self.adjust_auto(self.frame_processor_1.mode))
                
                # adjust detection button
                self.detection = self.findChild(QPushButton, "detection_button")
                self.detection.clicked.connect(lambda: self.adjust_detection(self.frame_processor_1.mode))


                #-----------------------------------------------------------
                # initilize counters
                self.metals = 0
                self.metal_Label = self.findChild(QLabel, "counterLabel_M")
                self.incrementButton_M = self.findChild(QPushButton, "incrementButton_M")
                self.incrementButton_M.clicked.connect(self.increment_metals)

                self.squares = 0
                self.square_Label = self.findChild(QLabel, "counterLabel_S")
                self.incrementButton_S = self.findChild(QPushButton, "incrementButton_S")
                self.incrementButton_S.clicked.connect(self.increment_squares)

                self.rectangles = 0
                self.rectangle_Label = self.findChild(QLabel, "counterLabel_R")
                self.incrementButton_R = self.findChild(QPushButton, "incrementButton_R")
                self.incrementButton_R.clicked.connect(self.increment_rectangles)

                self.triangles = 0
                self.triangle_Label = self.findChild(QLabel, "counterLabel_T")
                self.incrementButton_T = self.findChild(QPushButton, "incrementButton_T")
                self.incrementButton_T.clicked.connect(self.increment_triangles)

                self.circles = 0
                self.circle_Label = self.findChild(QLabel, "counterLabel_C")
                self.incrementButton_C = self.findChild(QPushButton, "incrementButton_C")
                self.incrementButton_C.clicked.connect(self.increment_circles)

                self.red = 0
                self.red_Label = self.findChild(QLabel, "counterLabel_r")
                self.incrementButton_r = self.findChild(QPushButton, "incrementButton_r")
                self.incrementButton_r.clicked.connect(self.increment_red)

                self.green = 0
                self.green_Label = self.findChild(QLabel, "counterLabel_g")
                self.incrementButton_g = self.findChild(QPushButton, "incrementButton_g")
                self.incrementButton_g.clicked.connect(self.increment_green)

                self.blue = 0
                self.blue_Label = self.findChild(QLabel, "counterLabel_b")
                self.incrementButton_b = self.findChild(QPushButton, "incrementButton_b")
                self.incrementButton_b.clicked.connect(self.increment_blue)

                self.yellow = 0
                self.yellow_Label = self.findChild(QLabel, "counterLabel_y")
                self.incrementButton_y = self.findChild(QPushButton, "incrementButton_y")
                self.incrementButton_y.clicked.connect(self.increment_yellow)
                #-----------------------------------------------------------------------------------------

                self.show()

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



        def closeEvent(self, event):
                # Release the camera and perform cleanup for both processors
                self.frame_processor_1.camera.release()
                event.accept()    

        def keyPressEvent(self, event):
                # Handle key events here
                key = event.key()

                if key == Qt.Key_W:
                        print("W key is pressed")
                        gemy.moveForward()

                if key == Qt.Key_A:
                        print("A key is pressed")
                        gemy.moveLeft()

                if key == Qt.Key_S:
                        print("S key is pressed")
                        gemy.stopMotors()

                if key == Qt.Key_D:
                        print("D key is pressed")
                        gemy.moveRight()

                if key == Qt.Key_X:
                        print("X key is pressed")
                        gemy.moveBackward()

                if key == Qt.Key_M:
                        print("M key is pressed")
                        gemy.servoClockwise()    

                if key == Qt.Key_N:
                        print("N key is pressed")
                        gemy.servoAnticlockwise()              

        def adjust_auto(self, mode):
                """adjust line follower mode"""
                if mode == 0 or mode == 2: # if it is in normal mode or in detection mode 
                        self.frame_processor_1.mode = 1 # set the line follower mode
                else: 
                        self.frame_processor_1.mode = 0

        def adjust_detection(self, mode): 
                """adjust detection mode"""
                if mode == 0 or mode == 1: # if it is in normal mode or in line follower
                        self.frame_processor_1.mode = 2 # set the detection mode
                else:
                        self.frame_processor_1.mode = 0

        def increment_metals(self):
                self.metals += 1
                self.metal_Label.setText(f"{self.metals}")    
        def increment_squares(self):
                self.squares += 1
                self.square_Label.setText(f"{self.squares}")   
        def increment_rectangles(self):
                self.rectangles += 1
                self.rectangle_Label.setText(f"{self.rectangles}")   
        def increment_triangles(self):
                self.triangles += 1
                self.triangle_Label.setText(f"{self.triangles}")      
        def increment_circles(self):
                self.circles += 1
                self.circle_Label.setText(f"{self.circles}")   
        def increment_red(self):
                self.red += 1
                self.red_Label.setText(f"{self.red}")   
        def increment_blue(self):
                self.blue += 1
                self.blue_Label.setText(f"{self.blue}")   
        def increment_green(self):
                self.green += 1
                self.green_Label.setText(f"{self.green}")   
        def increment_yellow(self):
                self.yellow += 1
                self.yellow_Label.setText(f"{self.yellow}")                                                            

def main():
        app = QApplication(sys.argv)
        window = MYGUI()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
        main()
