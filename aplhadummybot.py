import time

try:
    import RPi.GPIO as GPIO
    print("Running on Raspberry Pi: Real Hardware Activated")
    IS_PI = True
except ImportError:
    print("Running on PC: Simulation Mode Activated")
    IS_PI = False
    # Dummy GPIO class to prevent errors on PC
    class GPIO:
        BCM = "BCM"
        OUT = "OUT"
        HIGH = "HIGH"
        LOW = "LOW"
        def setmode(mode): pass
        def setwarnings(flag): pass
        def setup(pin, mode): pass
        def output(pin, state): pass
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

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        
        if IS_PI:
            self.PWMA = GPIO.PWM(self.ENA, 500)
            self.PWMB = GPIO.PWM(self.ENB, 500)
            self.PWMA.start(self.PA)
            self.PWMB.start(self.PB)
        self.stop()

    def forward(self):
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
        print(f"SIMULATION: Motors Set - Left: {left}, Right: {right}")
        if not IS_PI: return
        # (Original logic kept for real Pi)
        if((right >= 0) and (right <= 100)):
            GPIO.output(self.IN1,GPIO.HIGH)
            GPIO.output(self.IN2,GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif((right < 0) and (right >= -100)):
            GPIO.output(self.IN1,GPIO.LOW)
            GPIO.output(self.IN2,GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if((left >= 0) and (left <= 100)):
            GPIO.output(self.IN3,GPIO.HIGH)
            GPIO.output(self.IN4,GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif((left < 0) and (left >= -100)):
            GPIO.output(self.IN3,GPIO.LOW)
            GPIO.output(self.IN4,GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)