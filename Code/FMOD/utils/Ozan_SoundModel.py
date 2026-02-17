from .Classes.Banks.TriggerBank import * 
from .Classes.Sounds.Reverse_Beep import *
from .Classes.Sounds.EV_Sound import *
from .Classes.Adapters.MotorAdapter import *
from .utils.reverse_update import *
import keyboard
import sys
import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class SoundModel:
    #Datafunktionen
    data_packet = None
    sock = None
    def decode():
        data, addr = SoundModel.sock.recvfrom(2048)
        # JSON-String to dictionary
        SoundModel.data_packet = json.loads(data.decode())
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


    @staticmethod
    def __init__():
        SoundModel.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SoundModel.sock.bind((UDP_IP, UDP_PORT))
        TriggerBank.TriggerBank()
        TriggerBank.load()
        TriggerBank.prepare_events()
        reverse_beep.init()
        reverse_beep.dynamisch_Beep_erstellen()
    
    def run():
        #prevent constant restart of warning sound:
        Trigger = False
        Trigger2 = False
        ev = EVSoundEngine()

        while True:
            SoundModel.decode()
            SoundModel.print_all()

            #Geschwindigkeitswarner
            if (SoundModel.get_speed() > 100) and Trigger == False:
                TriggerBank.warning_sound.start()
                Trigger = True
            if TriggerBank.warning_sound.playback_state == PLAYBACK_STATE.STOPPED:
                Trigger = False
            
            #Crash
            if ((SoundModel.get_collision_event()) and Trigger2 == False) or keyboard.is_pressed('c'):
                TriggerBank.crash_sound.start()
                Trigger2 = True
            if TriggerBank.crash_sound.playback_state == PLAYBACK_STATE.STOPPED:
                Trigger2 = False

            #Honk
            if keyboard.is_pressed('h'):
                TriggerBank.honk_sound.start()

            #Reverse
            if reverse_trigger_handler.oneshot_reverse_trigger(SoundModel.get_gear()) or keyboard.is_pressed('r'):
                reverse_beep.play_reverse_beep()
            
            #EV_Sound
            if ev.is_running is False:
                ev.start()
            ev.update_params(SoundModel.get_speed(), MotorAdapter.calculate_torque(SoundModel.get_speed(), SoundModel.get_throttle()))
            ev.system.update()


            #   --Platz für Sound Engine Fälle--
            
            reverse_beep.update()
            TriggerBank.update_studio_system()
            if keyboard.is_pressed('ESC'):
                SoundModel.exit()
                break

    def exit():
        reverse_beep.shutdown()
        TriggerBank.shutdown()