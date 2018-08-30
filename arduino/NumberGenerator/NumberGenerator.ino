
const double OFFSET = 700.00;
const double RANGE = 600.00;
//random incrementor
const double STEP = 19.61;

bool up = true;
String response;
double num;

void setup(){
  Serial.begin(9600);
  num = 0.0;
}

void loop(){
  /*
    Check if buffer got some data
  */
  // if (Serial.available()) c_str[i++] = Serial.read();
  // if (i == 5){
  //  i = 0;
  //  Serial.write(c_str);
  // }
  if(num < 0){
    up = false;
  }
  if (num > RANGE){
    up = true;
  }
  if(up){
    num -= STEP;
  }else{
    num += STEP;
  }
  response = String(OFFSET + num);
  Serial.println(response);
  delay(500);
}