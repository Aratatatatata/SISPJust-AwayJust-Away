import time
import RPi.GPIO as GPIO
import sys

class servo:
    def __init__(self, pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.servo = GPIO.PWM(pin, 50)
        self.servo.start(0)

    def __del__(self):
        self.servo.stop()
        GPIO.cleanup()

    def write(self, angle): #0 ~ 180を受け取った時にその分だけ回す
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        dc = (angle/180)*9.5+2.5
        self.servo.ChangeDutyCycle(dc)
        print(angle)

if __name__ == '__main__':
    l_servo = servo(12)
    r_servo = servo(18)
    for i in range(1):
        l_servo.write(180)
        r_servo.write(180)
        time.sleep(3)
        l_servo.write(0)
        r_servo.write(180)
        time.sleep(3)
        l_servo.write(0)
        r_servo.write(0)
        time.sleep(3)
        l_servo.write(90)
        r_servo.write(90)
        time.sleep(3)
    del l_servo
    del r_servo
    print('fin')