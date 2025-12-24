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
            CarlaClient.vehicle_found = True
        #3. Daten auslesen:
        v = CarlaClient.vehicle.get_velocity()
        kmh = 3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2)
        control = CarlaClient.vehicle.get_control()

        #4. Daten in JSON Packet umwandeln:
        data_packet = {
                "speed": round(kmh, 2),
                "throttle": round(control.throttle, 2),
                "brake": round(control.brake, 2),
                "timestamp": time.time()
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
        throttle = data_packet["throttle"]
        brake = data_packet["brake"]
        
        print(f"S: {speed:6.2f} km/h | T: {throttle:.2f} | B: {brake:.2f}", end='\r')
