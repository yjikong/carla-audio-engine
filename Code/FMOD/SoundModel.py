from .Classes.Banks.TriggerBank import * 
from .Data_class import *
import keyboard
import sys

class SoundModel:
    @staticmethod
    def init():
        TriggerBank.TriggerBank()
        TriggerBank.load()
        TriggerBank.prepare_event()
        Data.Data()
    
    def run():
        #prevent constant restart of warning sound:
        Trigger = False

        while True:
            Data.decode()
            Data.print_all()
            if ((Data.get_speed() > 20) or (Data.get_speed() > Data.get_speed_limit())) and Trigger == False:
                TriggerBank.warning_sound.start()
                Trigger = True
            if TriggerBank.warning_sound.playback_state == PLAYBACK_STATE.STOPPED:
                Trigger = False

            #   --Platz für Sound Engine Fälle--

            TriggerBank.update_studio_system()
            if keyboard.is_pressed('q'):
                SoundModel.exit()
                break

    def exit():
        TriggerBank.shutdown()