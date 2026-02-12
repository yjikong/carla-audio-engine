import socket
from Code.FMOD.Adapters.MotorAdapter import MotorAdapter
from Code.FMOD.utils import Publisher
from ..Banks.TriggerBank import * 
from ..Sounds.Reverse_Beep import *
from .Data import *
from ..utils.reverse_update import *
import keyboard
import sys
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class SoundModel:
    #Datafunktionen
    data_packet = None
    sock = None

    def decode(self):
        data, addr = SoundModel.sock.recvfrom(2048)
        # JSON-String to dictionary
        SoundModel.data_packet:dict = json.loads(data.decode())
        self.client_values:dict = SoundModel.data_packet
    def get_speed():
        speed = SoundModel.data_packet["speed"]
        return speed
    def get_speed_limit():
        speed_limit = SoundModel.data_packet["speed_limit"]
        return speed_limit
    def get_gear():
        return SoundModel.data_packet["gear"]
    def get_collision_event():
        return SoundModel.data_packet["collision_event"]
    def get_rain_intensity():
        return SoundModel.data_packet.get("rain_intensity", "No Data")
    def get_wind_intensity():
        return SoundModel.data_packet.get("wind_intensity", "No Data") 
    def get_acceleration():
        return SoundModel.data_packet.get("acceleration", 0.0)
    def get_throttle():
        return SoundModel.data_packet.get("throttle", 0.0)
    def print_all():
        # .get(key, default_wert) verhindert den KeyError
        speed = SoundModel.data_packet.get("speed", 0.0)
        speed_limit = SoundModel.data_packet.get("speed_limit", 0.0)
        throttle = SoundModel.data_packet.get("throttle", 0.0)
        brake = SoundModel.data_packet.get("brake", 0.0)
        gear = SoundModel.data_packet.get("gear", "N")
        message = SoundModel.data_packet.get("message", "No Data")
        collision_event = SoundModel.data_packet.get("collision_event", False)
        rain_intensity = SoundModel.data_packet.get("rain_intensity", "No Data")
        wind_intensity = SoundModel.data_packet.get("wind_intensity", "No Data")

        print(f"S: {speed:6.2f} km/h | T: {throttle:.2f} | B: {brake:.2f} | L: {speed_limit:3f} | M: {message} | G: {gear} | CE: {collision_event} | R: {rain_intensity} | W: {wind_intensity}", end='\r')


    def __init__(self):
        SoundModel.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SoundModel.sock.bind((UDP_IP, UDP_PORT))

        self.acceleration_pub:Publisher = Publisher()
        self.brake_pub:Publisher = Publisher()
        self.collision_pub:Publisher = Publisher()
        self.gear_pub:Publisher = Publisher()
        self.message_pub:Publisher = Publisher()  
        self.rain_int_pub:Publisher = Publisher()
        self.speed_pub:Publisher = Publisher()
        self.speed_limit_pub:Publisher = Publisher()
        self.throttle_pub:Publisher = Publisher()
        self.wind_int_pub:Publisher = Publisher()

        self.actions = {
            "acceleration": self.acceleration_pub,
            "brake": self.brake_pub,
            "collision_event": self.collision_pub,
            "gear": self.gear_pub,
            "message": self.message_pub,
            "rain_intensity": self.rain_int_pub,
            "speed": self.speed_pub,
            "speed_limit": self.speed_limit_pub,
            "throttle": self.throttle_pub,
            "wind_intensity": self.wind_int_pub
        }

    def run(self):
        
        while True:
            old_vals:dict = self.client_values
            SoundModel.decode()
            SoundModel.print_all()

            diff = {k: v for k, v in self.client_values.items()
                if old_vals.get(k) != v}

            for key, value in diff.items():
                publisher = self.actions.get(key)
                if publisher:
                    publisher.submit(value)
                else:
                    print("No Publisher exists for this key")

            time.sleep(1)

            

    def exit():
        reverse_beep.shutdown()
        TriggerBank.shutdown()