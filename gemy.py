#-------------Library Included -------------------------------
import keyboard
import requests

#----------default access point ip for esp8266 also you can get it from ide -------------------
esp8266_ip = "192.168.137.37" 

#---------Functions for sending strings for my motion over url---------------------
def sendCommand(error):
    try:
        cmd= error
        url = f"http://{esp8266_ip}/set_number?number={cmd}"
        response = requests.get(url)
        if response.status_code == 200:
            print("Number sent successfully")
        else:
            print(f"Failed to send number. Status code: {response.status_code}")
    except:
        print("Invalid input. Please enter a valid number.")

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

    except:
        print("Error has happened")    

def lineFollower_auto():
    try:   
        print("automated car")
        data_to_send = "auto"
        url = f"http://{esp8266_ip}/postdata"
        payload = {'data': data_to_send}

        response = requests.post(url, data=payload)

    except:
        print("Error has happened") 
# Initialize a variable to track if any movement key is pressed
# movement_key_pressed = False
# while True:
#     if keyboard.is_pressed("w"):
#         moveForward()
#         movement_key_pressed = True
#     elif keyboard.is_pressed("s"):
#         moveBackward()
#         movement_key_pressed = True
#     elif keyboard.is_pressed("d"):
#         moveRight()
#         movement_key_pressed = True
#     elif keyboard.is_pressed("a"):
#         moveLeft()
#         movement_key_pressed = True
#     elif keyboard.is_pressed("e"):
#         moveFowardRight()
#         movement_key_pressed = True
#     elif keyboard.is_pressed("q"):
#         moveForwardLeft()
#         movement_key_pressed = True
#     elif keyboard.is_pressed("c"):
#         servoClockwise()
        
#     elif keyboard.is_pressed("x"):
#         servoAnticlockwise()
        
#     else:
#         # Condition for checking if any key is pressed
#         if movement_key_pressed:
#             stopMotors()
#             movement_key_pressed = False