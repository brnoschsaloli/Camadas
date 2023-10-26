const int pin = 13;
const int baudrate = 9600;
const long t = 1000000L/baudrate;
bool erroP = false;

void setup() {
  pinMode(pin, INPUT);
  Serial.begin(9600);

  while(true){
    if(digitalRead(pin) == LOW){
      delayMicroseconds(t);
      byte b = recieveData();
      Serial.println(b, BIN);
      Serial.println("--------------------------------------------------------------------------");
    }
    
  }
}

byte recieveData(){
  byte data = 0;
  int parityBit = 0;
  int parityRecieved = 0;
  int stopBit = 0;
  delayMicroseconds(t);

  for (int i=0;i<10;i++){
    int v = digitalRead(pin);
    if (i < 8){
      parityBit ^= (v & 1);
      data |=  (v << i);
    }else if(i == 8){
      parityRecieved = v;
    }else if(i==9){
      stopBit = v;
    }
    delayMicroseconds(2.5*t);

  }
  
  Serial.println("parityRecieved:");
  Serial.println(parityRecieved);
  Serial.println("parityBit:");
  Serial.println(parityBit);
  Serial.println("stopbit:");
  Serial.println(stopBit);
  
  if (parityBit == parityRecieved){
    Serial.println("----------------------------paridade ok!--------------------------------");
  }else{
    Serial.println("----------------------------erro de paridade!-----------------------------");
    erroP = true;
  }
  delayMicroseconds(t);

  return data;
}

void loop() {
}
