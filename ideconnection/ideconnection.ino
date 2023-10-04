//-- Libraries Included --------------------------------------------------------------
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>
#include <Wire.h>
#include <MPU6050_light.h>
#include <WiFiClient.h>

//---------------Define pins of motors on esp----------------------------------
#define MOTOR_RIGHT_FORWARD 15 //D8
#define MOTOR_RIGHT_BACKWARD 13  // D7
#define MOTOR_LEFT_FORWARD 12   // D6
#define MOTOR_LEFT_BACKWARD 14  // D5
//----------------MPU pins----------------
#define SDA_PIN 4 //D2
#define SCL_PIN 5 //D1
//--------------------IR pins------------------
#define IR_PIN1 0// D3
#define IR_PIN2 2 // D4
//------------------Servo motor pin---------------
#define servoPin 16//D0 
//-----------defining my mpu and servo ----------------- 
Servo myservo;
MPU6050 mpu(Wire);
//====================================================================================
struct MPUData {
  float angleX;
  float angleY;
  float angleZ;
};
//Getting angles only from mpu we can get others infos as in examples
MPUData getMPUData() {
  MPUData data;
  mpu.update();
  data.angleX = mpu.getAngleX();
  data.angleY = mpu.getAngleY();
  data.angleZ = mpu.getAngleZ();
  return data;
}
  int speed = 70 ; // Speed of DC motors
  int speedrot = 50;
 // Network Name and Password
const char* ssid = "Team3";
const char* password = "MOYAJ";

ESP8266WebServer server(80);

void setup() {
  Wire.begin(SDA_PIN,SCL_PIN);

    //Set motor pins as output
  pinMode(MOTOR_RIGHT_FORWARD,OUTPUT);
  pinMode(MOTOR_RIGHT_BACKWARD,OUTPUT);
  pinMode(MOTOR_LEFT_FORWARD,OUTPUT);
  pinMode(MOTOR_LEFT_BACKWARD,OUTPUT);

  //Set pins of IR sensor as input
  pinMode(IR_PIN1, INPUT);
  pinMode(IR_PIN2, INPUT);

    // Attaching the servo pin
  myservo.attach(servoPin);

    // Setting Serial Port
  Serial.begin(9600);
  //-------------MPU Connection-------------------
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while (status != 0) { } // stop everything if could not connect to MPU6050
  mpu.calcOffsets(); // gyro and accelerometer 
  Serial.println("Done!\n"); 
  //-----------Wifi controlling --------------
  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
  server.on("/postdata", HTTP_POST, handlePostData);
  server.on("/set_number", HTTP_GET, handleSetNumber);
  server.begin();
}

void loop() {
  server.handleClient();

}

void handleSetNumber() {
  String numberStr = server.arg("number");
  int number = numberStr.toInt();
  Serial.print("Received number: ");
  Serial.println(number);
   if(number > -1 && number < 181 )
            {
                handleServo(number);
            }
  server.send(200, "text/plain", "Number received: " + numberStr);
}
void handlePostData() {
  String receivedData = server.arg("data");
  Serial.println("Received data: " + receivedData);
  server.send(200, "text/plain","Received data: " + receivedData);
  if(receivedData == "forward" || receivedData == "backward" || receivedData == "right" || receivedData == "left" || receivedData == "stop" || receivedData == "auto")
  {

    handleMotors(receivedData);
  }
}
void handleServo(int angle)
{
  myservo.write(angle);
}
void handleMotors(String state)
{
  switch (state[0])
  {
    case 'f':
     moveForward(speed);
      break;

    case 'b':
      moveBackward(speed);
      break;

    case 'l':
      moveLeft(speedrot);
      break;

    case 'r':
      moveRight(speedrot);
      break;
    case 's':
      stopMotors();
      break;
    case 'a':
      lineFollower();  
      break;
  }
}
int handleIR(int IR_PIN) {
  return digitalRead(IR_PIN);
}
void moveRight(int speed) {
  Serial.println("MoveRight");
  analogWrite(MOTOR_RIGHT_FORWARD , speed);
  analogWrite(MOTOR_RIGHT_BACKWARD , 0);
  analogWrite(MOTOR_LEFT_FORWARD , 0);
  analogWrite(MOTOR_LEFT_BACKWARD ,0);
  
}
void moveLeft(int speed) { 
  Serial.println("MoveLeft");
   analogWrite(MOTOR_RIGHT_FORWARD , 0);
   analogWrite(MOTOR_RIGHT_BACKWARD , 0);
   analogWrite(MOTOR_LEFT_FORWARD , speed);
   analogWrite(MOTOR_LEFT_BACKWARD , 0);
}
void moveForward(int speed){
   Serial.println("MoveForward");
   analogWrite(MOTOR_RIGHT_FORWARD , speed);
   analogWrite(MOTOR_RIGHT_BACKWARD , 0);
   analogWrite(MOTOR_LEFT_FORWARD , speed);
   analogWrite(MOTOR_LEFT_BACKWARD , 0);
}
void moveBackward(int speed){
   Serial.println("MoveBackward");
   analogWrite(MOTOR_RIGHT_FORWARD , 0);
   analogWrite(MOTOR_RIGHT_BACKWARD , speed);
   analogWrite(MOTOR_LEFT_FORWARD , 0);
   analogWrite(MOTOR_LEFT_BACKWARD , speed);
}
void stopMotors() {
   Serial.println("Stopmotors");
   analogWrite(MOTOR_RIGHT_FORWARD , 0);
   analogWrite(MOTOR_RIGHT_BACKWARD , 0);
   analogWrite(MOTOR_LEFT_FORWARD , 0);
   analogWrite(MOTOR_LEFT_BACKWARD , 0);
}
void lineFollower()
{
  Serial.println("Its line follower time");
  //MPUData data = getMPUData() ; getting data from MPU like if(data.angleZ>45)stopMotors()
  //int IR_VALUE1 = handleIR(IR_PIN1); Reading for IR sensors
  //int IR_VALUE2 = handleIR(IR_PIN2);
}
void countMetals()
{
Serial.println("lsa hnshof hn3ml feha eh de ");
/* 3 Ir for example 
if(handleIR(IR1)== LOW || handle(IR2) == LOW || handle(IR3)== LOW)
{
  count ++;
}
*/
}
