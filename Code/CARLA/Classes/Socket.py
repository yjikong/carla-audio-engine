import socket as udp
import json
import time

class Socket:
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    socket = None
    def __init__(self):
        self.socket = udp.socket(udp.AF_INET, udp.SOCK_DGRAM)
    def publish_data(self, data_packet):
        message = json.dumps(data_packet).encode()
        self.socket.sendto(message, (self.UDP_IP, self.UDP_PORT))