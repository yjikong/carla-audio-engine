import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from Code.FMOD.utils import *
from Code.FMOD.Adapters import *
from Code.FMOD.Banks import *
from Code.FMOD.Model.SoundModel import *
from Code.FMOD.Sounds.EVSound import *
from Code.FMOD.Sounds.ReverseBeep import *

import sys

if __name__ == '__main__':
    bus = EventBus()

    env_bank = EnvironmentBank()
    env_bank.start_events()
    env_bank.update_studio_system() 

    trigger_bank = TriggerBank()
    motor_bank = MotorBank()

    ev = EVSoundEngine()

    env_adapter = EnvironmentAdapter(bus, env_bank)
    motor_adapter = EngineAdapter(bus, ev)
    trigger_adapter = TriggerAdapter(bus, trigger_bank)

    model = SoundModel(bus)

    while True:
        model.on_tick()
        trigger_adapter.on_tick()

        time.sleep(0.05)

    
