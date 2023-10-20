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
  byte parityBit = 0;

  delayMicroseconds(t);

  for (int i=0;i<8;i++){
    int v = digitalRead(pin);
    parityBit ^= (v & 1);
    data |=  (v << i);
    delayMicroseconds(31*t);
    Serial.println("bit: ");
    Serial.println(digitalRead(pin));
  }
  int parityRecieved = digitalRead(pin);
  Serial.println("parityRecieved:");
  Serial.println(parityRecieved);
  Serial.println("parityBit:");
  Serial.println(parityBit);
  if (parityBit == parityRecieved){
    
    
    Serial.println("---------------------paridade ok!--------------------------");
  }else{
    Serial.println("---------------------erro de paridade!----------------------");
    erroP = true;
  }

  
  int stopBit = 0;
  while(stopBit == 0){
    stopBit = digitalRead(pin);      // espera o stopbit
  }
  
  delayMicroseconds(t);

  return data;
}

void loop() {
}
