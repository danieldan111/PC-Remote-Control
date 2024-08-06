from pynput import keyboard
from pynput.keyboard import Key, Controller


keyboard1 = Controller()

# # keyboard1.press(Key.ctrl_l.value)
# keyboard1.press('a')
# keyboard1.release('a')
# # keyboard1.release(Key.ctrl_l)

def on_press(key):
    try:
        print(key.char)
        
    except AttributeError:
        print(key)


def on_release(key):
    try:
        print(key.char)
        
    except AttributeError:
        print(key)
    





listner = keyboard.Listener(on_press=on_press, on_release=on_release)
listner.start()
listner.join()