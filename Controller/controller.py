import threading
import socket
from PIL import *  #pip install pillow
import cv2
import numpy as np
from pynput import keyboard, mouse
import pyautogui
from pynput.mouse import Button, Controller as mice


HEADER = 64
PORT = 5050
SERVER = "10.0.0.7" #ip of the controlled device
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"

KEYBOARD_ADDR = (SERVER, 5056)
keyboard_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
keyboard_sock.connect(KEYBOARD_ADDR)

SCREEN_ADDR = (SERVER, 5050)
screen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
screen_sock.connect(SCREEN_ADDR)

MOUSE_ADDR = (SERVER, 5058)
mouse_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mouse_sock.connect(MOUSE_ADDR)


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
                    
                    screen_width, screen_height = pyautogui.size()
                    
                    height, width, _ = image.shape
                    aspect_ratio = width / height
                    new_width = min(screen_width, int(screen_height * aspect_ratio))
                    new_height = min(screen_height, int(screen_width / aspect_ratio))
                    resized_img = cv2.resize(image, (new_width, new_height))

                    cv2.namedWindow("Screen Viewer", cv2.WINDOW_NORMAL)
                    cv2.setWindowProperty("Screen Viewer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    # Display the resized image
                    cv2.imshow('Screen Viewer', resized_img)
                    
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

       
def mouse_share():
    def on_move(x, y):
        move_mouse = f"!MOVE {x} , {y}".encode(FORMAT)
        move_mouse += b' ' * (100 - len(move_mouse))

        mouse_sock.send(move_mouse)


    def on_click(x, y, button, pressed):
        click_mouse = f"!CLIK {button},{pressed}".encode(FORMAT)
        click_mouse += b' ' * (100 - len(click_mouse))

        mouse_sock.send(click_mouse)


    def on_scroll(x, y, dx, dy):
        pass


    mouse_msg = "MOUSE_connecting".encode(FORMAT)
    mouse_msg += b' ' * (100 - len(mouse_msg))

    mouse_sock.send(mouse_msg)

    confirm_msg = mouse_sock.recv(100).decode(FORMAT).strip()

    mouse = mice()
    
    mouse.position = (0, 0)
    
    listener = mouse.Listener(on_move=on_move,on_click=on_click,on_scroll=on_scroll)
    listener.start()
    listener.join()



keyboard_thread = threading.Thread(target=keyboard_share)
keyboard_thread.start()

mouse_thread = threading.Thread(target=mouse_share)
mouse_thread.start()

screen_watch()
