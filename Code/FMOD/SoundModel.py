from .Classes.Banks.TriggerBank import * 
from .Classes.Sounds.Reverse_Beep import *
from .Data_class import *
import keyboard
import sys

class SoundModel:
    @staticmethod
    def init():
        TriggerBank.TriggerBank()
        TriggerBank.load()
        TriggerBank.prepare_event()
        reverse_beep.init()
        reverse_beep.dynamisch_Beep_erstellen()
        Data.Data()
    
    def run():
        #prevent constant restart of warning sound:
        Trigger = False
        reversetrigger = False

        while True:
            Data.decode()
            Data.print_all()
            if ((Data.get_speed() > 20) or (Data.get_speed() > Data.get_speed_limit())) and Trigger == False:
                TriggerBank.warning_sound.start()
                Trigger = True
            if TriggerBank.warning_sound.playback_state == PLAYBACK_STATE.STOPPED:
                Trigger = False

            if (Data.get_gear() == -1 and reversetrigger == False) or keyboard.is_pressed('r'):
                reverse_beep.play_reverse_beep()
                reversetrigger = True

            #   --Platz für Sound Engine Fälle--
            reverse_beep.update()
            TriggerBank.update_studio_system()
            if keyboard.is_pressed('ESC'):
                SoundModel.exit()
                break

    def exit():
        reverse_beep.shutdown()
        TriggerBank.shutdown()