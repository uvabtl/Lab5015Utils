#include <Stepper.h>

// Define number of steps per revolution:
const int stepsPerRevolution = 200;
const int actualStepsPerRev = 12800;

//const int stepsPerRevolution = 3200;
//const int actualStepsPerRev = 3200*4;

#define dirA 3
#define dirB 6

//#define dirA 2
//#define dirB 3

// Initialize the stepper library on the motor shield:
Stepper myStepper = Stepper(stepsPerRevolution, dirA, dirB);



const int maxDeltaAngle = 90;


void setup() 
{
  Serial.begin(115200);
  Serial.setTimeout(1);
  
  // Set the motor speed (RPMs):
  myStepper.setSpeed(10);
  Serial.println("Starting...");
}

int fromPosToAngle (int Pos)
{
  int this_angle = int(Pos/actualStepsPerRev*360.);
  return this_angle;
}

int fromAngleToPos (int Angle)
{
  //Serial.println(Angle);
  //Serial.println(actualStepsPerRev);
  //Serial.println(int(float(Angle)/360.));
  //Serial.println(float(Angle)/360.*float(actualStepsPerRev));
  
  int this_pos = int64_t(round(float(Angle)/360.*float(actualStepsPerRev)));
  //Serial.println(this_pos);
  return this_pos;
}

void loop() 
{

  while (!Serial.available());

  delay(200);
  int deltaAngle   = Serial.readString().toInt();
  int deltaPos = fromAngleToPos(deltaAngle);

  Serial.print("Received target delta angle: ");
  Serial.println(deltaAngle);
  Serial.print("Moving for nsteps: ");
  Serial.println(deltaPos);
  
  delay(200);

  if (abs(deltaAngle)<maxDeltaAngle) 
  {
    myStepper.step(deltaPos);
    Serial.println("Rotation completed");
  }
  else
  {
    Serial.println("Delta angle out of allowed range");
  }
  delay(200);

}