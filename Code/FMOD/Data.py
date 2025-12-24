import socket
import json

# Socket Setup
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Empfänger bereit auf Port {UDP_PORT}...")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        
        # JSON-String wieder in ein Dictionary umwandeln
        data_packet = json.loads(data.decode())
        
        # Jetzt kannst du auf die einzelnen Werte zugreifen
        speed = data_packet["speed"]
        throttle = data_packet["throttle"]
        brake = data_packet["brake"]
        
        print(f"S: {speed:6.2f} km/h | T: {throttle:.2f} | B: {brake:.2f}", end='\r')

except KeyboardInterrupt:
    print("\nEmpfänger gestoppt.")