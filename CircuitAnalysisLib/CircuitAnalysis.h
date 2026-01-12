/*
  CircuitAnalysis.h - Library for sending voltage and current readings across a circuit.
  Created by CautiousPear, January 12, 2026.
  Updated by CautiousPear, January 12, 2026.
  Released into the public domain.
*/

#ifndef CIRCUIT_ANALYSIS_H
#define CIRCUIT_ANALYSIS_H

#include <Arduino.h>

class CircuitAnalysis
{
public:
  // Constructor
  CircuitAnalysis(int analogPin, float shuntOhms);

  // Library lifecycle
  void begin();
  void update();      // Call repeatedly from loop()
  bool isConnected(); // Communications port status

private:
  // Configuration
  int sensePin_;
  float shuntResistor_;

  // Timing
  unsigned long sampleInterval_ms_;
  unsigned long lastSampleTime_ms_;
  unsigned long startTime_ms_;

  // State flags
  bool sendingData_;
  bool handshakeDone_;

  // Internal helpers
  bool checkHandshake_();
  void processCommand_();
  void sendData_();
};

#endif
