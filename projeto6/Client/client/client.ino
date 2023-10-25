int pino = 13;
byte b = 0b11110000;
int start = 0;
int stop = 1;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pino, OUTPUT);
  digitalWrite(pino, HIGH);

  
}
void loop() {
  // put your main code here, to run repeatedly:
  sendData();
  delay(1000);
}

void sendData(){
  byte parityBit = 0;
  digitalWrite(pino, start);
  Serial.print("enviou start \n");
  delayMicroseconds((1000000L / 9600));

  for (int i = 0; i < 8; i++) {
    // Use o operador >> para deslocar o bit desejado para a posição 0 (o bit menos significativo)
    byte bit = (b >> i) & 1;
    
    // Agora, 'bit' contém o valor do bit que você deseja
    digitalWrite(pino, bit & 1 ? HIGH : LOW);
    String minhaString = "Enviou o bit: " + String(bit) + "\n";
    Serial.print(minhaString);
    delayMicroseconds((1000000L / 9600));
    parityBit ^= (bit & 1);
  }

  digitalWrite(pino, parityBit ? HIGH: LOW);
  String minhaString = "Enviou paridade: " + String(parityBit) + "\n";
  Serial.print(minhaString);
  delayMicroseconds((1000000L / 9600));

  digitalWrite(pino, HIGH);
  Serial.print("enviou stop \n");
}
