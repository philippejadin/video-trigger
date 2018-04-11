void setup() 
{
  Serial.begin(9600);              //Starting serial communication
  pinMode(LED_BUILTIN, OUTPUT);
}



void loop() 
{

  Serial.println("play fr.h264");
  digitalWrite(LED_BUILTIN, HIGH);
  delay(5000);

  Serial.println("stop");
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);

  Serial.println("play nl.h264");
  digitalWrite(LED_BUILTIN, HIGH);
  delay(5000);

  Serial.println("stop");
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);


  Serial.println("play en.h264");
  digitalWrite(LED_BUILTIN, HIGH);
  delay(5000);

  Serial.println("stop");
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);




}



