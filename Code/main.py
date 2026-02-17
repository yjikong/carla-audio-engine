import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from Code.FMOD.utils import *
from Code.FMOD.Adapters import *
from Code.FMOD.Banks import *
from Code.FMOD.Model.SoundModel import *
from Code.FMOD.Sounds.EVSound import *
from Code.FMOD.Sounds.ReverseBeep import *

import keyboard
import sys

if __name__ == '__main__':
    bus = EventBus()

    env_bank = EnvironmentBank()
    env_bank.load()
    env_bank.prepare_event()
    events = env_bank.get_events()
    env_bank.start_events()
    env_bank.update_studio_system()

    trigger_bank = TriggerBank()

    ev = EVSoundEngine()

    env_adapter = EnvironmentAdapter(bus, env_bank, events)
    motor_adapter = MotorAdapter(bus, ev)
    trigger_adapter = TriggerAdapter(bus, trigger_bank, events)

    model = SoundModel(bus)
    model.run()

    
