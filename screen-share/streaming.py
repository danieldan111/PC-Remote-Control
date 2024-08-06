import socket
from PIL import ImageGrab #pip install pillow
import os
from tkinter import *
import time
import threading
import io
from pynput.keyboard import Key, Controller


PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"
SERVER = "10.0.0.21" #ip of the server
MY_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
CONNECT_MSG = "!succses_connect"
CONNECT_MSG_SCREEN = "!SCREEN_CONNECT"
CONNECT_MSG_KEYBOARD = "!KEYBOARD_CONNECT"




controlled = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controlled.connect(ADDR)

confirm_connection_msg = "connecting".encode(FORMAT)
confirm_connection_msg += b' ' * (100 - len(confirm_connection_msg))

controlled.send(confirm_connection_msg)

confirm_msg = controlled.recv(100).decode(FORMAT).strip()
print(confirm_msg)

if CONNECT_MSG == confirm_msg:
    pass
    # for i in range(1):
    #     confirm_msg = controlled.recv(100).decode(FORMAT).strip()
    #     if confirm_msg == CONNECT_MSG_SCREEN:
    #         screen_thread = threading.Thread(target=screen_share)
    #         screen_thread.start()

    #     elif confirm_msg == CONNECT_MSG_KEYBOARD:
    #         keyboard_thread = threading.Thread(target=keyboard_share)
    #         keyboard_thread.start()