import socket as udp
import json
from Classes.Carla_client_class import *
from Classes.Collision_sensor import *

class socket:
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    socket = None
    def __init__(self):
        self.socket = udp.socket(udp.AF_INET, udp.SOCK_DGRAM)
    def publish_data(self, data_packet):
        message = json.dumps(data_packet).encode()
        self.socket.sendto(message, (self.UDP_IP, self.UDP_PORT))
        time.sleep(0.05)


if __name__ == '__main__':
    #connect and get data
    #CarlaClient.CarlaClient('localhost', 2000, 10.0)
    #CarlaClient.connect()
    client = CarlaClient('localhost', 2000, 10.0)
    client.connect()

    sock = socket()

    while True:
        data_packet = client.retrieve_data()
        sock.publish_data(data_packet)

        #Nur für Test der Carla_client_class:
        #Print data
        speed = data_packet["speed"]
        speed_limit = data_packet["speed_limit"]
        throttle = data_packet["throttle"]
        brake = data_packet["brake"]
        message = data_packet["message"]
        collision_event = data_packet["collision_event"]
        rain_intensity = data_packet["rain_intensity"]
        wind_intensity = data_packet["wind_intensity"]
        acceleration = data_packet["acceleration"]

        print(f"S: {speed:6.2f} km/h | T: {throttle:.2f} | B: {brake:.2f} | L: {speed_limit:3f} | M: {message} | C: {collision_event} | R: {rain_intensity} | W: {wind_intensity} | acc: {acceleration}", end='\r')