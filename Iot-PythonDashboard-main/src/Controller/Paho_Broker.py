"""
Python MQTT Subscription client - No Username/Password
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
from . import broker_IP
import src.Controller.ControllerSystem as cs
import paho.mqtt.subscribe as subscribe

class ESPBroker:

    # Don't forget to change the variables for the MQTT broker!
    def __init__(self, mqtt_topic="IoTlab/ESP"):
        self.mqtt_topic = mqtt_topic
        self.mqtt_broker_ip = broker_IP.ipaddress
        self.client = mqtt.Client()

    # These functions handle what happens when the MQTT client connects
    # to the broker, and what happens then the topic receives a message
    def on_connect(self, client, userdata, flags, rc):
        # rc is the error code returned when connecting to the broker
        print("Connected!", str(rc))

        # Once the client has connected to the broker, subscribe to the topic
        self.client.subscribe(self.mqtt_topic)

    def on_message(self, client, userdata, msg):
        # This function is called everytime the topic is published to.
        # If you want to check each message, and do something depending on
        # the content, the code to do this should be run in this function

        #print("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
        sensor_value = [int(s) for s in msg.payload.split() if s.isdigit()]
        cs.sensorValue = sensor_value[0]

        # The message itself is stored in the msg variable
        # and details about who sent it are stored in userdata
    def start_sub(self):
        # Here, we are telling the client which functions are to be run
        # on connecting, and on receiving a message
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Once everything has been set up, we can (finally) connect to the broker
        # 1883 is the listener port that the MQTT broker is using
        self.client.connect_async(self.mqtt_broker_ip, port=1883, keepalive=60, bind_address="")
        #self.client.connect(self.mqtt_broker_ip, 1883)

        # Once we have told the client to connect, let the client object run itself
        #self.client.loop_forever()
        #self.client.disconnect()
        self.client.loop_start()
        # msg = subscribe.simple(self.mqtt_topic, hostname=self.mqtt_broker_ip)
        # value = msg
        # print("%s %s" % (msg.topic, msg.payload))