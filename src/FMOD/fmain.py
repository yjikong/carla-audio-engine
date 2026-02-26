import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.FMOD.utils import *
from src.FMOD.Adapters import *
from src.FMOD.Banks import *
from src.FMOD.Model.SoundModel import *
from src.FMOD.Sounds.EVSoundEngine import *
from src.FMOD.Sounds.ReverseBeep import *

import sys

if __name__ == '__main__':
    bus = EventBus()

    env_bank = EnvironmentBank()
    trigger_bank = TriggerBank()
    # example_bank = ExampleBank()

    ev = EVSoundEngine()
    rev_beep = ReverseBeep()

    env_adapter = EnvironmentAdapter(bus, env_bank)
    engine_adapter = EngineAdapter(bus, ev)
    trigger_adapter = TriggerAdapter(bus, rev_beep, trigger_bank)

    model = SoundModel(bus)

    while True:
        model.on_tick()
        trigger_adapter.on_tick()

        time.sleep(0.05)

    
