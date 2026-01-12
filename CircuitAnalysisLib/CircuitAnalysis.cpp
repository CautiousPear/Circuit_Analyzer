/*
  CircuitAnalysis.cpp - Library for sending voltage and current readings across a circuit.
  Created by CautiousPear, January 12, 2026.
  Updated by CautiousPear, January 12, 2026.
  Released into the public domain.
*/

#include "CircuitAnalysis.h"

/* ----------------------------
  Constructor
*/
CircuitAnalysis::CircuitAnalysis(int analogPin, float shuntOhms)
{
  sensePin_ = analogPin;
  shuntResistor_ = shuntOhms;

  sampleInterval_ms_ = 10; // 500 ms default
  lastSampleTime_ms_ = 0;
  startTime_ms_ = 0;
  sendingData_ = false;
  handshakeDone_ = false;
}

/* ----------------------------
  Begin (called from setup)
*/
void CircuitAnalysis::begin()
{
  Serial.begin(500000);
}

/* ----------------------------
  Update (called from loop)
*/
void CircuitAnalysis::update()
{
  // Wait for handshake before doing anything else
  if (!handshakeDone_)
  {
    handshakeDone_ = checkHandshake_();
    return;
  }

  // Handle incoming commands
  processCommand_();

  // Periodic data sampling
  if (sendingData_ && millis() - lastSampleTime_ms_ >= sampleInterval_ms_)
  {
    lastSampleTime_ms_ = millis();
    sendData_();
  }
}

/* ----------------------------
  Public status query
*/
bool CircuitAnalysis::isConnected()
{
  return handshakeDone_;
}

/* ----------------------------
  Receive ping request to verify port
*/
bool CircuitAnalysis::checkHandshake_()
{
  if (Serial.available())
  {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "OSCIL:PING")
    {
      Serial.println("OSCIL:FOUND");
      return true;
    }
  }
  return false;
}

/* ----------------------------
  Command processing
*/
void CircuitAnalysis::processCommand_()
{
  if (Serial.available())
  {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // START
    if (cmd == "OSCIL:START")
    {
      sendingData_ = true;
      startTime_ms_ = millis();
      Serial.println("OSCIL:STARTED");
    }
    // STOP
    else if (cmd == "OSCIL:STOP")
    {
      sendingData_ = false;
      Serial.println("OSCIL:STOPPED");
    }
    else if (cmd.startsWith("OSCIL:INTERVAL,"))
    {
      int commaIndex = cmd.indexOf(',');
      if (commaIndex != -1)
      {
        unsigned long interval_ = cmd.substring(commaIndex + 1).toInt();
        if (interval_ > 0)
        {
          sampleInterval_ms_ = interval_;
          Serial.print("OSCIL:INTERVAL SET ");
          Serial.println(sampleInterval_ms_);
        }
      }
    }
    else if (cmd.startsWith("OSCIL:BAUD,"))
    {
      int commaIndex = cmd.indexOf(',');
      if (commaIndex != -1)
      {
        unsigned int customBaud_ = cmd.substring(commaIndex + 1).toInt();
        Serial.print("OSCIL:BAUD SET ");
        Serial.println(customBaud_);
        Serial.end();
        Serial.begin(customBaud_);
      }
    }
  }
}
/* ----------------------------
  Data transmission
*/
void CircuitAnalysis::sendData_()
{
  int rawVolts = analogRead(sensePin_);
  float voltage = rawVolts * (5.0 / 1023.0);
  float current = 0.0;
  if (shuntResistor_ > 0)
  {
    current = voltage / shuntResistor_;
  }
  unsigned long time = millis() - startTime_ms_;

  Serial.print("D:");
  Serial.print(time);
  Serial.print(",");
  Serial.print(voltage, 3);
  Serial.print(",");
  Serial.println(current, 3);
}
