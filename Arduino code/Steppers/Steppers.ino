// Include the AccelStepper Library
#include <AccelStepper.h>

#define motorInterfaceType 1

// Define pin connections
const int dirPin1 = 3;
const int stepPin1 = 4;
const int dirPin2 = 8;
const int stepPin2 = 9;
int stepsPerRevolution = 200;
const int magnet = 6;

int times = 0;

AccelStepper myStepper1(motorInterfaceType, stepPin1, dirPin1);
AccelStepper myStepper2(motorInterfaceType, stepPin2, dirPin2);

void setup() {
	// set the maximum speed, acceleration factor,
	// initial speed and the target position

  myStepper1.setMaxSpeed(100);
	myStepper1.setAcceleration(50);
	myStepper1.setSpeed(50);
	myStepper1.moveTo(200);

  myStepper2.setMaxSpeed(100);
	myStepper2.setAcceleration(50);
	myStepper2.setSpeed(50);
	myStepper2.moveTo(-200);

  pinMode(magnet, OUTPUT);
  digitalWrite(magnet, LOW);

}

void loop() {
    // Wait 1 second before starting loop
  if (times == 0){
    delay(1000);
    times ++;
  }
  if (myStepper1.distanceToGo() == 0) 
		myStepper1.moveTo(-myStepper1.currentPosition());

	// Move the motor one step
	myStepper1.run();

  if (myStepper2.distanceToGo() == 0) 
		myStepper2.moveTo(-myStepper2.currentPosition());

	// Move the motor one step
	myStepper2.run();

  digitalWrite(magnet, LOW);
}