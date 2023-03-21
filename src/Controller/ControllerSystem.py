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
            "**reply with (Yes/No) ",
        body_params=
        {
            "temp": temp
        }
    )
    print("Message Sent!")


# Receiving Email
def check_email() -> bool:
    box = EmailBox(
        host="smtp.gmail.com",
        port=993,
        username='jgrospetest@gmail.com',
        password='suleiglvphkvgfbc')

    # Select Email
    inbox = box["INBOX"]

    # query and process messages
    messages = inbox.search(subject="Alert", unseen=False)

    # iterate through the results
    for i, msg in enumerate(messages):
        # Set message to read
        msg.read()

        # Get Header information
        sender = msg.from_
        subject = msg.subject
        date = msg.date

        # Get Text Body of the email
        body = msg.text_body

        # get HTML body
        html_body = msg.html_body

        # print the content of the email
        print(
            f"""
                   Sender : {msg.from_}
                   subject : {subject}
                   date : {date}
                   Content : {body}
                   """)

        if subject == "Alert":
            if body == "Yes":
                return True

    return False
