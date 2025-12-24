import socket as udp
import json
from Carla_client_class import *

class socket:
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    def socket():
        sock = udp.socket(udp.AF_INET, udp.SOCK_DGRAM)
        return sock
    def publish_data(sock, data_packet):
        message = json.dumps(data_packet).encode()
        sock.sendto(message, (socket.UDP_IP, socket.UDP_PORT))
        time.sleep(0.05)


if __name__ == '__main__':
    #connect and get data
    CarlaClient.CarlaClient('localhost', 2000, 10.0)
    CarlaClient.connect()
    while True:
        data_packet = CarlaClient.retrieve_data()
        socket.publish_data(socket.socket(), data_packet)