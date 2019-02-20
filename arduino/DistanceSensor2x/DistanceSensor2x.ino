const int analog_sensor1 = A1;    
const int analog_sensor2 = A2;

int value_sensor1 = 0;
int value_sensor2 = 0;
int value2_sensor1 = 0;
int value2_sensor2 = 0;
int output_sensor1 = 0;
int output_sensor2 = 0;

String s;

void setup() {
  Serial.begin(9600);
  Serial.flush();
}

void loop() {
  s = "{\"sensor1\":";
  
  value_sensor1 = analogRead(analog_sensor1);
  value_sensor2 = analogRead(analog_sensor2);
  
  delay(50);
  
  value2_sensor1 = analogRead(analog_sensor1);
  value2_sensor2 = analogRead(analog_sensor2);

  output_sensor1 = (value_sensor1 + value2_sensor1) / 2;
  output_sensor2 = (value_sensor2 + value2_sensor2) / 2;

  if(output_sensor1 < 80 || output_sensor1 > 497)
  {
    output_sensor1 = -1;
  }
  if(output_sensor2 < 80 || output_sensor2 > 497)
  {
    output_sensor2 = -1;
  }

  s = s + output_sensor1;
  s = s + ",\"sensor2\":";
  s = s + output_sensor2;
  s = s + "}";

  Serial.println(s);
  Serial.flush();

  s = "";
  
  delay(50);
  
}
