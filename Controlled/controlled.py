import socket
from PIL import ImageGrab #pip install pillow
import os
from tkinter import *
import time
import threading
import io
from pynput.keyboard import Key, Controller as board
from pynput.mouse import Button, Controller as mice



FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"
MY_IP = socket.gethostbyname(socket.gethostname())
CONNECT_MSG = "!succses_connect"
CONNECT_MSG_SCREEN = "!SCREEN_CONNECT"
CONNECT_MSG_KEYBOARD = "!KEYBOARD_CONNECT"






#binding screen, keyboard and mouse:
SCREEN_ADDR = (MY_IP, 5050)
screen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
screen.bind(SCREEN_ADDR)

KEYBOARD_ADDR = (MY_IP, 5056)
keyboard = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
keyboard.bind(KEYBOARD_ADDR)

MOUSE_ADDR = (MY_IP, 5058)
mouse = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mouse.bind(MOUSE_ADDR)


def start_screen():
    def handle_screen(conn, addr):
        confirm_msg = conn.recv(100).decode(FORMAT)

        print(confirm_msg)
        
        confirm_back = "keyboard connected".encode(FORMAT)
        confirm_back += b' ' * (100 - len(confirm_back))

        conn.send(confirm_back)

        screen_sharing = True
        while screen_sharing:
            try:
                screenshot = ImageGrab.grab()
                buffer = io.BytesIO()
                screenshot.save(buffer, format='JPEG', quality=100)  # Adjust JPEG quality here
                data = buffer.getvalue()

                # Send the size of the image first
                size_info = len(data).to_bytes(4, 'big')
                conn.send(size_info)

                conn.sendall(data)
                time.sleep(0.000001)
            except Exception as e:
                print(f"Error capturing or sending screen: {e}")
                break                                   


    screen.listen()
    print(f"[LISTENING] Screen is listnening on {MY_IP}")
    while True:
        conn, addr = screen.accept()
        handle_screen(conn, addr)


def start_keyboard():
    def handle_keyboard(conn, addr):
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
            "Key.caps_lock": Key.caps_lock,
            

            # Add more key mappings as needed
        }
        speciel_keys = {
            "☺": "a",
            "▬": "v",
            "↑": "x",
            "→": "z",
            "♥": "c"
        }
        keyboard_listen = True
        keyboard = board()

        while keyboard_listen:
            key_stroke = conn.recv(100).decode(FORMAT).strip()
            if key_stroke:
                mode = key_stroke[:6]
                key = key_stroke[7::]
                if mode == "!PRESS":
                    if key in speciel_keys:
                        keyboard.press(speciel_keys[key])
                    else:
                        try:
                            keyboard.press(key)
                        except ValueError:
                            keyboard.press(key_map[key])
                        
                elif mode == "!RELIS":
                    if key in speciel_keys:
                        keyboard.release(speciel_keys[key])
                    else:
                        try:
                            keyboard.release(key)
                        except ValueError:
                            keyboard.release(key_map[key])
                        


    keyboard.listen()
    print(f"[LISTENING] Keyboard is listnening on {MY_IP}")
    while True:
        conn, addr = keyboard.accept()
        handle_keyboard(conn, addr)


def start_mouse():
    def handle_mouse(conn, addr):
        confirm_msg = conn.recv(100).decode(FORMAT)

        print(confirm_msg)

        confirm_back = "mouse connected".encode(FORMAT)
        confirm_back += b' ' * (100 - len(confirm_back))

        conn.send(confirm_back)

        mouse = mice()

        mouse.position = (0,0)
        
        mouse_listen = True

        mouse_key_map = {"Button.left" : Button.left, "Button.right": Button.right}
        while mouse_listen:
            mouse_move = conn.recv(100).decode(FORMAT).strip()
            if mouse_move:
                mode = mouse_move[0:5]
                mouse_move = mouse_move[5::]
                if mode == "!MOVE":
                    x, y = mouse_move.split(",")
                    pos = (int(x), int(y))
                    mouse.position = (pos)

                elif mode == "!CLICK":
                    button, pressed = mouse_move.split(",")
                    if pressed:
                        mouse.press(mouse_key_map[button])
                    else:
                        mouse.release(mouse_key_map[button])
                    



    mouse.listen()
    print(f"[LISTENING] Mouse is listnening on {MY_IP}")
    while True:
        conn, addr = mouse.accept()
        handle_mouse(conn, addr)




def start_sockets():
    mouse_thread = threading.Thread(target=start_mouse)
    mouse_thread.start()

    keyboard_thread = threading.Thread(target=start_keyboard)
    keyboard_thread.start()
    start_screen()


start_sockets()




        