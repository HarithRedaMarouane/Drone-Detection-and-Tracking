#include <ESP32Servo.h>

Servo servoX, servoY;
int servoPinX = 19;  // X Axis
int servoPinY = 18;  // Y Axis
const int BUFFER_SIZE = 50;
char inputBuffer[BUFFER_SIZE];

const int MIN_Y = 0;  // Min for Y Axis
const int MAX_Y = 180; // Max for Y Axis
const int MIN_X = 0;   // Min for X Axis
const int MAX_X = 180; // Max for X Axis

int currentAngleX = 90;
int currentAngleY = 90;

// Proportional control factors
float kpX = 0.1; // Proportional gain for X. Tune this value.
float kpY = 0.1; // Proportional gain for Y. Tune this value.

const int CENTER_DEADZONE_RADIUS = 5; // Center deadzone radius in degrees
const int SLOW_ZONE_RADIUS = 10; // Slow zone radius in degrees

void setup() {
  servoX.attach(servoPinX);
  servoY.attach(servoPinY);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    int bytesRead = Serial.readBytesUntil('\n', inputBuffer, BUFFER_SIZE - 1);
    inputBuffer[bytesRead] = 0;

    String inputStr = String(inputBuffer);
    int commaIndex = inputStr.indexOf(',');
    int targetAngleX = inputStr.substring(0, commaIndex).toInt();
    int targetAngleY = inputStr.substring(commaIndex + 1).toInt();

    targetAngleX = constrain(targetAngleX, MIN_X, MAX_X);
    targetAngleY = constrain(targetAngleY, MIN_Y, MAX_Y);

    int errorX = targetAngleX - currentAngleX;
    int errorY = targetAngleY - currentAngleY;

    // Check if the object is within the dead zone
    if (abs(errorX) > CENTER_DEADZONE_RADIUS || abs(errorY) > CENTER_DEADZONE_RADIUS) {
      // Apply proportional control based on the zone
      float controlX = kpX * errorX;
      float controlY = kpY * errorY;

      // If the object is in the slow zone, reduce the control signal
      if (sqrt(sq(errorX) + sq(errorY)) < SLOW_ZONE_RADIUS) {
        controlX *= 0.5;
        controlY *= 0.5;
      }

      // Update the servo positions
      currentAngleX += controlX;
      currentAngleY += controlY;

      // Constrain the angles to prevent over-driving the servos
      currentAngleX = constrain(currentAngleX, MIN_X, MAX_X);
      currentAngleY = constrain(currentAngleY, MIN_Y, MAX_Y);
    }

    // Write the new angles to the servos
    servoX.write(currentAngleX);
    servoY.write(currentAngleY);
  }
}
