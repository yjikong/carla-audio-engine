import socket as udp
import json
from Code.CARLA.Classes.CarlaClient import *
from Code.CARLA.Classes.CollisionSensor import *

class Socket:
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    socket = None
    def __init__(self):
        self.socket = udp.socket(udp.AF_INET, udp.SOCK_DGRAM)
    def publish_data(self, data_packet):
        message = json.dumps(data_packet).encode()
        self.socket.sendto(message, (self.UDP_IP, self.UDP_PORT))


if __name__ == '__main__':
    client = CarlaClient('localhost', 2000, 10.0)
    client.connect()

    sock = Socket()

    while True:
        data_packet = client.retrieve_data()
        sock.publish_data(data_packet)
        time.sleep(0.05)