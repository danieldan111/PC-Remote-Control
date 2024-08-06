import socket
import time
import cv2
import numpy as np
from PIL import ImageGrab



def capture_and_send(conn):
    while True:
        
        img = ImageGrab.grab()
        
        img_np = np.array(img)
        img_bytes = cv2.imencode('.jpg', img_np)[1].tobytes()
        
        # Send image size
        conn.sendall(len(img_bytes).to_bytes(4, byteorder='big'))

        # Send image data in chunks
        for i in range(0, len(img_bytes), 4096):
            conn.sendall(img_bytes[i:i+4096])

        time.sleep(1/60)  # Target 60 FPS

def main():
    host = '10.0.0.21'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            capture_and_send(conn)


if __name__ == '__main__':
    main()