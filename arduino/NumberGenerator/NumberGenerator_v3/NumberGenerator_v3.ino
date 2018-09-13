const double MIN_RANGE = 753.28f;
const double MAX_RANGE = 754.41f;

const double MAX_STEP = 0.9;
boolean up; 
double num;
String response;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  num = 0.0f;
}

void loop() {
  // put your main code here, to run repeatedly:
  num = random(MIN_RANGE, MAX_RANGE);
  for(int i =0; i < 10; i++){
    response = String(num + (i*.031));
    Serial.println(response);
    delay(300);
  }
  for(int i =0; i < 10; i++){
    response = String(num - (i*.031));
    Serial.println(response);
    delay(300);
  }
}
