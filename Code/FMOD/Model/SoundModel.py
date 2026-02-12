import socket
from Code.FMOD.Adapters.MotorAdapter import MotorAdapter
from Code.FMOD.utils import Publisher, Subscriber
from Code.FMOD.utils.DataKey import DataKey
from ..Banks.TriggerBank import * 
from ..Sounds.Reverse_Beep import *
from ..utils.reverse_update import *
import keyboard
import sys
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class SoundModel:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))

        self.data_packet: dict = {}

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
            DataKey.ACCELERATION: self.acceleration_pub,
            DataKey.BRAKE: self.brake_pub,
            DataKey.COLLISION_EVENT: self.collision_pub,
            DataKey.GEAR: self.gear_pub,
            DataKey.MESSAGE: self.message_pub,
            DataKey.RAIN_INTENSITY: self.rain_int_pub,
            DataKey.SPEED: self.speed_pub,
            DataKey.SPEED_LIMIT: self.speed_limit_pub,
            DataKey.THROTTLE: self.throttle_pub,
            DataKey.WIND_INTENSITY: self.wind_int_pub,
        }

    def addSubscriber(self, key: DataKey, sub: Subscriber):
        self.actions[key].subscribe(sub)

    def decode(self):
        data = self.sock.recvfrom(2048)
        # JSON-String to dictionary
        self.data_packet: dict = json.loads(data.decode())
    def get_speed(self):
        return self.data_packet["speed"]
    def get_speed_limit(self):
        return SoundModel.data_packet["speed_limit"]
    def get_gear(self):
        return SoundModel.data_packet["gear"]
    def get_collision_event(self):
        return SoundModel.data_packet["collision_event"]
    def get_rain_intensity(self):
        return SoundModel.data_packet.get("rain_intensity", "No Data")
    def get_wind_intensity(self):
        return SoundModel.data_packet.get("wind_intensity", "No Data") 
    def get_acceleration(self):
        return SoundModel.data_packet.get("acceleration", 0.0)
    def get_throttle(self):
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


    def run(self):      
        while True:
            old_vals:dict = self.data_packet
            SoundModel.decode()
            SoundModel.print_all()

            diff = {k: (k, v) for k, v in self.data_packet.items()
                if old_vals.get(k) != v}

            for key, value in diff.items():
                publisher = self.actions.get(key)
                if publisher:
                    publisher.submit(value)
                else:
                    print("No Publisher exists for this key")

            time.sleep(1)
