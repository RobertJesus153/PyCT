const int Verde_1 = 2;
const int Verde_2 = 3;
const int Verde_3 = 4;
const int Rojo_1 = 5;
const int Rojo_2 = 6;
const int Rojo_3 = 7;
int h=0;
bool Jugador_1 = true;
bool Jugador_2 = true;
bool Jugador_3 = true;
int reset()
{
  digitalWrite(Verde_1,LOW);
  digitalWrite(Verde_2,LOW);
  digitalWrite(Verde_3,LOW);
  digitalWrite(Rojo_1,LOW);
  digitalWrite(Rojo_2,LOW);
  digitalWrite(Rojo_3,LOW);
  bool Jugador_1 = true;
  bool Jugador_2 = true;
  bool Jugador_3 = true;
  Serial.println("Reset");
  h=1;   
}
int win(int Verde,int Rojo)
{
  for (int i = 1;  i <= 7; i++){
    digitalWrite(Verde, HIGH);
    digitalWrite(Rojo, HIGH);
    delay(500);
    digitalWrite(Verde, HIGH);
    digitalWrite(Rojo, HIGH);
    delay(500);
  }  
}
int option_a()
{
  if (h==1)
      {
        Serial.println("h == 1");
        digitalWrite(Verde_1,LOW);
        digitalWrite(Rojo_1,LOW);
        if      (Jugador_2)  {digitalWrite(Verde_2,HIGH); h=2;}
        else if (Jugador_3)  {digitalWrite(Verde_3,HIGH); h=3;}
        else                 {win(Verde_1, Rojo_1); reset();}
      }
  else if (h==2)
      {
        Serial.println("h == 2");
        digitalWrite(Verde_2,LOW);
        digitalWrite(Rojo_2,LOW);
        if      (Jugador_3) {digitalWrite(Verde_3,HIGH); h=3;}
        else if (Jugador_1) {digitalWrite(Verde_1,HIGH); h=1;}
        else                {win(Verde_2, Rojo_2); reset();}
      }
  else if (h==3)
      {
        Serial.println("h == 3");
        digitalWrite(Verde_3,LOW);
        digitalWrite(Rojo_3,LOW);
        if      (Jugador_1) {digitalWrite(Verde_1,HIGH); h=1;}
        else if (Jugador_2) {digitalWrite(Verde_2,HIGH); h=2;}
        else                {win(Verde_3, Rojo_3); reset();}
      }
  else{ Serial.println("Error");}
}
void setup()
{
  Serial.begin(9600);          
  pinMode(Verde_1, OUTPUT);
  pinMode(Verde_2, OUTPUT);
  pinMode(Verde_3, OUTPUT);
  pinMode(Rojo_1, OUTPUT);
  pinMode(Rojo_2, OUTPUT);
  pinMode(Rojo_3, OUTPUT);
}
 
void loop()
{
  if (Serial.available()>0)
  {
    char option = Serial.read();
    if(option == 's'){digitalWrite(Verde_1,HIGH);h=1;}
    if(option == 'r'){reset();}
    if(option == 'a'){option_a();}  //La 'a' indica que la jugada es acertada, entonces le toca mover al siguiente
    if (option=='b')                //La 'b' indica que la jugada está mal hecha, por lo que el led rojo del que ha movido se enciende
    {
      if (h==1)
      {
        digitalWrite(Verde_1,LOW);
        digitalWrite(Rojo_1,HIGH);
      }
     else if (h==2)
      {
        digitalWrite(Verde_2,LOW);
        digitalWrite(Rojo_2,HIGH);
      }
     else if (h==3)
      {
        digitalWrite(Verde_3,LOW);
        digitalWrite(Rojo_3,HIGH);
      }
     else{ Serial.println("Error");}
    }
    if (option == 'x'){Jugador_1 = false; option_a();} //La 'x' indica que se ha hecho jaque mate a Jugador_1
    if (option == 'y'){Jugador_2 = false; option_a();} //La 'y' indica que se ha hecho jaque mate a Jugador_2
    if (option == 'z'){Jugador_3 = false; option_a();} //La 'z' indica que se ha hecho jaque mate a Jugador_3
    }}
