# Python / Graph Interface

## Requirements
* **Python 3.14+**
* **PySide6**
* **pyqtgraph**
* Other dependencies listed in `requirements.txt`


## Installation & Setup

### Option A: Run from pre-built executable

1. Download `CircuitAnalyzer.zip` from the [Releases]() page.

2. Extract the folder.

3. Run `CircuitAnalyzer.exe`.

### Option B: Run from source

1. **Create and activate a virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

2. Install Dependencies
```bash
pip install -r python_app/requirements.txt
```

3. Launch the app
```bash
python python_app/app.py
```


# Arduino Library

## Installation

1. Copy the CircuitAnalysis folder from CircuitAnalysisLib/ into your Arduino IDE libraries/ folder.

2. Restart the Arduino IDE.

3. Include the library in your sketch: 
```
#include <CircuitAnalysis.h>
```


# Usage Notes

- To measure current, you MUST have a shunt resistor (Low value resistor, typically ~10Ω). This is used to measure voltage drop without knowing the circuit's resistance.
Further Info: [Measuring Current using Shunt Resistors](https://www.tek.com/en/blog/measuring-current-using-shunt-resistors)

- Voltage can still be measured without the use of a shunt resistor by passing 0 as the shunt resistor value.

- The Python app communicates with the Arduino via Serial, detected automatically. Ensure your Arduino is connected and using the correct COM port.

- The Arduino sketch `example.ino` MUST be **non-blocking** in order to send data over Serial.

- Samples are sent to the Python script in CSV format: timestamp,<voltage,current
