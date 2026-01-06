import carla
import time
import math
from finder import *

class CarlaClient:
    #Die Simulatorwelt muss von anderen Klassen zugänglich sein:
    world = None
    client = None
    vehicle_found = False
    vehicle = None

    def CarlaClient(ip,port,timeout):
        try:
            CarlaClient.client = carla.Client(ip, port)
            CarlaClient.client.set_timeout(timeout)
        except Exception as e:
            print(f"Carla_client.py konnte sich nicht mit Carla Server verbinden.\nSicherstellen, dass Carla Simulator läuft.")

    def connect():
        CarlaClient.world = CarlaClient.client.get_world()

    def retrieve_data():
        if CarlaClient.vehicle_found == False:
            #1. Fahrzeug finden:
            CarlaClient.vehicle = finder.get_vehicle(CarlaClient.world)
            #2. Variable setzen:
            if CarlaClient.vehicle is not None:
                CarlaClient.vehicle_found = True
        #3. Daten auslesen:
        if CarlaClient.vehicle_found == True:

            speed_limit = CarlaClient.vehicle.get_speed_limit()
            v = CarlaClient.vehicle.get_velocity()
            kmh = 3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2)
            control = CarlaClient.vehicle.get_control()

            #4. Daten in JSON Packet umwandeln:
            data_packet = {
                    "speed": round(kmh, 2),
                    "throttle": round(control.throttle, 2),
                    "brake": round(control.brake, 2),
                    "speed_limit": speed_limit,
                    "message": "GREEN",
                }
        else:
            data_packet = {
                "speed": 0.0,
                "throttle": 0.0,
                "brake": 0.0,
                "speed_limit": 0.0,
                "message": "keine Daten verfügbar.",
            }
        return data_packet
        

if __name__ == '__main__':
    #connect and get data
    CarlaClient.CarlaClient('localhost', 2000, 10.0)
    CarlaClient.connect()
    while True:
        data_packet = CarlaClient.retrieve_data()
        
        #Print data
        speed = data_packet["speed"]
        speed_limit = data_packet["speed_limit"]
        throttle = data_packet["throttle"]
        brake = data_packet["brake"]
        message = data_packet["message"]

        print(f"S: {speed:6.2f} km/h | T: {throttle:.2f} | B: {brake:.2f} | L: {speed_limit:3f} | M: {message}", end='\r')
