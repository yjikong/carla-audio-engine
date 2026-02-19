import carla
import time
import math
import keyboard
#funktioniert nur wenn Socket.py ausgeführt wird!!!
from Classes.CollisionSensor import *

class CarlaClient:
    def __init__(self, ip,port,timeout):
        try:
            self.client = carla.Client(ip, port)
            self.client.set_timeout(timeout)
        except Exception as e:
            print(f"Carla_client.py konnte sich nicht mit Carla Server verbinden.\nSicherstellen, dass Carla Simulator läuft.")
        self.world = None
        self.vehicle_found = False
        self.vehicle = None
        self.collision_sensor = None
        self.crash_counter = 0
        self.crash_impulse = False
        self.honk_trigger = False
        
        self.connect()
        

    def connect(self):
        self.world = self.client.get_world()
    
    def get_vehicle(self):
        vehicles = self.world.get_actors().filter('vehicle.*')

        if vehicles:
            for vehicle in vehicles:
                if vehicle.attributes.get('role_name') == "hero":
                    print(f"Verbunden mit vorhandenem Fahrzeug: {vehicle.type_id}")
                    return vehicle
        else:
            print("Es wurden keine Autos gefunden!")
            return None

    def retrieve_data(self):
        #Wetterdaten
        weather = self.world.get_weather()
        rain_intensity = weather.precipitation
        wind_intensity = weather.wind_intensity
        #Hupen
        honk = False
        if keyboard.is_pressed('h') and self.honk_trigger is True:
            honk = False
        elif keyboard.is_pressed('h') and self.honk_trigger is False:
            honk = True
            self.honk_trigger = True
        elif not keyboard.is_pressed('h'):
            self.honk_trigger = False
        #Fahrzeugdaten
        if self.vehicle_found == False:
            #1. Fahrzeug finden:
            self.vehicle = self.get_vehicle()
            #2. Variable setzen:
            if self.vehicle is not None:
                self.vehicle_found = True
                #Attach Collision Sensor to vehicle
                self.collision_sensor = CollisionSensor(self.vehicle)
        #3. Daten auslesen:
        if self.vehicle_found == True:

            acceleration = self.vehicle.get_acceleration()
            speed_limit = self.vehicle.get_speed_limit()
            v = self.vehicle.get_velocity()
            kmh = 3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2)
            control = self.vehicle.get_control()
            gear = control.gear
            handbrake = control.hand_brake()
            steer = control.steer

            if self.collision_sensor.collision_counter > self.crash_counter and self.collision_sensor.intensity > 100:
                self.crash_impulse = True
                self.crash_counter = self.collision_sensor.collision_counter

            #4. Daten in JSON Packet umwandeln:
            data_packet = {
                    "speed": round(kmh, 2),
                    "throttle": round(control.throttle, 2),
                    "brake": round(control.brake, 2),
                    "speed_limit": speed_limit,
                    "message": "GREEN",
                    "gear" : gear,
                    "collision_event" : self.crash_impulse,
                    "rain_intensity" : rain_intensity,
                    "wind_intensity" : wind_intensity,
                    "acceleration" : acceleration.y,
                    "honk" : honk,
                    "handbrake" : handbrake
                }
        self.crash_impulse = False
        return data_packet
    
    def set_rain(self, in_rain_intensity):
        weather = self.world.get_weather()
        weather.precipitation = float(in_rain_intensity)
        weather.wetness = float(in_rain_intensity)
        self.world.set_weather(weather)
    
    def set_wind(self, in_wind_intensity=0):
        weather = self.world.get_weather()
        weather.wind_intensity = float(in_wind_intensity)
        self.world.set_weather(weather)
