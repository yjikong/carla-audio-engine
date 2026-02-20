import socket as udp
import json
import time

class Socket:
    def __init__(self):
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5005
        self.socket = udp.socket(udp.AF_INET, udp.SOCK_DGRAM)
    def publish_data(self, data_packet):
        message = json.dumps(data_packet).encode()
        self.socket.sendto(message, (self.UDP_IP, self.UDP_PORT))