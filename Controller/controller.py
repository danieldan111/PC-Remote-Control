from PIL import Image,ImageTk #pip install pillow
import time
import threading
import socket
from PIL import *
import cv2
import numpy as np
from pynput.keyboard import Key, Controller


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DIS_MSG"

controller = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controller.bind(ADDR)


def screen_display(main_conn, main_addr):
    ADDR_SCREEN = (SERVER, 5055)
    screen_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_recv.bind(ADDR_SCREEN)
    

    def screen_begin(conn, addr):
        def stream(conn, addr):
            sharing = True
            while sharing:
                
                img_size = conn.recv(100).decode(FORMAT)
                
                if img_size:
                    

                    img_size = int(img_size)

                    data = b''
                    while len(data) < img_size:
                        packet = conn.recv(1024)
                        if not packet:
                            break
                        data += packet

                    
                    np_array = np.frombuffer(data, np.uint8)
                    
                    
                    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                    
                    # Display the image using OpenCV
                    cv2.imshow('Image', image)
                    cv2.waitKey(1)
                    # cv2.destroyAllWindows()


                    img_confirm = "img recv".encode(FORMAT)
                    img_confirm += b' ' * (100 - len(img_confirm))

                    conn.send(img_confirm)

                    contin_msg = conn.recv(100).decode(FORMAT)
                    # print(contin_msg)
                    time.sleep(0.00833333333)
                    # sharing = False

            

        confirm_msg = conn.recv(100).decode(FORMAT)

        confirm_back = "screen connected".encode(FORMAT)
        confirm_back += b' ' * (100 - len(confirm_back))

        conn.send(confirm_back)
        
        stream(conn, addr)
        


    def start_screen():
        screen_recv.listen()
        print(f"[LISTENING] Screen is Waiting for connection on {SERVER}")

        accept_screen_msg = "!SCREEN_CONNECT".encode(FORMAT)
        accept_screen_msg += b' ' * (100 - len(accept_screen_msg))
        main_conn.send(accept_screen_msg)

        while True:
            conn, addr = screen_recv.accept()
            screen_begin(conn, addr)

    
    start_screen()

def keyboard_start(main_conn, main_addr):
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
        main_conn.send(accept_keyboard_msg)

        while True:
            conn, addr = keyboard_recv.accept()
            keyboard_begin(conn, addr)
    
    start_keyboard()

def begin_remote_controll(conn, addr):
    confirm_msg = conn.recv(100).decode(FORMAT)

    print(confirm_msg)

    confirm_back = "!succses_connect".encode(FORMAT)
    confirm_back += b' ' * (100 - len(confirm_back))
    conn.send(confirm_back)

    # screen_share = threading.Thread(target=screen_display,args=(conn,addr))
    # screen_share.start()

    keyboard_thread = threading.Thread(target=keyboard_start, args=(conn, addr))
    keyboard_thread.start()
    

def start():
    controller.listen()
    print(f"[LISTENING] Server is listnening on {SERVER}")
    while True:
        conn, addr = controller.accept()
        begin_remote_controll(conn, addr)
        


start() 

