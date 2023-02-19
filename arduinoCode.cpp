#include <Servo.h>

Servo Lshoulder;
Servo Rshoulder;
Servo neckServo;
Servo headServo;



void setup() {
  Serial.begin(9600); // Set the baud rate
  Lshoulder.attach(3); 
  neckServo.attach(5);
  Rshoulder.attach(9);
  headServo.attach(10);

  Lshoulder.write(90); // Set the angle of the servo
  neckServo.write(90);
  Rshoulder.write(90);
  headServo.write(90);
  }

void loop() {
  if (Serial.available() >= 4) { // Wait until 2 bytes are received
    int NeckAngle = (Serial.read() << 8) | Serial.read(); // Combine two bytes to form an angle integer
    int LshoulderAngle = (Serial.read() << 8) | Serial.read();
    int RshoulderAngle = (Serial.read() << 8) | Serial.read();
    int headAngle = (Serial.read() << 8) | Serial.read();
    
    Lshoulder.write(LshoulderAngle/0.8); // Set the angle of the servo
    neckServo.write(NeckAngle/.8);
    Rshoulder.write(RshoulderAngle);
    headServo.write(headAngle);
  }
}
