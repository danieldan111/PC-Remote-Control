import socket
import cv2
import numpy as np

def receive_and_display():
    host = '10.0.0.21'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            # Receive image size
            img_size = int.from_bytes(s.recv(4), byteorder='big')

            # Receive image data in chunks
            img_data = b''
            while len(img_data) < img_size:
                img_data += s.recv(4096)

            # Decode and display image
            img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('Screen Share', img)
            cv2.waitKey(10)
            


if __name__ == '__main__':
    receive_and_display()