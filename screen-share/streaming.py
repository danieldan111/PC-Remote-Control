import socket
import threading
from PIL import ImageGrab #pip install pillow
import io
import time



PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

screen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
screen.bind(ADDR)



def screen_share(conn, addr):
    sharing_screen = True
    chunk_size = 1024

    while sharing_screen:
        img = ImageGrab.grab()

        binary_stream = io.BytesIO()
        img.save(binary_stream, format='PNG')
        binary_data = binary_stream.getvalue()


        img_size = str(len(binary_data)).encode()
        img_size += b' ' * (100 - len(img_size))

        conn.send(img_size)

        total_sent = 0

        total_sent = 0
        while total_sent < len(binary_data):
            chunk = binary_data[total_sent:total_sent + chunk_size]
            if len(chunk) < 1024:
                    chunk += b' ' * (1024 - len(chunk))

            conn.send(chunk)
            total_sent += 1024

        ending_msg = "!SENT_ALL".encode(FORMAT)
        ending_msg += b' ' * (100 - len(ending_msg))
        conn.send(ending_msg)
        # time.sleep()


def screen_listen():
    screen.listen()
    print(f"[LISTENING] Server is listnening on {SERVER}")
    while True:
        conn, addr = screen.accept()
        screen_share(conn, addr)
        


screen_listen()