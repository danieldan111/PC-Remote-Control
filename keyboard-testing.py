from pynput.keyboard import Key, Controller
from pynput import keyboard
import time

keyboard1 = Controller()

keyboard1.press(Key.ctrl_l)
keyboard1.press("a")



keyboard1.release(Key.ctrl_l)
keyboard1.release("a")

#hello