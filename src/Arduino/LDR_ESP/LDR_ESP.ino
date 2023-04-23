#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "arduino_secrets.h"


// RFID
#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN D8
#define RST_PIN D0
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
MFRC522::MIFARE_Key key;
// Init array that will store new NUID
byte nuidPICC[4];


//const char* ssid = "TP-Link_2AD8";
const char* ssid = SECRET_SSID;
//const char* password = "14730078";
const char* password = SECRET_PASS;
//const char* mqtt_server = "192.168.0.148";
const char* mqtt_server = "10.0.0.197";
WiFiClient vanieriot;
PubSubClient client(vanieriot);
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
 Serial.print("WiFi connected - ESP-8266 IP address: ");
 Serial.println(WiFi.localIP());
}
void callback(String topic, byte* message, unsigned int length) {
 Serial.print("Message arrived on topic: ");
 Serial.print(topic);
 Serial.print(". Message: ");
 String messagein;

 for (int i = 0; i < length; i++) {
 Serial.print((char)message[i]);
 messagein += (char)message[i];
 }

}
void reconnect() {
 while (!client.connected()) {
 Serial.print("Attempting MQTT connection...");
 if (client.connect("vanieriot")) {
 Serial.println("connected");

 } else {
 Serial.print("failed, rc=");
 Serial.print(client.state());
 Serial.println(" try again in 3 seconds");
 // Wait 5 seconds before retrying
 delay(3000);
 }
 }
}
void setup() {

 Serial.begin(115200);
 setup_wifi();
 client.setServer(mqtt_server, 1883);
 client.setCallback(callback);
 // setup for the rfid
 SPI.begin(); // Init SPI bus
 rfid.PCD_Init(); // Init MFRC522
 Serial.println();
 Serial.print(F("Reader :"));
 rfid.PCD_DumpVersionToSerial();
 for (byte i = 0; i < 6; i++) {
  key.keyByte[i] = 0xFF;
 }
 //Note: To use the RFID RC522 module we use the SPI.h library which will allow us to
 //establish the communication between the ESP8266 card and the module; and the
 //MFRC522.h library which will allow us to dialogue with the module.
 Serial.println();
 Serial.println(F("This code scan the MIFARE Classic NUID."));
 Serial.print(F("Using the following key:"));
}
void loop() {
 //int sensorValue = analogRead(A0);
 // char sum[5];
 //itoa(sensorValue, sum, 10);
 // start of rfid
 // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
 // card id
String card_id = "";
if ( ! rfid.PICC_IsNewCardPresent())
 return;
// Verify if the NUID has been readed
if ( ! rfid.PICC_ReadCardSerial())
 return;
Serial.print(F("PICC type: "));
MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
Serial.println(rfid.PICC_GetTypeName(piccType));
// Check is the PICC of Classic MIFARE type
if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
 piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
 piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
 Serial.println(F("Your tag is not of type MIFARE Classic."));
 return;
}
if (rfid.uid.uidByte[0] != nuidPICC[0] ||
 rfid.uid.uidByte[1] != nuidPICC[1] ||
 rfid.uid.uidByte[2] != nuidPICC[2] ||
 rfid.uid.uidByte[3] != nuidPICC[3] ) {
 Serial.println(F("A new card has been detected."));
 // Store NUID into nuidPICC array
 for (byte i = 0; i < 4; i++) {
 nuidPICC[i] = rfid.uid.uidByte[i];
 }
 Serial.println(F("The NUID tag is:"));
 Serial.println();
 Serial.print(F("In dec: "));
 printDec(rfid.uid.uidByte, rfid.uid.size);
 card_id = String(rfid.uid.uidByte[0]) + String(rfid.uid.uidByte[1]) + String(rfid.uid.uidByte[2]) + String(rfid.uid.uidByte[3]);
 Serial.println();
 Serial.print("UID : " + card_id);
}
else {
  card_id = "";
  Serial.println(F("Card read previously."));
}
// Halt PICC
rfid.PICC_HaltA();
// Stop encryption on PCD
rfid.PCD_StopCrypto1();

 // -- end of rfid
 
 if (!client.connected()) {
 reconnect();
 }
 if(!client.loop())
  client.connect("vanieriot");
  String name = "jeffrey";

  //client.publish("IoTlab/ESP",sum);
client.publish("IoTlab/RFID","helo");

 delay(5000);
 }

 /** 
 Helper routine to dump a byte array as dec values to Serial.
*/
void printDec(byte *buffer, byte bufferSize) {
for (byte i = 0; i < bufferSize; i++) {
 Serial.print(buffer[i] < 0x10 ? " 0" : " ");
 Serial.print(buffer[i], DEC);
 
}

}
