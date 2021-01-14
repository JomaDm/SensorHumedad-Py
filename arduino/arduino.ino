int val [] = {0,0,0,0,0,0,0,0};
void setup() {  
  Serial.begin(9600);    
  pinMode(10,INPUT);
  pinMode(9,INPUT);
  pinMode(8,INPUT);
  pinMode(7,INPUT);
  pinMode(6,INPUT);
  pinMode(5,INPUT);
  pinMode(4,INPUT);
  pinMode(3,INPUT);
}

void loop() {  
  if(!Serial.available()){
    val[0] = digitalRead(10);
    val[1] = digitalRead(9);
    val[2] = digitalRead(8);
    val[3] = digitalRead(7);
    val[4] = digitalRead(6);
    val[5] = digitalRead(5);
    val[6] = digitalRead(4);
    val[7] = digitalRead(3);  
    Serial.print(val[0]);
    Serial.print(val[1]);
    Serial.print(val[2]);
    Serial.print(val[3]);
    Serial.print(val[4]);
    Serial.print(val[5]);
    Serial.print(val[6]);
    Serial.print(val[7]);
    Serial.println();
    delay(5);  
  }  
}
