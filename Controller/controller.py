from PIL import Image,ImageTk #pip install pillow
import os
from tkinter import *
import time
import threading
import socket
from PIL import *
import base64
import io


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

                    

                    img = ImageTk.PhotoImage(Image.open(io.BytesIO(data)))

                    

                    # canvas1.delete('all')
                    # canvas1.create_image(0, 0, image = img, anchor = 'nw')
                    
                    
                    # window.update()

                    img_confirm = "img recv".encode(FORMAT)
                    img_confirm += b' ' * (100 - len(img_confirm))

                    conn.send(img_confirm)

                    contin_msg = conn.recv(100).decode(FORMAT)
                    print(contin_msg)
                    # sharing = False

            

        confirm_msg = conn.recv(100).decode(FORMAT)

        confirm_back = "screen connected".encode(FORMAT)
        confirm_back += b' ' * (100 - len(confirm_back))

        conn.send(confirm_back)
        
        window = Tk()

        width= window.winfo_screenwidth() 
        height= window.winfo_screenheight()

        window.geometry("%dx%d" % (width, height))
        window.state('zoomed')

        #canvas for the img
        canvas1 = Canvas(window, width = width, height = height) 
        canvas1.pack(fill = "both", expand = True) 

        stream_thread = threading.Thread(target=stream, args=(conn, addr))
        stream_thread.start()

        window.mainloop()
        


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

    screen_share = threading.Thread(target=screen_display,args=(conn,addr))
    screen_share.start()


def start():
    controller.listen()
    print(f"[LISTENING] Server is listnening on {SERVER}")
    while True:
        conn, addr = controller.accept()
        begin_remote_controll(conn, addr)
        


start()

