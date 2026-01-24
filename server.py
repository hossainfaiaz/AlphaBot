# ...existing code...
import socket
import AlphaBot
import time
import sqlite3

def move():
    data_byte = conn.recv(BUFFER)
    if not data_byte:
        print("Client disconnected")
        return -1
    instruction = data_byte.decode().strip()

    #print(f"Received: {instruction}")

    # handle speed messages "left|right"
    if '|' in instruction:
        parts = instruction.split('|')
        try:
            left = int(parts[0])
            right = int(parts[1])
            alphabot.setMotor(left, right)
        except Exception as e:
            print("Invalid speed message:", e)
    else:
        if(instruction in ['w', 'a', 's', 'd', 'stop']):
            readData(instruction, forward='w', left='a', backward='s', right='d')
        elif (instruction in keysDB()):
            move_instruction = db(instruction)
            print(f"data list: {move_instruction}")
            for move in move_instruction:
                print(f"move: {move}\n")
                readData(move)



def readData(instruction, forward='forward', left='left', backward='backward', right='right'):
    print(f"doing: {instruction}")
    command = instruction.split(',')
    instruction = command[0]
    
    if instruction == forward:
        alphabot.forward()
    elif instruction == left:
        alphabot.left()
    elif instruction == backward:
        alphabot.backward()
    elif instruction == right:
        alphabot.right()
    elif instruction == 'stop':
        alphabot.stop()
    else:
        print("Unknown command")
    if len(command) == 2:
        print(f"time: {command[1]}")
        time.sleep(int(command[1]))

def db(key):
    try:
        print(key)
        x = key
        con = sqlite3.connect('./movementsDB.db')
        cur = con.cursor()
        res = cur.execute(f"SELECT command FROM Movements WHERE key = '{x}'")
        results = res.fetchall()
        con.close()
        if results:
            results = [item[0] for item in results][0]
            results = results.replace(' ', '').split('|')
            print(f"results: {results}")
            return results
        else:
            print(f"Nessun comando trovato per il tasto '{x}'")
    except Exception as e:
        print(f"Errore: {e}")

def keysDB():
    try:
        con = sqlite3.connect('./movementsDB.db')
        cur = con.cursor()
        res = cur.execute(f"SELECT key FROM Movements")
        results = res.fetchall()
        con.close()
        if results:
            #results = [item[0] for item in results][0]
            #results = results.replace(' ', '').split('|')
            results = [item[0] for item in results]
            print(type(results))
            print(results)
        else:
            print(f"Nessun comando trovato per il tasto '{x}'")
    except Exception as e:
        print(f"Errore: {e}")

ADDRESS = ('0.0.0.0', 4004)
BUFFER = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

alphabot = AlphaBot.AlphaBot()
alphabot.stop()

s.bind(ADDRESS)
s.listen(5)
conn, addr = s.accept()


try:
    while True:
        move()

        conn.send("ricevuto".encode())

except Exception as e:
    print(f"ERROR!: {e}")
finally:
    conn.close()
    s.close()
# ...existing code...








"""data_byte = conn.recv(BUFFER)
        if not data_byte:
            print("Client disconnected")
            break
        instruction = data_byte.decode().strip()

        print(f"Received: {instruction}")

        # handle speed messages "left|right"
        if '|' in instruction:
            parts = instruction.split('|')
            try:
                left = int(parts[0])
                right = int(parts[1])
                alphabot.setMotor(left, right)
            except Exception as e:
                print("Invalid speed message:", e)
        else:
            if instruction == 'w':
                alphabot.forward()
            elif instruction == 'a':
                alphabot.left()
            elif instruction == 's':
                alphabot.backward()
            elif instruction == 'd':
                alphabot.right()
            elif instruction == 'stop':
                alphabot.stop()
            else:
                print("Unknown command")
"""