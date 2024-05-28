int val;
int tempPin=1; // la ce pin e conectat senzorul de temperatura
int pinLED=8;

void setup()
{
  Serial.begin(9600);
   // Setam pinul LED ca pin de iesire
  pinMode(pinLED, OUTPUT);
}

void loop()
{
  val = analogRead(tempPin);
	 // convertim la grade Celsius
  float temperature = (val * 5.0 * 100.0) / 1024.0;
  Serial.print("TEMPERATURE: ");
  Serial.print(temperature);
  
  if (Serial.available() > 0) { // verifica daca primeste ceva prin interfata seriala
    char comanda = Serial.read();

    // Verificam comanda primita si controlam LED-ul corespunzator
    if (comanda == 'A') {
      digitalWrite(pinLED, HIGH); // Aprindem LED-ul
      
    } else if (comanda == 'S') {
      digitalWrite(pinLED, LOW); // Stingem LED-ul
    }
  }

}