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


    #@staticmethod
    def __init__(self):
        SoundModel.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SoundModel.sock.bind((UDP_IP, UDP_PORT))

        reverse_beep.init()
        reverse_beep.dynamisch_Beep_erstellen()

        self.speed_pub = Publisher()
        self.speed_limit_pub = Publisher()
        self.gear_pub = Publisher()
        self.collision_pub = Publisher()
        self.rain_int_pub = Publisher()
        self.wind = Publisher()
        self.acceleration_pub = Publisher()
        self.throttle_pub = Publisher()

    def run(self):
        #prevent constant restart of warning sound:
        Trigger = False
        Trigger2 = False
        

        while True:
            old_vals:dict = self.client_values
            SoundModel.decode()
            SoundModel.print_all()

            common_keys = old_vals.keys() & self.client_values.keys()

            diff = {
                k: (old_vals[k], self.client_values[k])
                for k in common_keys
                if old_vals[k] != self.client_values[k]
            }

            actions = {
                "speed": self.speed_pub,
                "gear": self.gear_pub
            }

            for k in diff.keys():
                actions[k].submit(diff.get(k))
            

    def exit():
        reverse_beep.shutdown()
        TriggerBank.shutdown()