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
String card_id = "";


//const char* ssid = "TP-Link_2AD8";
const char* ssid = SECRET_SSID;
const char* password = SECRET_PASS;
const char* mqtt_server = SECRET_IP;
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
  delay(2000);
  if (!client.connected()) {
 reconnect();
 }
 if(!client.loop()){
  client.connect("vanieriot");
 }
 
  int sensorValue = analogRead(A0);
  char sum[5];
  itoa(sensorValue, sum, 10);
  client.publish("IoTProject/PhotoSensor",sum); 
  //client.publish("IoTlab/ESP","hi");
 
 // start of rfid
 // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
 // card id
if ( ! rfid.PICC_IsNewCardPresent()){
 return; 
}
 
// Verify if the NUID has been readed
if ( ! rfid.PICC_ReadCardSerial()){
 return; 
}
 
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
  card_id = "false";
  // reset nuid array

   for (byte i = 0; i < 4; i++) {
 nuidPICC[i] = 0;
 }
  Serial.println(F("Card read previously."));
}


 int str_len = card_id.length() + 1;
 char char_arr[str_len];
 card_id.toCharArray(char_arr,str_len);
 client.publish("IoTlab/RFID",char_arr);


// Halt PICC
rfid.PICC_HaltA();
// Stop encryption on PCD
rfid.PCD_StopCrypto1();

 // -- end of rfid

 
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

void array_to_string(byte array[], unsigned int len, char buffer[])
{
  for (unsigned int i = 0; i < len ; i++)
  {
    byte nib1 = (array[i] >> 4) & 0x0F;
    byte nib2 = (array[i] >> 0) & 0x0F;
    buffer[i * 2 + 0] = nib1 < 0xA ? '0' + nib1 : 'A' + nib1 - 0xA;
    buffer[i * 2 + 1] = nib2 < 0xA ? '0' + nib2 : 'A' + nib2 - 0xA; 
  }
  buffer[len * 2] = '\0';
}
