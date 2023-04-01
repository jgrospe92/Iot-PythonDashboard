#include <PubSubClient.h>
#include <ESP8266WiFi.h>

const char* ssid = "Your IP";
const char* password = "Your password";

const char* mqtt_server = "Your mqtt broker server";

WiFiClient espClient;
PubSubClient client(espClient);

const int output = 15;
const int ldr = A0;

// Timers - Auxiliary variables
unsigned long now = millis();
unsigned long lastMeasure = 0;
boolean startTimer = false;
unsigned long currentTime = millis();
unsigned long previousTime = 0; 

// the setup routine runs once when you press reset:
void setup() {
  pinMode(output, OUTPUT);
  digitalWrite(output, HIGH);
  // Serial port for debugging purposes
  Serial.begin(115200);
    
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT
  // If a message is received on the topic esp8266/output, you check if the message is either on or off. 
  // Turns the output according to the message received
  if(topic=="esp8266/output"){
    Serial.print("Changing output to ");
    if(messageTemp == "on"){
      digitalWrite(output, LOW);
      Serial.print("on");
    }
    else if(messageTemp == "off"){
      digitalWrite(output, HIGH);
      Serial.print("off");
    }
  }
  Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");  
      // Subscribe or resubscribe to a topic
      // You can subscribe to more topics (to control more outputs)
      client.subscribe("esp8266/output");  
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// the loop routine runs over and over again forever:
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // Timer variable with current time
  now = millis();

  // Publishes new temperature and LDR readings every 30 seconds
  if (now - lastMeasure > 30000) {
    lastMeasure = now;

    // Publishes LDR values
    client.publish("esp8266/ldr", String(analogRead(ldr)).c_str());
    Serial.println("LDR values published");    
  }

}
