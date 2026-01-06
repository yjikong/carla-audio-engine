from FMOD.Classes.Banks.TriggerBank import * 
from FMOD.Data_class import *

BANK_PATH = r".\Banks\Trigger_Bank"

if __name__ == '__main__':
    #Init
    TriggerBank.TriggerBank()
    TriggerBank.load()
    TriggerBank.prepare_event()
    Data.Data()

    #prevent constant restart of warning sound:
    Trigger = False

    while True:
        Data.decode()
        Data.print_all()
        # if Data.get_speed() > Data.get_speed_limit() and Trigger == False:
        #     TriggerBank.event_inst.start()
        #     Trigger = True
        #Zum Test Speedlimit runter gesetzt:
        if Data.get_speed() > 15 and Trigger == False:
            TriggerBank.event_inst.start()
            Trigger = True
        if TriggerBank.event_inst.playback_state == PLAYBACK_STATE.STOPPED:
            Trigger = False
        TriggerBank.update_studio_system()
