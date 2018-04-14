// Read pyserial input and set the servos accordingly
// NOTE: Do not open serial monitor until after starting pyserial
char receivedChar;
boolean newData = false;

void setup() {
  Serial.begin(9600);
}

void loop() {
  recvOneChar();
  showNewData();
}

void recvOneChar() {
  if (Serial.available() > 0) {
    receivedChar = Serial.read();
    newData = true;
  }
}

void showNewData() {
  if (newData == true) {
    Serial.println(receivedChar);
    newData = false;
  }
}


