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
        data, addr = Data.sock.recvfrom(1024)
        # JSON-String to dictionary
        Data.data_packet = json.loads(data.decode())
    def get_speed():
        speed = Data.data_packet["speed"]
        return speed
    def get_speed_limit():
        speed_limit = Data.data_packet["speed_limit"]
        return speed_limit
    def print_all():
        speed = Data.data_packet["speed"]
        speed_limit = Data.data_packet["speed_limit"]
        throttle = Data.data_packet["throttle"]
        brake = Data.data_packet["brake"]

        print(f"S: {speed:6.2f} km/h | T: {throttle:.2f} | B: {brake:.2f} | L: {speed_limit:3f}", end='\r')