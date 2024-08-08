from PIL import Image,ImageTk #pip install pillow
import time
import threading
import socket
from PIL import *
import cv2
import numpy as np
from pynput import keyboard


HEADER = 64
PORT = 5050
SERVER = "10.0.0.7" #ip of the controlled device
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"

# KEYBOARD_ADDR = (SERVER, 5056)
# keyboard_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# keyboard_sock.connect(KEYBOARD_ADDR)

SCREEN_ADDR = (SERVER, 5050)
screen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
screen_sock.connect(SCREEN_ADDR)


def screen_watch():
    screen_msg = "SCREEN_connecting".encode(FORMAT)
    screen_msg += b' ' * (100 - len(screen_msg))

    screen_sock.send(screen_msg)

    confirm_msg = screen_sock.recv(100).decode(FORMAT).strip()

    screen_sharing = True
    while screen_sharing:
        #code
        try:
            # Receive the size of the image
            size_info = screen_sock.recv(4)
            if not size_info:
                break
            size = int.from_bytes(size_info, 'big')

            # Receive the image data
            data = b''
            while len(data) < size:
                packet = screen_sock.recv(size - len(data))
                if not packet:
                    break
                data += packet

            if data:
                # Convert the byte data to a numpy array and then decode it
                image_data = np.frombuffer(data, dtype=np.uint8)
                image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

                if image is not None:
                    # Get the dimensions of the image
                    # img_height, img_width = image.shape[:2]
                    
                    # # Calculate the scale factor to fit the image to full screen
                    # screen_width = cv2.getWindowImageRect('Screen Viewer')[2]
                    # screen_height = cv2.getWindowImageRect('Screen Viewer')[3]
                    # scale_factor = min(screen_width / img_width, screen_height / img_height)
                    # new_width = int(img_width * scale_factor)
                    # new_height = int(img_height * scale_factor)

                    # # Resize the image
                    # resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)


                    cv2.namedWindow("Screen Viewer", cv2.WINDOW_NORMAL)
                    cv2.setWindowProperty("Screen Viewer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    # Display the resized image
                    cv2.imshow('Screen Viewer', image)

                    # Handle window events
                    key = cv2.waitKey(1)
                    if key == 27:  # ESC key
                        break

        except Exception as e:
            print(f"Error receiving or displaying image: {e}")
            break


def keyboard_share():
    def on_press(key):
        try:
            press_key = "!PRESS ".encode(FORMAT)
            press_key += str(key.char).encode(FORMAT)
            press_key += b' ' * (100 - len(press_key))
            keyboard_sock.send(press_key)
            
        except AttributeError:
            press_key = "!PRESS ".encode(FORMAT)
            press_key += str(key).encode(FORMAT)
            press_key += b' ' * (100 - len(press_key))
            keyboard_sock.send(press_key)


    def on_release(key):
        try:
            press_key = "!RELIS ".encode(FORMAT)
            press_key += str(key.char).encode(FORMAT)
            press_key += b' ' * (100 - len(press_key))
            keyboard_sock.send(press_key)

            
        except AttributeError:
            press_key = "!RELIS ".encode(FORMAT)
            press_key += str(key).encode(FORMAT)
            press_key += b' ' * (100 - len(press_key))
            keyboard_sock.send(press_key)
    

    keyboard_msg = "KEYBOARD_connecting".encode(FORMAT)
    keyboard_msg += b' ' * (100 - len(keyboard_msg))

    keyboard_sock.send(keyboard_msg)

    confirm_msg = keyboard_sock.recv(100).decode(FORMAT).strip()

    
    listner = keyboard.Listener(on_press=on_press, on_release=on_release)
    listner.start()
    listner.join()
        

# keyboard_share()

screen_watch()
