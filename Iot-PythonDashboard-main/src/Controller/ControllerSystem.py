# This class handles all functionalities when connecting to the Raspberry

#     from redmail import EmailSender
#     from redbox import EmailBox
# from . import email_config

# Import Rpi and sleep libraries
# Uncomment this if your working on your GPIO
import RPi.GPIO as GPIO
from time import sleep
import time
# Set a global flag
isActive = 0  # this tells the program if the light is on or off
LED = 0


def set_up():
    global LED
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    LED = 23
    GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)


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
        GPIO.setmode(GPIO.BOARD)

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

def loop():
    dht = DHT(11)
    sumCnt = 0
    okCnt = 0
    while (True):
        sumCnt += 1
        chk = dht.readDHT11()
        if (chk is 0):
            okCnt += 1
        okRate = 100.0 * okCnt / sumCnt;
        print("sumCnt : %d, \t okRate : %.2f%% " % (sumCnt, okRate))
        print("chk : %d, \t Humidity : %.2f, \t Temperature : %.2f " % (chk, dht.humidity, dht.temperature))
        time.sleep(1)


def fan_spin():
    try:
        loop()
    #temp = dht.temperature;
    except KeyboardInterrupt:
        pass
    exit()
    

# sending email
# def send_email(temp: int, email_to : str):
#     email = EmailSender(
#         host="smtp.gmail.com",
#         port=587,
#         username=email_config.username,
#         password=email_config.password)
# 
#     email.send(
#         subject="Alert",  # Email Subject
#         sender="jgrospetest@gmail.com",
#         receivers=[email_to],
#         text="The current temperature is {{ temp }},\n"
#             "would you like to turn on the fan? \n"
#             "**reply with (Yes/No) ",
#         body_params=
#         {
#             "temp": temp
#         }
#     )
#     print("Message Sent!")
# 
# 
# # Receiving Email
# def check_email() -> bool:
#     box = EmailBox(
#         host="smtp.gmail.com",
#         port=993,
#         username=email_config.username,
#         password=email_config.password)
# 
#     # Select Email
#     inbox = box["INBOX"]
# 
#     # query and process messages
#     messages = inbox.search(subject="Alert", unseen=False)
# 
#     # iterate through the results
#     for i, msg in enumerate(messages):
#         # Set message to read
#         msg.read()
# 
#         # Get Header information
#         sender = msg.from_
#         subject = msg.subject
#         date = msg.date
# 
#         # Get Text Body of the email
#         body = msg.text_body
# 
#         # get HTML body
#         html_body = msg.html_body
# 
#         # print the content of the email
#         print(
#             f"""
#                    Sender : {msg.from_}
#                    subject : {subject}
#                    date : {date}
#                    Content : {body}
#                    """)
# 
#         if subject == "Alert":
#             if body == "Yes":
#                 return True
# 
#     return False


