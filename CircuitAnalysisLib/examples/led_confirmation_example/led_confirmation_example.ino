#include <CircuitAnalysis.h>

// Create the analyzer object
// A0 = analog pin to measure
// 10.0 = shunt resistor in ohms
CircuitAnalysis analyzer(A0, 10.0);

void setup() {
  // Optional: LED to show connection status
  pinMode(LED_BUILTIN, OUTPUT);

  // Start the analyzer (starts Serial)
  analyzer.begin(9600);
}

void loop() {
  // Keep the analyzer running
  analyzer.update();

  // Optional: react to connection state
  if (analyzer.isConnected()) {
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
