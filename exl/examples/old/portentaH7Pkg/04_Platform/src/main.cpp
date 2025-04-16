#include <Arduino.h>
#include "RaPClient.h"

#/*
	Blink green LED using Portenta M7 Core
*/

const int ON = LOW; // Voltage level is inverted
const int OFF = HIGH;

//initiate RaPClient
RaPClient rapClient(Serial);

void setup() {
  bootM4(); // Boot M4 core
  pinMode(LEDG, OUTPUT); // Set green LED as output
  Serial.begin(9600);

  
  //log example
  rapClient.log('Microcontroller startup');

  //push example
  Flag Panomaly;
  Panomaly.value = false;
  
  if (rapClient.push('Panomaly',Panomaly)) {
        Serial.println("Item pushed successfully!");
    } else {
        Serial.println("Failed to push item.");
    }

}

void loop() {
  digitalWrite(LEDG, ON); // Turn green LED on
  delay(1000); // Wait for 1 second
  Serial.println("on");
  digitalWrite(LEDG, OFF); // Turn green LED off
  Serial.println("off");
  delay(1000);
}
