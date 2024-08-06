import socket
import threading
import time



PORT = 5050
SERVER = "10.0.0.21"  #the ip of the computer you want to control
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

screen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
screen.connect(ADDR)

def screen_share():
    watching_stream = True
    while watching_stream:
        img_size = screen.recv(100).strip()
        # print(img_size)
        if len(img_size) > 0:
            img_size = int(img_size.decode(FORMAT))
            img_data = b''
            while len(img_data) < img_size:
                chunk = screen.recv(1024)
                img_data += chunk
            

            confirm_ending_msg = screen.recv(100).decode(FORMAT)

            ending_msg = "!SENT_ALL".encode(FORMAT)
            ending_msg += b' ' * (100 - len(ending_msg))
            screen.send(ending_msg)

            print(confirm_ending_msg)

            with open("procces.png", 'wb') as screeny:
                screeny.write(img_data)
            
            # time.sleep(0.1)
            



screen_share()
