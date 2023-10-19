


//-- Libraries Included --------------------------------------------------------------
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>
#include <Wire.h>
#include <MPU6050_light.h>
#include <ESP8266HTTPClient.h>
//---------------Define pins of motors on esp----------------------------------
#define MOTOR_RIGHT_FORWARD 15 //D8
#define MOTOR_RIGHT_BACKWARD 13  // D7
#define MOTOR_LEFT_FORWARD 12   // D6
#define MOTOR_LEFT_BACKWARD 14  // D5
//----------------MPU pins----------------
#define SDA_PIN 4 //D2
#define SCL_PIN 5 //D1
//------------------Servo motor pin---------------
#define servoPin 16//D0 
//-----------defining my mpu and servo ----------------- 
Servo myservo;
MPU6050 mpu(Wire);
//-----------Speed sensor variables (any except for GPIO 16)
#define vel_pin  2 //D4
#define vel2_pin 0 //D3 
volatile int counterL = 0 ;
volatile int counterR = 0; //pulse counters

float slots= 20.0;//number of slots in pinwheel
const float wheelradius = 3.15;//wheel radius in cm

unsigned prev_time = 0, cr_time = 0, dtime =0, timer=0;
float vel=0, rpmL=0, rpmR =0;
float distance=0;
int rotation =0;
//interrupts for motors
void ICACHE_RAM_ATTR ISR_countL()
{
  counterL++;
  rotation = counterL;
  cr_time = millis();
  if(cr_time - prev_time >250)
  {
    if(rotation > slots)
    {dtime = millis() - prev_time;
    rpmL = 2*3.141*((1000/dtime)*60);
    prev_time = millis();
    rotation =0;
    }
  }
} //function counts interrupts;
void ICACHE_RAM_ATTR ISR_countR()
{
  counterR++;
  rotation = counterR;
  cr_time = millis();
  if(cr_time - prev_time >250)
  {
    if(rotation >slots){
    dtime = millis() - prev_time;
    rpmR = 2*3.141*((1000/dtime)*60);
    prev_time = millis();
    rotation =0;
    }
  }
}


//====================================================================================
//-----Speed of motors (2 DC, 1 servo)
  unsigned int speed = 150 ; // Speed of DC motors
  unsigned int updatedSpeed;
  unsigned int speedrot = 70;
  unsigned int coeff = 2 ;  
  int servoAngle = 0;
  int Line_speed = 100;
  int Line_speedrot = 20;
  int line_error = 0 ; 
  int angle_error = 90;
//--------------------
//variables for PID motion control
  double Kp=0.1, setPoint, output, crError;

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


    // Attaching the servo pin
  myservo.attach(servoPin);
  myservo.write(0);  
  
  //setting up speed sensor
  pinMode(vel_pin, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(MOTOR_LEFT_FORWARD),ISR_countL,CHANGE);//increases counter Left motor when speed is increasing
  attachInterrupt(digitalPinToInterrupt(MOTOR_RIGHT_FORWARD),ISR_countR,CHANGE);

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
//-----------------------------------------------------
  
//--------------------------------------------------

  //if no motion, set rpm and velocity to 0
  if (millis()-cr_time>500)
  {
    rpmL=rpmR = vel = 0;
    cr_time = millis();
  }
}

void handleSetNumber() {
  String numberStr = server.arg("number");
  int number = numberStr.toInt();
  Serial.print("Received number: ");
  Serial.println(number);
  line_error = number ; 

  
  server.send(200, "text/plain", "Number received: " + numberStr);
}
void handlePostData() {
  String receivedData = server.arg("data");
  Serial.println("Received data: " + receivedData);
  server.send(200, "text/plain","Received data: " + receivedData);
  if(receivedData == "forward" || receivedData == "backward" || receivedData == "right" || receivedData == "left" || receivedData == "stop" || receivedData == "auto" || receivedData == "eright" || receivedData =="qleft")
  {

    handleMotors(receivedData);
  }
  if(receivedData=="cw")
  { 
    servoAngle +=50;
    myservo.write(servoAngle);
    Serial.print("The angle of servo is ");
    Serial.println(servoAngle); 
    
  }
  if(receivedData=="ccw")
  {
    servoAngle -=50;
    myservo.write(servoAngle);
    Serial.print("The angle of servo is ");
    Serial.println(servoAngle); 
  
  }
  
}

void drawTrack()
{
  if(millis()-timer >1000){
   mpu.update();
   float val1 =mpu.getAngleZ();
   float val2 = calc_distance();
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
      lineFollower(line_error, angle_error);  
      break;
    case 'e':
       moveForwardRight(speed);
       break;
    case 'q':
       moveForwardLeft(speed);
       break;
  }
}
int handleIR(int IR_PIN) {
  return digitalRead(IR_PIN);
}

int motorControl(double prevSpeed, double actualSpeed)
{
  setPoint=prevSpeed;
  crError = setPoint - actualSpeed;

  output = Kp*crError;
  actualSpeed = crError;

  return output;
  
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
   updatedSpeed = motorControl(speed,calc_speed());
   analogWrite(MOTOR_RIGHT_FORWARD , updatedSpeed);
   analogWrite(MOTOR_RIGHT_BACKWARD , 0);
   analogWrite(MOTOR_LEFT_FORWARD , updatedSpeed);
   analogWrite(MOTOR_LEFT_BACKWARD , 0);
}
void moveBackward(int speed){
   Serial.println("MoveBackward");
   updatedSpeed = motorControl(speed,calc_speed());
   analogWrite(MOTOR_RIGHT_FORWARD , 0);
   analogWrite(MOTOR_RIGHT_BACKWARD , updatedSpeed);
   analogWrite(MOTOR_LEFT_FORWARD , 0);
   analogWrite(MOTOR_LEFT_BACKWARD , updatedSpeed);
}
void stopMotors() {
   Serial.println("Stopmotors");
   analogWrite(MOTOR_RIGHT_FORWARD , 0);
   analogWrite(MOTOR_RIGHT_BACKWARD , 0);
   analogWrite(MOTOR_LEFT_FORWARD , 0);
   analogWrite(MOTOR_LEFT_BACKWARD , 0);
}
void moveForwardRight(int speed)
{
   int s = speed/coeff;
   Serial.println("MoveForwardRight");
   analogWrite(MOTOR_RIGHT_FORWARD , s);
   analogWrite(MOTOR_RIGHT_BACKWARD , 0);
   analogWrite(MOTOR_LEFT_FORWARD , speed);
   analogWrite(MOTOR_LEFT_BACKWARD , 0); 
}
void moveForwardLeft(int speed)
{
   Serial.println("MoveForwardLeft");
   int s = speed/coeff;
   Serial.println(s);
   analogWrite(MOTOR_RIGHT_FORWARD , speed);
   analogWrite(MOTOR_RIGHT_BACKWARD , 0);
   analogWrite(MOTOR_LEFT_FORWARD , s);
   analogWrite(MOTOR_LEFT_BACKWARD , 0); 
   
}

float calc_speed()
{
  vel = wheelradius*((rpmL+rpmR)/2);
  return vel;
}
float calc_distance()
{
    vel = calc_speed();
    distance = (2*3.141*wheelradius)*(((counterL+counterR)/2)/slots)*vel;
    Serial.print("Distance = ");
    Serial.println(distance);
    return distance;
}
void lineFollower(int Line_error, int angle_error)
{

  while(Line_error<0 || angle_error<89)
  {
    moveForwardLeft(Line_speed);

    delay(1000);
  }
  while(Line_error>0 || angle_error>91)
  {
    moveForwardRight(Line_speed);
    delay(1000);
  }
  while(Line_error==0 || angle_error == 90)
  {
    moveForward(Line_speed);
     delay(1000);
  }
  
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
