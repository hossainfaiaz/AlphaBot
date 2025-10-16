import socket
from pynput import keyboard #python -m pip install pynput

# 192.168.1.118
# 10.210.0.50
ADDRESS = ('192.168.1.120', 4004) # 0-0-0-0 : indirizzo speciale anche detto "this host" 
BUFFER = 4096

#crea un socekt ipv4 TCP
Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#invia richiesta al server
Client.connect(ADDRESS)

# funzione eseguita qundo tasto è premuto
def on_press(key):
    try:
        if key.char in ['a', 's', 'd', 'w']:
            input()
            time = int(input("How long do you wannna move: "))

            Client.sendall(f"{key.char}|{time}".encode())
    except AttributeError:
        if key == keyboard.Key.space:
            Client.sendall(b'stop')
        elif key == keyboard.Key.esc:
            print('Exiting...')
        else:
            print(f'Invalid key: {key}')

# eseguita qudno tasto viene rilasciato
def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

Client.close()