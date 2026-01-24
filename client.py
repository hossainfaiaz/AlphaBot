# ...existing code...
import socket
from pynput import keyboard
import time

ADDRESS = ('192.168.1.114', 4004)
BUFFER = 4096

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client.connect(ADDRESS)

startTime = 0
keyPressed = ""

def on_press(key):
    global keyPressed, startTime
    try:
        keyPressed = key.char
        startTime = time.time()
        Client.sendall(key.char.encode())
    except AttributeError:
        if key == keyboard.Key.space:
            Client.sendall(b'stop')
        elif key == keyboard.Key.esc:
            print('Exiting...')
            return False

def on_release(key):
    global keyPressed
    if key == keyboard.Key.esc:
        return False
    try:
        keyPressed = ""
        Client.sendall(b'stop')
    except AttributeError:
        pass

try:
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
finally:
    Client.close()
# ...existing code...


