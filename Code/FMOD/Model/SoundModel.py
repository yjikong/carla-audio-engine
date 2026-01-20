from ..Banks.TriggerBank import * 
from ..Sounds.Reverse_Beep import *
from .Data import *
from ..utils.reverse_update import *
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

        while True:
            Data.decode()
            Data.print_all()
            if (Data.get_speed() > 70) and Trigger == False:
                TriggerBank.warning_sound.start()
                Trigger = True
            if TriggerBank.warning_sound.playback_state == PLAYBACK_STATE.STOPPED:
                Trigger = False

            if reverse_trigger_handler.oneshot_reverse_trigger(Data.get_gear()) or keyboard.is_pressed('r'):
                reverse_beep.play_reverse_beep()

            #   --Platz für Sound Engine Fälle--
            reverse_beep.update()
            TriggerBank.update_studio_system()
            if keyboard.is_pressed('ESC'):
                SoundModel.exit()
                break

    def exit():
        reverse_beep.shutdown()
        TriggerBank.shutdown()