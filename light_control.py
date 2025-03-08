import serial
import serial.tools.list_ports
import time

def list_all_ports():
    global com_port
    ports = serial.tools.list_ports.comports()
    print(ports)
    if len(ports) == 0:
        print("Žádné porty nebyly nalezeny.")
    else:
        print("Nalezené porty:")
        for port in ports:
            com_port = port.device
            print(port)
            print(f"Port: {com_port}, Zařízení: {port.description}")
            # Check for known ports; adjust these as needed for your system
            if com_port == "/dev/ttyUSB1":
                return "/dev/ttyUSB1"
            elif com_port == "/dev/ttyS0":
                return "/dev/ttyUSB0"

def turn_on_power(port):
    with serial.Serial(port, 9600, timeout=1) as ser:
        ser.write(b'on')  # Příkaz pro zapnutí napájení
    ser.close()

def turn_off_power(port):
    with serial.Serial(port, 9600, timeout=1) as ser:
        ser.write(b'off')  # Příkaz pro vypnutí napájení
    ser.close()

turn_off_power("/dev/ttyUSB0")
"""print(list_all_ports())
try:
    while True:
        turn_on_power("/dev/ttyUSB0")
        print("on")
        time.sleep(20)
        turn_off_power("/dev/ttyUSB0")
        print("off")
        time.sleep(20)
except Exception:
    print("Nebylo možné nalézt jakákoliv zařízení s názvem /dev/ttyUSB0 nebo /dev/ttyUSB1")"""