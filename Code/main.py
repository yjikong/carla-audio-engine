from FMOD.Classes.Banks.TriggerBank import * 
from FMOD.Data_class import *

if __name__ == '__main__':
    #Init
    TriggerBank.TriggerBank()
    TriggerBank.load()
    TriggerBank.prepare_event()
    Data.Data()

    #prevent constant restart of warning sound:
    Trigger = False

    while True:
        if Data.get_speed() > Data.get_speed_limit & Trigger == False:
            TriggerBank.event_inst.start()
            Trigger = True
        if TriggerBank.event_inst.playback_state == PLAYBACK_STATE.STOPPED:
            Trigger = False
