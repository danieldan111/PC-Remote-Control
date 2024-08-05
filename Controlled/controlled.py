import socket
from PIL import ImageGrab #pip install pillow
import os
from tkinter import *
import time
import threading
import io
import base64
from pynput.keyboard import Key, Controller


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
    ADDR_KEYBOARD = (SERVER, 5056)
    keyboard_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    keyboard_recv.bind(ADDR_KEYBOARD)


    def keyboard_begin(conn, addr):
        confirm_msg = conn.recv(100).decode(FORMAT)

        print(confirm_msg)

        confirm_back = "keyboard connected".encode(FORMAT)
        confirm_back += b' ' * (100 - len(confirm_back))

        conn.send(confirm_back)
        key_map = {
            "Key.ctrl_l": Key.ctrl_l,
            "Key.ctrl_r": Key.ctrl_r,
            "Key.alt_l": Key.alt_l,
            "Key.alt_r": Key.alt_r,
            "Key.shift": Key.shift,
            "Key.shift_r": Key.shift_r,
            "Key.cmd": Key.cmd,
            "Key.cmd_r": Key.cmd_r,
            "Key.tab": Key.tab,
            "Key.esc": Key.esc,
            "Key.space": Key.space,
            "Key.enter": Key.enter,
            "Key.backspace": Key.backspace,
            "Key.caps_lock": Key.caps_lock
	

            # Add more key mappings as needed
        }
        keyboard_listen = True
        keyboard = Controller()

        while keyboard_listen:
            key_stroke = conn.recv(100).decode(FORMAT).strip()
            if key_stroke:
                mode = key_stroke[:6]
                key = key_stroke[7::]
                if mode == "!PRESS":
                    try:
                        keyboard.press(key)
                    except ValueError:
                        keyboard.press(key_map[key])
                elif mode == "!RELIS":
                    try:
                        keyboard.release(key)
                    except ValueError:
                        keyboard.release(key_map[key])

    def start_keyboard():
        keyboard_recv.listen()
        print(f"[LISTENING] Keyboard is Waiting for connection on {SERVER}")

        accept_keyboard_msg = "!KEYBOARD_CONNECT".encode(FORMAT)
        accept_keyboard_msg += b' ' * (100 - len(accept_keyboard_msg))
        controlled.send(accept_keyboard_msg)

        while True:
            conn, addr = keyboard_recv.accept()
            keyboard_begin(conn, addr)
    
    start_keyboard()





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
            





        