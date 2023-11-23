#include <Stepper.h>

const int steps = 400; //Set to 200 for NEMA 17
const int d = 445; //Distancia en milímetros
bool FlagI = false;
String error = "";

//Actuadores
int actuador = 17;
int iman = 16;

// Motor A
#define IN1A 14
#define IN2A 32
#define IN3A 15
#define IN4A 33

// Motor B
#define IN1B 21
#define IN2B 13
#define IN3B 12
#define IN4B 27

Stepper motorA(steps, IN1A, IN2A, IN3A, IN4A);
Stepper motorB(steps, IN1B, IN2B, IN3B, IN4B);


void setup()
{
  Serial.begin(9600); // Set the baud rate to match the Raspberry Pi
  pinMode(actuador, OUTPUT);
  pinMode(iman, OUTPUT);
  motorA.setSpeed(60);
  motorB.setSpeed(60);

  /*Secuencia de prueba
  digitalWrite(actuador, HIGH);
  delay(5000);
  digitalWrite(iman, HIGH);
  delay(1000);
  digitalWrite(actuador, LOW);
  delay(5000);
  motorA.step(2*d);
  motorB.step(-d);
  motorA.step(d);
  delay(500)
  digitalWrite(actuador, HIGH);
  delay(5000);
  digitalWrite(iman, LOW);
  delay(1000);
  digitalWrite(actuador, LOW);
  delay(5000);
  */  
}

void loop() {
  
  if (Serial.available() > 0) {

    String instruccion = Serial.readStringUntil('\n');
    
    switch (instruccion.toInt()) {

      // Lógica para el movimiento en los dos ejes
      
      case 0:
        //Serial.println("No mueve");
        break;
      case 1:
        //Movimiento en x+
        motorA.step(d);
        break;
      case 2:
        //Movimiento en x-
        //Serial.println("x-");
        motorA.step(-d);
        break;     
      case 3:
        //Movimiento en y+
        //Serial.println("y+");
        motorB.step(-d);
        break;
      case 4:
        //Movimiento en y-
        //Serial.println("y-");
        motorB.step(d);
        break;
        
      // Lógica para el funcionamiento de actuador e imán
      
      case 5:
        // Se baja el actuador
        digitalWrite(actuador, HIGH);
        delay(3000);

        // Se verifica si se está recogiendo o dejando
        if (FlagI){
          digitalWrite(iman, LOW);
          delay(500); 
          FlagI = false;
        } 
        else{
          digitalWrite(iman, HIGH);
          delay(500);
          FlagI = true;
        }
        
        // Se sube el actuador
        digitalWrite(actuador, LOW);
        break;
              
      default:
        error = ("Código desconocido:" + String(instruccion) + "FIN");
        Serial.println(error);  
    }
    Serial.println(instruccion); 
  }
}
