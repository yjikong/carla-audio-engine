from FMOD.utils import *
from FMOD.Adapters import *
from FMOD.Banks import *
from FMOD.Model.SoundModel import *
from FMOD.Sounds.EV_Sound import *
from FMOD.Sounds.Reverse_Beep import *

import keyboard
import sys

if __name__ == '__main__':
    bus = EventBus()

    # Environment Bank Setup
    env_bank = EnvironmentBank()
    env_bank.load()
    env_bank.prepare_event()
    events = env_bank.get_events()
    env_bank.start_events()
    env_bank.update_studio_system()

    #Trigger Bank Setup
    TriggerBank.TriggerBank()
    TriggerBank.load()
    TriggerBank.prepare_events()
    reverse_beep.init()
    reverse_beep.dynamisch_Beep_erstellen()

    ev = EVSoundEngine()

    env_adapter = EnvironmentAdapter(bus, env_bank, events)
    motor_adapter = MotorAdapter(bus, ev)

    model = SoundModel(bus)

    
