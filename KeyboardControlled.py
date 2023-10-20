#-------------Library Included -------------------------------
import keyboard
import requests
import time
import serial
import psutil
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from matplotlib import style
#----------default access point ip for esp8266 also you can get it from esp code-------------------
esp8266_ip = "192.168.137.37" 

#---------Functions for sending strings for my motion over url---------------------
def moveForward():
      try:   
         print("move forward")
         data_to_send = "forward"
         url = f"http://{esp8266_ip}/postdata"
         payload = {'data': data_to_send}

         response = requests.post(url, data=payload)

      except:
           print("Error has happened")   
def moveBackward():
      try:   
         print("move backward")
         data_to_send = "backward"
         url = f"http://{esp8266_ip}/postdata"
         payload = {'data': data_to_send}

         response = requests.post(url, data=payload)

      except:
           print("Error has happened") 
def moveLeft():
      try:   
         print("move left")
         data_to_send = "left"
         url = f"http://{esp8266_ip}/postdata"
         payload = {'data': data_to_send}

         response = requests.post(url, data=payload)

      except:
           print("Error has happened") 
def moveRight():
      try:  
         print("move right")
         data_to_send = "right"
         url = f"http://{esp8266_ip}/postdata"
         payload = {'data': data_to_send}

         response = requests.post(url, data=payload)

      except:
           print("Error has happened") 
def stopMotors():
      try:   
         print("stop motors")
         data_to_send = "stop"
         url = f"http://{esp8266_ip}/postdata"
         payload = {'data': data_to_send}

         response = requests.post(url, data=payload)

      except:
           print("Error has happened") 
def moveFowardRight():
      try:   
         print("move forward right")
         data_to_send = "eright"
         url = f"http://{esp8266_ip}/postdata"
         payload = {'data': data_to_send}

         response = requests.post(url, data=payload)

      except:
           print("Error has happened") 
def moveForwardLeft():
      try:   
         print("move forward left")
         data_to_send = "qleft"
         url = f"http://{esp8266_ip}/postdata"
         payload = {'data': data_to_send}

         response = requests.post(url, data=payload)

      except:
           print("Error has happened") 


def servoClockwise():
      try:
            print("clockwise")
            data_to_send="cw"
            url = f"http://{esp8266_ip}/postdata"  
            payload = {'data': data_to_send}
            response = requests.post(url, data=payload)

      except:
          print("Error has happened")        
def servoAnticlockwise():
      try:
            print("Anticlockwise")
            data_to_send="ccw"
            url = f"http://{esp8266_ip}/postdata"  
            payload = {'data': data_to_send}
            response = requests.post(url, data=payload)
            print("received data: ",response.text)
            
      except:
          print("Error has happened")    



# Initialize a variable to track if any movement key is pressed
movement_key_pressed = False
while True:
    if keyboard.is_pressed("w"):
        moveForward()
        movement_key_pressed = True
    elif keyboard.is_pressed("s"):
        moveBackward()
        movement_key_pressed = True
    elif keyboard.is_pressed("d"):
        moveRight()
        movement_key_pressed = True
    elif keyboard.is_pressed("a"):
        moveLeft()
        movement_key_pressed = True
    elif keyboard.is_pressed("e"):
        moveFowardRight()
        movement_key_pressed = True
    elif keyboard.is_pressed("q"):
        moveForwardLeft()
        movement_key_pressed = True
    elif keyboard.is_pressed("c"):
         servoClockwise()
        
    elif keyboard.is_pressed("x"):
         servoAnticlockwise()
         
    else:
        # Condition for checking if any key is pressed
        if movement_key_pressed:
            stopMotors()
            movement_key_pressed = False
