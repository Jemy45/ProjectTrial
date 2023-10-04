import keyboard
import requests
esp8266_ip = "192.168.4.1" 
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
import keyboard

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
    else:
        # Check if any movement key was previously pressed
        if movement_key_pressed:
            stopMotors()
            movement_key_pressed = False
