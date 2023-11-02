#include <Stepper.h>

const int steps_per_rev = 400; //Set to 200 for NEMA 17
#define IN1 14
#define IN2 32
#define IN3 15
#define IN4 33

Stepper motor(steps_per_rev, IN1, IN2, IN3, IN4);


void setup()
{
  motor.setSpeed(60);
  Serial.begin(115200);
}

void loop() 
{
  Serial.println("Rotating Clockwise...");
  motor.step(steps_per_rev);
  delay(500);

  Serial.println("Rotating Anti-clockwise...");
  motor.step(-steps_per_rev);
  delay(500);
}