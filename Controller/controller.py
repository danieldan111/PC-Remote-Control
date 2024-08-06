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

KEYBOARD_ADDR = (SERVER, 5056)
keyboard_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
keyboard_sock.connect(KEYBOARD_ADDR)



    

    
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
        

keyboard_share()


