import tkinter as tk
import requests

esp8266_ip = "192.168.4.1" 

def sendCommand():
    try:
        cmd= int(txtCMD.get())
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
def lineFollower():
      try:   
         print("automated car")
         data_to_send = "auto"
         url = f"http://{esp8266_ip}/postdata"
         payload = {'data': data_to_send}

         response = requests.post(url, data=payload)

      except:
           print("Error has happened") 
root = tk.Tk()
mf = tk.Frame(root)
mf.pack()
tk.Label(mf, text='Spindle Angle:').grid(row=1, column=0)
txtCMD = tk.StringVar()
tk.Entry(mf, textvariable=txtCMD).grid(row=1, column=1)
tk.Button(mf, text='Send', command=sendCommand).grid(row=1, column=2)
tk.Button(mf, text='Move Right', command=moveRight).grid(row=5, column=3)
tk.Button(mf, text='Move Left', command=moveLeft).grid(row=5, column=1)
tk.Button(mf, text='Move Backward', command=moveBackward).grid(row=6, column=2)
tk.Button(mf, text='Move Forward', command=moveForward).grid(row=4, column=2)
tk.Button(mf, text='Stop motors', command=stopMotors).grid(row=4, column=1)
tk.Button(mf, text='Line Follower', command=lineFollower).grid(row=4, column=0)
root.title('Wifi motors control')
root.mainloop()
