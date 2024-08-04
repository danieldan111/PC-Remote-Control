import socket
from PIL import ImageGrab #pip install pillow
import os
from tkinter import *
import time
import threading
import io
import base64


PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"
SERVER = "10.0.0.21" #ip of the server
ADDR = (SERVER, PORT)
CONNECT_MSG = "!succses_connect"
CONNECT_MSG_SCREEN = "!SCREEN_CONNECT"


def screen_share():
    ADDR_SCREEN = (SERVER, 5055)
    screen_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_stream.connect(ADDR_SCREEN)

    screen_msg = "SCREEN_connecting".encode(FORMAT)
    screen_msg += b' ' * (100 - len(screen_msg))

    screen_stream.send(screen_msg)

    confirm_msg = screen_stream.recv(100).decode(FORMAT).strip()
    
    img = ImageGrab.grab()

    binary_stream = io.BytesIO()
    img.save(binary_stream, format='PNG')
    binary_data = binary_stream.getvalue()

    send_size = str(len(binary_data)).encode()
    send_size += b' ' * (100 - len(send_size))

    screen_stream.send(send_size)

    screen_stream.sendall(binary_data)
    # print("finito")
    # time.sleep(5)
    # print("contineo")
    # img = ImageGrab.grab()

    # binary_stream = io.BytesIO()
    # img.save(binary_stream, format='PNG')
    # binary_data = binary_stream.getvalue()

    # send_size = str(len(binary_data)).encode()
    # send_size += b' ' * (100 - len(send_size))


controlled = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controlled.connect(ADDR)

confirm_connection_msg = "connecting".encode(FORMAT)
confirm_connection_msg += b' ' * (100 - len(confirm_connection_msg))

controlled.send(confirm_connection_msg)

confirm_msg = controlled.recv(100).decode(FORMAT).strip()
print(confirm_msg)

if CONNECT_MSG == confirm_msg:
    confirm_msg = controlled.recv(100).decode(FORMAT).strip()
    if confirm_msg == CONNECT_MSG_SCREEN:
        screen_thread = threading.Thread(target=screen_share)
        






        