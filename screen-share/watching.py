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



def screen_display(main_conn, main_addr):
    ADDR_SCREEN = (SERVER, 5055)
    screen_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screen_recv.bind(ADDR_SCREEN)

        
    def screen_begin(conn, addr):
        
        def stream(conn, addr):
            sharing = True
            while sharing:
                
                img_size = conn.recv(100).strip()
                print(img_size)
                if img_size:
                    
                    img_size = img_size.decode(FORMAT)
                    img_size = int(img_size)

                    data = b''
                    while len(data) < img_size:
                        packet = conn.recv(4096)
                        if not packet:
                            break
                        data += packet

                    
                    
                    np_array = np.frombuffer(data, np.uint8)
                    
                    
                    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                    
                    # Display the image using OpenCV
                    cv2.imshow('Image', image)
                    cv2.waitKey(1)
                    # cv2.destroyAllWindows()


                    # img_confirm = "img recv".encode(FORMAT)
                    # img_confirm += b' ' * (100 - len(img_confirm))

                    # conn.send(img_confirm)

                    # contin_msg = conn.recv(100).decode(FORMAT)
                    # print(contin_msg)
                    time.sleep(1/60)
                    # sharing = False

        
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


def begin_remote_controll(conn, addr):
    confirm_msg = conn.recv(100).decode(FORMAT)
    print(confirm_msg)

    confirm_back = "!succses_connect".encode(FORMAT)
    confirm_back += b' ' * (100 - len(confirm_back))
    conn.send(confirm_back)

    # screen_share = threading.Thread(target=screen_display,args=(conn,addr))
    # screen_share.start()



def start():
    controller.listen()
    print(f"[LISTENING] Server is listnening on {SERVER}")
    while True:
        conn, addr = controller.accept()
        begin_remote_controll(conn, addr)
        


start() 
