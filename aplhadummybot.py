import time

# Fake GPIO for PC
try:
    import RPi.GPIO as GPIO
    print("Running on Raspberry Pi: Real Hardware Activated")
    IS_PI = True
except ImportError:
    print("Running on PC: Simulation Mode Activated")
    IS_PI = False
    class GPIO:
        BCM = "BCM"
        OUT = "OUT"
        IN = "IN"
        PUD_UP = "PUD_UP"
        HIGH = "HIGH"
        LOW = "LOW"
        def setmode(mode): pass
        def setwarnings(flag): pass
        def setup(pin, mode, pull_up_down=None): pass
        def output(pin, state): pass
        # Returns 1 (No Obstacle) by default. Change to 0 to simulate a wall.
        def input(pin): return 1 
        class PWM:
            def __init__(self, pin, freq): pass
            def start(self, duty): pass
            def ChangeDutyCycle(self, duty): pass

class AlphaBot(object):
    def __init__(self, in1=12, in2=13, ena=6, in3=20, in4=21, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA = 50
        self.PB = 50

        self.DR = 16
        self.DL = 19

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        GPIO.setup(self.DR, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.DL, GPIO.IN, GPIO.PUD_UP)
        
        if IS_PI:
            self.PWMA = GPIO.PWM(self.ENA, 500)
            self.PWMB = GPIO.PWM(self.ENB, 500)
            self.PWMA.start(self.PA)
            self.PWMB.start(self.PB)
        self.stop()

    def is_blocked(self):
        if GPIO.input(self.DR) == 0 or GPIO.input(self.DL) == 0:
            return True
        return False

    def forward(self):
        if self.is_blocked():
            print("SIMULATION: 🛑 Obstacle Detected! Stopping.")
            self.stop()
            return

        print("SIMULATION: Robot Moving Forward ⬆️")
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def stop(self):
        print("SIMULATION: Robot Stopped ⏹️")
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def backward(self):
        print("SIMULATION: Robot Moving Backward ⬇️")
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def left(self):
        print("SIMULATION: Robot Turning Left ⬅️")
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def right(self):
        print("SIMULATION: Robot Turning Right ➡️")
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        
    def setPWMA(self, value):
        self.PA = value
        if IS_PI: self.PWMA.ChangeDutyCycle(value)

    def setPWMB(self, value):
        self.PB = value
        if IS_PI: self.PWMB.ChangeDutyCycle(value)    
        
    def setMotor(self, left, right):
        if not IS_PI: return
        # Logic for real hardware would go here