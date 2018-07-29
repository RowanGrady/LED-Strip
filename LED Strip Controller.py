import RPi.GPIO as GPIO
import time
import binascii
GPIO.setwarnings(False)
from tkinter import *

#Constants
CYCLESUPPERLIMIT = float(100.0)
CYCLESLOWERLIMIT = float(0.0)
BINARYUPPERLIMIT = int(255)
BINARYLOWERLIMIT = int(0)
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
    cyclesValue = int(binaryValue) * CYCLESUPPERLIMIT / BINARYUPPERLIMIT
    return cyclesValue


def convertBinaryToHex(binaryValue):
    hexValue = hex(binaryValue)
    return hexValue

def setHexBoxValues(redValue, greenValue, blueValue):
    hexArray = [int(redValue), int(greenValue), int(blueValue)]
    hexString = binascii.hexlify(bytes(bytearray(hexArray)))

    hexBox.delete(0, END)
    hexBox.insert(END, hexString)

def convertHexToBinary(colorName, hexValue):
    try:
        binaryValue = int(hexValue, 16)
        return binaryValue
    except:
        launchErrorWindow(colorName + ' hex value of ' + str(colorValue) + ' is out of range.  Must be between ' + str(BINARYLOWERLIMIT) + ' and ' + str(BINARYUPPERLIMIT))
        return 0
    

def convertHexToCycles(colorName, hexValue):
    cyclesValue = convertBinaryToCycles( convertHexToBinary(colorName, hexValue) )
    return cyclesValue


def checkHexValue(hexValue):
    if len(hexValue) != 6:
        launchErrorWindow(hexValue + ' is not valid. Entry must be six (6) characters long, 0-9 or A-F.')
        return False
    else:
        try:
            int(hexValue, 16)
            return True
        except:
            launchErrorWindow(hexValue + ' is not a valid hexadecimal value.')
            return False
        

def testColorValue(colorName, colorValue):
    #check for number value
    try:    
        #check for valid number value
        if int(colorValue) > BINARYUPPERLIMIT or int(colorValue) < BINARYLOWERLIMIT:
            launchErrorWindow(colorName + ' value of ' + str(colorValue) + ' is out of range.  Must be between ' + str(BINARYLOWERLIMIT) + ' and ' + str(BINARYUPPERLIMIT))
            return False
        else:
            return True   
    except:
        launchErrorWindow('Value for ' + colorName + ' is not a number.')
        return False


def changeRGB(redValue, greenValue, blueValue):
    red.ChangeDutyCycle(float(redValue))
    green.ChangeDutyCycle(float(greenValue))
    blue.ChangeDutyCycle(float(blueValue))
    

def update_hex_colors():

    hexValue = hexBox.get()
    if checkHexValue(hexValue):
        redValue = convertHexToCycles('red', hexValue[0:2])
        greenValue = convertHexToCycles('green', hexValue[2:4])
        blueValue = convertHexToCycles('blue', hexValue[4:6])

        changeRGB(redValue, greenValue, blueValue)

        setRGBBoxValues(convertHexToBinary('red', hexValue[0:2]), convertHexToBinary('green', hexValue[2:4]), convertHexToBinary('blue', hexValue[4:6]))    


def launchErrorWindow(message):
    errorWindow = Tk()
    errorWindow.title('Error')
    Label(errorWindow, text= message).grid(row=0)
    okay = Button(errorWindow, text='OK',command=errorWindow.destroy).grid(row=1)


def exit():
    changeRGB(0, 0, 0)
    quit()


def update_rgb_colors():
    redValue = redBox.get()
    greenValue = greenBox.get()
    blueValue = blueBox.get()
    
    if testColorValue("Red", redValue) and testColorValue("Blue", blueValue) and testColorValue("Green", greenValue):
        changeRGB(convertBinaryToCycles(redValue), convertBinaryToCycles(greenValue), convertBinaryToCycles(blueValue))
        setHexBoxValues(redValue, greenValue, blueValue)


def setRGBBoxValues(redValue, greenValue, blueValue):

    redBox.delete(0, END)
    greenBox.delete(0, END)
    blueBox.delete(0, END)
    
    redBox.insert(END, redValue)
    greenBox.insert(END, greenValue)
    blueBox.insert(END, blueValue)

def Pattern_Mode_Win():
    Color_Menu = Tk()
    Color_Menu.title('Pattern Selector')

#Main
window = Tk()
c = Canvas(window, height=600, width=600)
window.title('LED Test')
Label(window, text='Red (0-255)', width=13).grid(row=0)
Label(window, text='Green (0-255)', width=13).grid(row=1)
Label(window, text='Blue (0-255)', width=13).grid(row=2)

redBox = Entry(window, width=3, bg='#ff0000')
greenBox = Entry(window, width=3, bg='#00ff00')
blueBox = Entry(window, width=3, bg='#0000ff', fg='#ffffff')

redBox.grid(row=0, column=1)
greenBox.grid(row=1, column=1)
blueBox.grid(row=2, column=1)

redBox.bind("<Return>", (lambda event: update_rgb_colors()))
greenBox.bind("<Return>", (lambda event: update_rgb_colors()))
blueBox.bind("<Return>", (lambda event: update_rgb_colors()))
redBox.bind("<KP_Enter>", (lambda event: update_rgb_colors()))
greenBox.bind("<KP_Enter>", (lambda event: update_rgb_colors()))
blueBox.bind("<KP_Enter>", (lambda event: update_rgb_colors()))

setRGBBoxValues(0, 0, 0)

rgbApply = Button(window, text='RGB Colors', command=update_rgb_colors)
rgbApply.grid(row=3, column=0)

Pattern_Mode_Button = Button(window, text='Patterns', command=Pattern_Mode_Win)
Pattern_Mode_Button.grid(row=3, column=2)

Label(window, text='Hex #').grid(row=1, column=3)
hexBox = Entry(window, width=6)
hexBox.grid(row=1, column=4)
hexBox.insert(END, '000000')
hexBox.bind("<Return>", (lambda event: update_hex_colors()))

hexApply = Button(window, text='Hex Colors', command=update_hex_colors)
hexApply.grid(row=3, column=4)


exit = Button(window, text='Exit', command=exit).grid(row=4, column=2)
