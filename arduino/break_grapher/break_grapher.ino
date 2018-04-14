// Read pyserial input and set the servos accordingly
// Packet example 'a007z'
//  where a is the servo id
//  007 is the servo position
//  z is the end of packet signal
// NOTE: Do not open serial monitor until after starting pyserial
// Pins:
//        Servo a = D9
//        Servo b = D10

#include <Servo.h>

Servo aServo;
Servo bServo;
char newChar;
bool readNum = false;
int packetSlot = 100;
boolean newData = false;
char servo_id;
int servo_position;
int servo_add;

void setup() {
  Serial.begin(9600);
  aServo.attach(9);
  bServo.attach(10);
}

void loop() {
  recvInstruction();
  if (newData == true) {
    showNewData();
    //writeServoPosition();
  }
}

// Read the data chars and construct packets
void recvInstruction() {
  if (Serial.available() > 0) {
    newChar = Serial.read();
    // Packet end: z
    if (newChar == 'z') {
      readNum = false;
      newData = true;
      packetSlot = 100;
    }
    // Servo position
    else if (readNum == true) {
      servo_add = packetSlot * int(newChar-'0');
      servo_position += servo_add;
      packetSlot = packetSlot/10;
    }
    // Packet begin: servo id
    else if (newChar == 'a' || newChar == 'b') {
      servo_id = newChar;
      readNum = true;
      servo_position = 0;
    }
  }
}

// Confirm we got things right
void showNewData() {
    Serial.println(servo_id);
    Serial.println(servo_position);
    //Serial.println(servo_id);
    //Serial.println(servo_position);
    newData = false;
}

// Write the servo position received
void writeServoPosition() {
  if (servo_id == "a") {
    aServo.write(servo_position);
  }
  else if (servo_id == "b") {
    bServo.write(servo_position);
  }
  else {
    Serial.println("ERROR: Invalid servo id");
  }
  newData = false;
}
