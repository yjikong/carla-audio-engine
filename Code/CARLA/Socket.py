import socket as udp
import json
from Classes.Carla_client_class import *

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

    sock = socket.socket()

    while True:
        data_packet = CarlaClient.retrieve_data()
        socket.publish_data(sock, data_packet)

        #Nur für Test der Carla_client_class:
        #Print data
        speed = data_packet["speed"]
        speed_limit = data_packet["speed_limit"]
        throttle = data_packet["throttle"]
        brake = data_packet["brake"]
        message = data_packet["message"]
        collision_event = data_packet.get("collision_event" "None")

        print(f"S: {speed:6.2f} km/h | T: {throttle:.2f} | B: {brake:.2f} | L: {speed_limit:3f} | M: {message}", end='\r')