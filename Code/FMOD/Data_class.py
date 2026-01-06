import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class Data:
    data_packet = None
    sock = None
    def Data():
        #Init Socket
        Data.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Data.sock.bind((UDP_IP, UDP_PORT))
    def decode():
        data, addr = Data.sock.recvfrom(2048)
        # JSON-String to dictionary
        Data.data_packet = json.loads(data.decode())
    def get_speed():
        speed = Data.data_packet["speed"]
        return speed
    def get_speed_limit():
        speed_limit = Data.data_packet["speed_limit"]
        return speed_limit
    def print_all():
        # .get(key, default_wert) verhindert den KeyError
        speed = Data.data_packet.get("speed", 0.0)
        speed_limit = Data.data_packet.get("speed_limit", 0.0)
        throttle = Data.data_packet.get("throttle", 0.0)
        brake = Data.data_packet.get("brake", 0.0)
        #message = Data.data_packet.get("message", "No Data")
        message = Data.data_packet["message"]

        print(f"S: {speed:6.2f} km/h | T: {throttle:.2f} | B: {brake:.2f} | L: {speed_limit:3f} | M: {message}", end='\r')