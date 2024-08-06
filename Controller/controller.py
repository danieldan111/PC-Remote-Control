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
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"

controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controller.bind(ADDR)


    

    
def keyboard_share(main_conn, main_addr):
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

    accept_keyboard_msg = "!KEYBOARD_CONNECT".encode(FORMAT)
    accept_keyboard_msg += b' ' * (100 - len(accept_keyboard_msg))
    main_conn.send(accept_keyboard_msg)
    
    SERVER_IP = main_conn.recv(100).decode(FORMAT).strip()
    print(SERVER_IP)

    ADDR_KEYBOARD = (SERVER_IP, 5056)
    keyboard_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    keyboard_stream.connect(ADDR_KEYBOARD)

    keyboard_msg = "KEYBOARD_connecting".encode(FORMAT)
    keyboard_msg += b' ' * (100 - len(keyboard_msg))

    keyboard_stream.send(keyboard_msg)

    confirm_msg = keyboard_stream.recv(100).decode(FORMAT).strip()

    
    listner = keyboard.Listener(on_press=on_press, on_release=on_release)
    listner.start()
        


def begin_remote_controll(conn, addr):
    confirm_msg = conn.recv(100).decode(FORMAT)

    print(confirm_msg)

    confirm_back = "!succses_connect".encode(FORMAT)
    confirm_back += b' ' * (100 - len(confirm_back))
    conn.send(confirm_back)

    screen_share = threading.Thread(target=screen_display,args=(conn,addr))
    screen_share.start()
    time.sleep(1)
    keyboard_thread = threading.Thread(target=keyboard_share, args=(conn, addr))
    keyboard_thread.start()
    

def start():
    controller.listen()
    print(f"[LISTENING] Server is listnening on {SERVER}")
    while True:
        conn, addr = controller.accept()
        begin_remote_controll(conn, addr)
        


start() 

