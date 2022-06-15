import time
import RPi.GPIO as GPIO

class MG996R:
    def __init__(self, pin):
        #GPIO.setwornings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50) #50kHz
        self.pwm.start(0)

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()

    def write(self, angle): #0 ~ 180
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        dc = angle * 9.5 / 180.0 + 2.5
        self.pwm.ChangeDutyCycle(dc)

class LG20MG:
    def __init__(self, pin):
        #GPIO.setwornings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50) #50kHz
        self.pwm.start(0)
        
    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()

    def write(self, angle): #0 ~ 180
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        dc = angle * 10 / 180.0 + 2.5
        self.pwm.ChangeDutyCycle(dc)

if __name__ == '__main__':
    l_servo = MG996R(18)
    r_servo = LG20MG(12)
    time.sleep(1)
    i = 0
    while i < 3:
        l_servo.write(0)
        r_servo.write(0)
        time.sleep(1)
        l_servo.write(90)
        r_servo.write(90)
        time.sleep(1)
        l_servo.write(180)
        r_servo.write(180)
        time.sleep(1)
        l_servo.write(90)
        r_servo.write(90)
        time.sleep(1)
        i = i + 1
    print('fin')
