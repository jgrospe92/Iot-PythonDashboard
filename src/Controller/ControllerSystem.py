# This class handles all functionalities when connecting to the Raspberry

from redmail import EmailSender
from redbox import EmailBox
from . import email_config
import time
from time import sleep

# Import Rpi and sleep libraries
# Uncomment this if your working on your GPIO
import RPi.GPIO as GPIO

# Set a global flag
isActive = 0  # this tells the program if the light is on or off
LED = 0
# EMAIL_STATUS is a boolean flag that indicates if the email is sent
EMAIL_STATUS = False
# FAN_ON is a boolean flag that indicates if the fan is on
FAN_ON = False


"""
@PARAMS
@RETURN
DESC: DHT class
"""
class DHT(object):
    DHTLIB_OK = 0
    DHTLIB_ERROR_CHECKSUM = -1
    DHTLIB_ERROR_TIMEOUT = -2
    DHTLIB_INVALID_VALUE = -999

    DHTLIB_DHT11_WAKEUP = 0.020  # 0.018		#18ms
    DHTLIB_TIMEOUT = 0.0001  # 100us

    humidity = 0
    temperature = 0

    def __init__(self, pin):
        self.pin = pin
        self.bits = [0, 0, 0, 0, 0]
        # GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM)

    # Read DHT sensor, store the original data in bits[]
    def readSensor(self, pin, wakeupDelay):
        mask = 0x80
        idx = 0
        self.bits = [0, 0, 0, 0, 0]
        # Clear sda
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        # start signal
        GPIO.output(pin, GPIO.LOW)
        time.sleep(wakeupDelay)
        GPIO.output(pin, GPIO.HIGH)
        # time.sleep(0.000001)
        GPIO.setup(pin, GPIO.IN)

        loopCnt = self.DHTLIB_TIMEOUT
        # Waiting echo
        t = time.time()
        while True:
            if (GPIO.input(pin) == GPIO.LOW):
                break
            if ((time.time() - t) > loopCnt):
                return self.DHTLIB_ERROR_TIMEOUT
        # Waiting echo low level end
        t = time.time()
        while (GPIO.input(pin) == GPIO.LOW):
            if ((time.time() - t) > loopCnt):
                # print ("Echo LOW")
                return self.DHTLIB_ERROR_TIMEOUT
        # Waiting echo high level end
        t = time.time()
        while (GPIO.input(pin) == GPIO.HIGH):
            if ((time.time() - t) > loopCnt):
                # print ("Echo HIGH")
                return self.DHTLIB_ERROR_TIMEOUT
        for i in range(0, 40, 1):
            t = time.time()
            while (GPIO.input(pin) == GPIO.LOW):
                if ((time.time() - t) > loopCnt):
                    # print ("Data Low %d"%(i))
                    return self.DHTLIB_ERROR_TIMEOUT
            t = time.time()
            while (GPIO.input(pin) == GPIO.HIGH):
                if ((time.time() - t) > loopCnt):
                    # print ("Data HIGH %d"%(i))
                    return self.DHTLIB_ERROR_TIMEOUT
            if ((time.time() - t) > 0.00005):
                self.bits[idx] |= mask
            # print("t : %f"%(time.time()-t))
            mask >>= 1
            if (mask == 0):
                mask = 0x80
                idx += 1
        # print (self.bits)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        return self.DHTLIB_OK

    # Read DHT sensor, analyze the data of temperature and humidity
    def readDHT11Once(self):
        rv = self.readSensor(self.pin, self.DHTLIB_DHT11_WAKEUP)
        if (rv is not self.DHTLIB_OK):
            self.humidity = self.DHTLIB_INVALID_VALUE
            self.temperature = self.DHTLIB_INVALID_VALUE
            return rv
        self.humidity = self.bits[0]
        self.temperature = self.bits[2] + self.bits[3] * 0.1
        sumChk = ((self.bits[0] + self.bits[1] + self.bits[2] + self.bits[3]) & 0xFF)
        if (self.bits[4] is not sumChk):
            return self.DHTLIB_ERROR_CHECKSUM
        return self.DHTLIB_OK

    def readDHT11(self):
        result = self.DHTLIB_INVALID_VALUE
        for i in range(0, 15):
            result = self.readDHT11Once()
            if result == self.DHTLIB_OK:
                return self.DHTLIB_OK
            time.sleep(0.1)
        return result

"""
@PARAMS
@RETURN
DESC: Important! this set ups all the required pins, setmode and setup
    needed for the circuit to work
"""
def set_up():
    global LED
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    # INITIALIZE BCM PINS
    LED = 23

    # SET UP
    GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

"""
@PARAMS
@RETURN int 
DESC: controlls when to turn on the light
"""
def light_controller() -> int:
    global isActive
    if isActive == 1:
        # Turn the light off
        # GPIO.output(LED, 0)
        isActive = 0
        return 0
    else:
        # Turn the light on
        isActive = 1
        # GPIO.output(LED, 1)
        return 1


"""
@PARAMS temp : int, email_to : str
@RETURN
DESC: emmail the temperature to the reciever 
"""
def send_email(temp: int, email_to: str):
    global EMAIL_STATUS
    # If the EMAIL_STATUS is False, then we can send the email
    if not EMAIL_STATUS:
        # create an instance of email
        email = EmailSender(
            host="smtp.gmail.com",
            port=587,
            username=email_config.username,
            password=email_config.password)
        # send the email with the temperature value
        email.send(
            subject="Alert",  # Email Subject
            sender="jgrospetest@gmail.com",
            receivers=[email_to],
            text="The current temperature is {{ temp }},\n"
                 "would you like to turn on the fan? \n"
                 "**reply with (YES/NO) or (STOP) to turn the fan off ",
            body_params=
            {
                "temp": temp
            }
        )
    # Once the email is sent, Set EMAIL_STATUS to True, so it wont keep sending it
    EMAIL_STATUS = True
    print("EMAIL STATUS : ", end="")
    print(EMAIL_STATUS)
    print("Message Sent!")

"""
@PARAMS
@RETURN
DESC: processes the recieved email
    and check if the response is YES
"""
# Receiving Email
def check_email():
    global EMAIL_STATUS, FAN_ON
    print("EMAIL STATUS : ", end="")
    print(EMAIL_STATUS)
    print("FAN STATUS : ", end="")
    print(FAN_ON)
    msg = ""
    # if EMAI_STATUS is True, check the inbox
    if EMAIL_STATUS:
        box = EmailBox(
            host="smtp.gmail.com",
            port=993,
            username=email_config.username,
            password=email_config.password)

        # Select Email inbox
        inbox = box["INBOX"]

        # query and process messages
        messages = inbox.search(subject="Alert", unseen=True)
        if messages:
            # read the first unseen message
            messages[0].read()
            # turn the string message into an array string
            body = messages[0].text_body.split()
            # check the fist index if its equal to 'YES'
            if 'YES' == body[0]:
                print('BODY IS YES')
                FAN_ON = True
            # If the first index is equal to 'STOP'
            # turn the fan off and EMAIL_STATUS False
            elif 'STOP' == body[0]:
                FAN_ON = False
                EMAIL_STATUS = False

"""
@PARAMS
@RETURN int 
DESC: reads the dht and returns humidity and temperature 
"""
def dht11_read():
    dht = DHT(11)
    sumCnt = 0
    okCnt = 0
    # chk = dht.readDHT11()
    humidity = dht.humidity
    temperature = dht.temperature
    print("Humidity : %.2f, \t Temperature : %.2f " % (humidity, temperature))
    return temperature, humidity

"""
@PARAMS on : str
@RETURN
DESC: if argument is 'on' turn on fan, off otherwise
"""
def turn_fan_on(state):
    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setwarnings(False)
    print("RUN THE MOTOR")
    Motor1 = 22  # Enable Pin 22 , 15
    Motor2 = 23  # Input Pin 23 , 16
    Motor3 = 12  # Input Pin 12, 32
    GPIO.setup(Motor1, GPIO.OUT)
    GPIO.setup(Motor2, GPIO.OUT)
    GPIO.setup(Motor3, GPIO.OUT)
    if state == "ON":
        GPIO.output(Motor1, GPIO.HIGH)
        GPIO.output(Motor2, GPIO.LOW)
        GPIO.output(Motor3, GPIO.HIGH)
    elif state == "OFF":
        GPIO.output(Motor1, GPIO.LOW)
        GPIO.cleanup()
