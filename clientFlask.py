from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import AlphaBot
#import aplhadummybot as AlphaBot
import time
import threading

app = Flask(__name__)
app.secret_key = 'chiave_segreta_molto_piu_sicura_cambiala'

# --- FLASK LOGIN CONFIG ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Robot
alphabot = AlphaBot.AlphaBot()
alphabot.stop()

# --- THREAD ---
class Handle_client(threading.Thread):
    def __init__(self, bot):
        super().__init__()
        self.daemon = True
        self.bot = bot
        self.running = True
    
    def run(self):
        while self.running:
            try:
                if self.bot.is_blocked():
                    self.bot.stop()
                time.sleep(0.001)
            except Exception as e:
                break
    
    def stop(self):
        self.running = False

thread = Handle_client(alphabot)
thread.start()

def move_logic(instruction):
    #print(f"Received: {instruction}")
    if(instruction in ['w', 'a', 's', 'd', 'stop']):
        # Manual movement: map letters to robot directions
        readData(instruction)
    elif(instruction in ['i','j','k','l']):
        readData_slow(instruction)
    elif (instruction in ['q', 'c']):
        # Special movement: fetch from DB
        move_instruction = db(instruction)
        print(f"data list: {move_instruction}")
        if move_instruction:
            for move in move_instruction:
                print(f"move: {move}")
                # Recursively call readData for standard text commands
                readData(move)
        # Ensure robot stops after sequence
        alphabot.stop()

def readData(instruction):
    speed2 = 30
    print(f"done: {instruction}")
    if instruction == 'w':
        #alphabot.forward()
        alphabot.setMotor(-speed2,speed2)
    elif instruction == 'a':
        #alphabot.left()
        alphabot.setMotor(-speed2,-speed2)
    elif instruction == 's':
        #alphabot.backward()
        alphabot.setMotor(speed2, -speed2)
    elif instruction == 'd':
        alphabot.setMotor(speed2, speed2)
        #alphabot.right()
    elif instruction == 'stop':
        alphabot.stop()
    else:
        print(f"Unknown command: {instruction}")

def readData_slow(instruction):
    speed = 100
    print(f"done: {instruction}")
    if instruction == 'i':
        alphabot.setMotor(-speed,speed)
    elif instruction == 'j':
        alphabot.setMotor(-speed,-speed)
    elif instruction == 'k':
        alphabot.setMotor(speed, -speed)
    elif instruction == 'l':
        alphabot.setMotor(speed, speed)
    elif instruction == 'stop':
        pass
    else:
        print(f"Unknown command: {instruction}")

    

def db(key):
    try:
        print(key)
        x = key
        con = sqlite3.connect('db.db') 
        cur = con.cursor()
        # Using parameterized query for safety
        cur.execute("SELECT command FROM Movements WHERE key = ?", (x,))
        results = cur.fetchone()
        con.close()
        
        if results:
            results = results[0] # Get the string
            # Clean string and split
            results = results.replace(' ', '').split('|')
            print(f"results: {results}")
            return results
        else:
            print(f"Nessun comando trovato per il tasto '{x}'")
            return []
    except Exception as e:
        print(f"Errore: {e}")
        return []

#    FLASK ROUTES

# User Class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def validate_user(username, password):
    con = sqlite3.connect('db.db') 
    cur = con.cursor()
    cur.execute("SELECT PASSWORD FROM USERS WHERE USERNAME = ?", (username,))
    row = cur.fetchone()
    con.close()
    if row and row[0] == password: return True
    else : return False

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("control"))
    if request.method == "POST":
        if validate_user(request.form.get("username"), request.form.get("password")):
            login_user(User(request.form.get("username")))
            return redirect(url_for("control"))
        else:
            flash("Invalid Credentials", "error")
    return render_template("login.html")

@app.route("/control", methods=["GET", "POST"])
@login_required
def control():
    if request.method == "POST":
        # 1. Translate Flask Buttons to your One-Letter Codes
        cmd = None
        
        # Mapping HTML buttons to your code structure ('w', 'a', 's', 'd')
        if "Avanti" in request.form: cmd = 'w'
        elif "Sinistra" in request.form: cmd = 'a'
        elif "Indietro" in request.form: cmd = 's'
        elif "Destra" in request.form: cmd = 'd'
        elif "Stop" in request.form: cmd = 'stop'

        elif "Avantis" in request.form: cmd = 'i'
        elif "Sinistras" in request.form: cmd = 'j'
        elif "Indietros" in request.form: cmd = 'k'
        elif "Destras" in request.form: cmd = 'l'

        
        # Mapping Special Keys
        elif "q" in request.form: cmd = 'q'
        elif "c" in request.form: cmd = 'c'

        # 2. Execute your logic (in a thread to prevent freezing)'''
        if cmd:
            threading.Thread(target=move_logic, args=(cmd,)).start()

        return "", 204
    
    return render_template("control.html", username=current_user.id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host='192.168.1.114', port=5005, debug=False)
    # Runs on localhost for testing
    #app.run(host='127.0.0.1', port=5005, debug=True)