const double START = 753.28f;
const double END = 754.41f;
const double RANGE = 1.13f;
const double STEP = 0.015f;
String response;
double num;
boolean up;

void setup() {
  Serial.begin(9600);
  num = 0.0f;
}

void loop() {

  if(num < 0){
    up = false;
  }else{
    if (num > RANGE){
      up = true;
    }
  }

  if(up){
    num -= STEP;
  }else{
    num += STEP;
  }
  response = String(START + num);
  Serial.println(response);
  delay(500);
}
