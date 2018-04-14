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

// Motors
Servo aServo;
Servo bServo;
// Packets
char newChar;
bool readNum = false;
int packetSlot = 100;
char servoId;
int servoPosition;
int servoAdd;
// Simultaneous motor control
bool writeServos = false;
int aPosition;
int bPosition;
int aPrevPosition = 5; // Also initial position
int bPrevPosition = 95; // Also initial position

void setup() {
  Serial.begin(9600);
  aServo.attach(9);
  bServo.attach(10);
  aServo.write(aPrevPosition);
  bServo.write(bPrevPosition);
}

void loop() {
  // If packet has been received for a and b, write
  if (writeServos == true) {
    writeServoPosition();
  } else {
    recvInstruction();
  }
}

// Read the data chars and construct packets
void recvInstruction() {
  if (Serial.available() > 0) {
    newChar = Serial.read();
    // Packet end: z
    if (newChar == 'z') {
      readNum = false;
      packetSlot = 100;
      if (servoId == 'a') {
        aPosition = servoPosition;
      }
      if (servoId == 'b') {
        bPosition = servoPosition;
        writeServos = true;      
      }
    }
    // Servo position
    if (readNum == true) {
      servoPosition += packetSlot * int(newChar-'0');
      packetSlot = packetSlot/10;
    }
    // Packet begin: servo id
    if (newChar == 'a' || newChar == 'b') {
      servoId = newChar;
      readNum = true;
      servoPosition = 0;
    }
  }
}

// Write the servo position received
void writeServoPosition() {
  if (aPrevPosition < aPosition) {
    aPrevPosition++;
    aServo.write(aPrevPosition);
  }
  else if (aPrevPosition > aPosition) {
    aPrevPosition--;
    aServo.write(aPrevPosition);
  }
  if (bPrevPosition < bPosition) {
    bPrevPosition++;
    bServo.write(bPrevPosition);
  }
  else if (bPrevPosition > bPosition) {
    bPrevPosition--;
    bServo.write(bPrevPosition);
  }
  if (aPrevPosition == aPosition && bPrevPosition == bPosition) {
    writeServos = false;
    Serial.println(aPosition);
    Serial.println(bPosition);
  }
}
