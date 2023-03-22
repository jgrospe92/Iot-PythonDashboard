# This class handles all functionalities when connecting to the Raspberry

from redmail import EmailSender
from redbox import EmailBox
from . import email_config

# Import Rpi and sleep libraries
# Uncomment this if your working on your GPIO
# import RPi.GPIO as GPIO
# from time import sleep
# Set a global flag
isActive = 0  # this tells the program if the light is on or off
LED = 0
EMAIL_STATUS = False
FAN_ON = False


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


# sending email
def send_email(temp: int, email_to : str):
    global EMAIL_STATUS
    if not EMAIL_STATUS:
        email = EmailSender(
            host="smtp.gmail.com",
            port=587,
            username=email_config.username,
            password=email_config.password)

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
    EMAIL_STATUS = True
    print("EMAIL STATUS : ", end="")
    print(EMAIL_STATUS)
    print("Message Sent!")


# Receiving Email
def check_email():
    global EMAIL_STATUS, FAN_ON
    print("EMAIL STATUS : ", end="")
    print(EMAIL_STATUS)
    print("FAN STATUS : ", end="")
    print(FAN_ON)
    msg = ""
    if EMAIL_STATUS:
        box = EmailBox(
            host="smtp.gmail.com",
            port=993,
            username=email_config.username,
            password=email_config.password)

        # Select Email
        inbox = box["INBOX"]

        # query and process messages
        messages = inbox.search(subject="Alert", unseen=True)
        if messages:
            messages[0].read()
            body = messages[0].text_body.split()
            print(body)
            if 'YES' == body[0]:
                print('BODY IS YES')
                FAN_ON = True
            elif 'STOP' == body[0]:
                FAN_ON = False
                EMAIL_STATUS = False
