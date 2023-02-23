# This class handles all functionalities when connecting to the Raspberry

# Import Rpi and sleep libraris
import RPi.GPIO as GPIO
from time import sleep
# Set a global flag
isActive = 0 # this tells the program if the light is on or off

def set_up():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    LED = 23
    GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)


def light_controller()->int:
    global isActive
    if isActive == 1:
        # Turn the light off
        #GPIO.output(LED, 0)
        print("LIGHT OFF: " + str(isActive))
        isActive = 0
        return 0
    else:
        # Turn the light on
        isActive = 1
        print("LIGHT ON: " + str(isActive))
        #GPIO.output(LED, 1)
        return 1