import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
from tkinter import *

#Constants
UPPERLIMIT = 100.0
LOWERLIMIT = 0.0
freq = (120)

#setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)

#Set instance
red = GPIO.PWM(31, freq)
green = GPIO.PWM(32, freq)
blue = GPIO.PWM(35, freq)

#Start the freaking thing
red.start(0)
green.start(0)
blue.start(0)

def convertBinaryToCycles(binaryValue):
    cyclesValue = 100 / binaryValue
    return cyclesValue

def testColorValue(colorName, colorValue):
    #check for number value
    try:
        #print('colorValue is ' + str(colorValue)
        
        
            #check for valid number value
        if float(colorValue) > UPPERLIMIT or float(colorValue) < LOWERLIMIT:
            launchErrorWindow(colorName, colorValue, colorName + ' value of ' + str(colorValue) + ' is out of range.  Must be between 0.0 and 100.0')
            return False
        else:
            return True
        
    except:
        launchErrorWindow(colorName, colorValue, 'Value for ' + colorName + ' is not a number.')
        return False


def changeRGB(redValue, greenValue, blueValue):
    if testColorValue("Red", redValue) and testColorValue("Blue", blueValue) and testColorValue("Green", greenValue):
        red.ChangeDutyCycle(float(redValue))
        green.ChangeDutyCycle(float(greenValue))
        blue.ChangeDutyCycle(float(blueValue))

def launchErrorWindow(colorName, colorValue, message):
    errorWindow = Tk()
    errorWindow.title('Error')
    Label(errorWindow, text= message).grid(row=0)
    okay = Button(errorWindow, text='OK',command=errorWindow.destroy).grid(row=1)

def exit():
    changeRGB(0, 0, 0)
    quit()

def update_colors():
    redValue = e1.get()
    blueValue = e2.get()
    greenValue = e3.get()

    changeRGB(redValue, greenValue, blueValue)

#Main
window = Tk()
c = Canvas(window, height=600, width=600)
window.title('LED Test')
Label(window, text='red').grid(row=0)
Label(window, text='blue').grid(row=1)
Label(window, text='green').grid(row=2)

e1 = Entry(window)
e2 = Entry(window)
e3 = Entry(window)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

e1.insert(END, '0')
e2.insert(END, '0')
e3.insert(END, '0')

apply = Button(window, text='Apply Colors', command=update_colors)
apply.grid(row=3, column=1)

exit = Button(window, text='Exit', command=exit).grid(row=3, column=2)
