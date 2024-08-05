from pynput.keyboard import Key, Controller
from pynput import keyboard

keyboard1 = Controller()

keyboard1.press("ctr")
keyboard1.release("s")