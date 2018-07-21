import RPi.GPIO as GPIO
import time

#setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
#Set instance
red = GPIO.PWM(31, 60)
green = GPIO.PWM(32, 60)
blue = GPIO.PWM(35, 60)
#Start the freaking thing
red.start(0)
green.start(100)
blue.start(0)

while True:
    for dutyCycle in range (0, 100, 5):
        red.ChangeDutyCycle(dutyCycle)
        green.ChangeDutyCycle(100 - dutyCycle)
        blue.ChangeDutyCycle(dutyCycle)
        time.sleep(0.1)

    for dutyCycle in range (100, 0, -5):
        red.ChangeDutyCycle(dutyCycle)
        green.ChangeDutyCycle(100 - dutyCycle)
        blue.ChangeDutyCycle(dutyCycle)
        time.sleep(0.1)
