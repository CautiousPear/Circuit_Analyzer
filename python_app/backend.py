import time
import serial
from serial.tools import list_ports

class ArduinoCommunication:
    def __init__(self):
        self.serial_port = None

    def find_device(self): # Find Arduino and open serial connection
        for port in list_ports.comports():
            try:
                ser = serial.Serial(port.device, 500000, timeout=1)
                time.sleep(2)  # allow Arduino reset
                ser.reset_input_buffer()
                ser.write(b"OSCIL:PING\n")
                start_time = time.time()
                while time.time() - start_time < 3: # Wait 3 seconds for response 
                    if ser.in_waiting:
                        response = ser.readline().decode(errors="ignore").strip()
                        if response == "OSCIL:FOUND": # If a response bounces back, set as serial
                            self.serial_port = ser
                            print(f"OSCIL:Connected to Arduino on {port.device}")
                            return True
                ser.close()
            except Exception as e:
                print(f"OSCIL:{port.device} error: {e}")
        print("OSCIL:No Arduino found")
        return False

    def start_sampling(self):
        if self.serial_port:
            cmd = f"OSCIL:START\n"
            self.serial_port.write(cmd.encode())

    def stop_sampling(self):
        if self.serial_port:
            self.serial_port.write(b"OSCIL:STOP\n")

    def set_update_interval(self, update_interval):
        cmd = f"OSCIL:INTERVAL,{update_interval}\n"
        self.serial_port.write(cmd.encode())


    def read_data(self):
        """Return a single sample as (timestamp, voltage, current) or (None, None, None)."""
        samples = []
        while self.serial_port and self.serial_port.in_waiting:
            samples = []
            line = self.serial_port.readline().decode(errors="ignore").strip()
            if not line.startswith("D:"):
                continue
            line = line[2:]  # remove the first characters: "D:"
            print(line)
            if line:
                try:
                    parts = line.split(',')
                    timestamp = float(parts[0])
                    voltage = float(parts[1])
                    current = float(parts[2])

                    samples.append((timestamp, voltage, current))
                except Exception as e:
                    print(f"OSCIL:Failed to parse Arduino data: {line} ({e})")
        return samples