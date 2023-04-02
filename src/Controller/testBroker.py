import paho.mqtt.client as mqtt
import broker_IP
import paho.mqtt.subscribe as subscribe
import src.Controller.ControllerSystem as cs


# Don't forget to change the variables for the MQTT broker!
mqtt_topic = "IoTlab/ESP"
mqtt_broker_ip = broker_IP.ipaddress
client = mqtt.Client()


# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print("Connected!", str(rc))

    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe(mqtt_topic)


def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function

    print("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
    sensor_value = [int(s) for s in msg.payload.split() if s.isdigit()]
    cs.sensorValue = sensor_value[0]
    print(sensor_value)
    print("value from cs " +  str(cs.sensorValue))
    print("rounded " + str(round(cs.sensorValue / 100)))
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

    # Here, we are telling the client which functions are to be run
    # on connecting, and on receiving a message


client.on_connect = on_connect
client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, 1883)

# Once we have told the client to connect, let the client object run itself
client.loop_forever()
#client.disconnect()
# msg = subscribe.simple(mqtt_topic, hostname=mqtt_broker_ip)
# value = msg
# print("%s %s" % (msg.topic, msg.payload))
