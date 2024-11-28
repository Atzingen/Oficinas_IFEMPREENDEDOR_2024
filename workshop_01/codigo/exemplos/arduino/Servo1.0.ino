#include <Servo.h>

#define pinServo 7

Servo servo1;
int grau = 90;  // Ângulo inicial

void setup() {
  servo1.attach(pinServo);
  Serial.begin(9600);
  servo1.write(grau);  // Define o ângulo inicial do servo
  Serial.print("Angulo inicial: ");
  Serial.println(grau);
}

void loop() {
  // Verifica se há dados disponíveis no serial
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Lê a linha completa até o Enter
    
    // Verifica se a entrada é um número
    if (input.length() > 0 && input.toInt() != 0 || input == "0") {
      int novoGrau = input.toInt();

      // Verifica se o valor está dentro do intervalo aceitável
      if (novoGrau >= 0 && novoGrau <= 180) {
        grau = novoGrau;
        servo1.write(grau);
        Serial.print("Angulo: ");
        Serial.println(grau);
      }
    } else {
      Serial.println("Entrada invalida. Insira um numero entre 0 e 180.");
    }
  }

  delay(20);  // Pequeno atraso para suavizar a leitura
}
