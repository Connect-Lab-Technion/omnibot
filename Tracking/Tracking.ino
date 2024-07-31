#include <Servo.h>
String inputString;

Servo left_right;
Servo up_down;

int theta_x = 90;
int theta_y = 90;

void setup()
{
  left_right.attach(9);
  up_down.attach(6);
  left_right.write(theta_x);
  up_down.write(theta_y);
  Serial.begin(9600);
}


void loop()
{
  while(Serial.available())
  {
    inputString = Serial.readStringUntil('\r');
    Serial.println(inputString);
    int x_axis = inputString.substring(0, inputString.indexOf(',')).toInt();
    int y_axis = inputString.substring(inputString.indexOf(',') + 1).toInt();
    
    if (abs(320-x_axis) > 30){
      if(x_axis > 320){
        theta_x -= (1 + (12*abs(320-x_axis))/320);
        left_right.write(theta_x);
      }
      else{
        theta_x += (1 + (12*abs(320-x_axis))/320);
        left_right.write(theta_x);
      }
    }
    if (abs(240-y_axis) > 20){
      if(y_axis > 240){
        theta_y -= (1 + (8*abs(240-y_axis))/240);
      }
      else{
        theta_y += (1 + (8*abs(240-y_axis))/240);
      }
      if (theta_y > 145){
        up_down.write(145);
      }
      else if (theta_y < 50){
        up_down.write(50);
      }
      else {
        up_down.write(theta_y);
      }
    }
  }
}
