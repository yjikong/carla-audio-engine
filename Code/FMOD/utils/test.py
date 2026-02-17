import sys
from pathlib import Path

# Füge das Projekt-Root hinzu
PROJECT_ROOT = Path(__file__).resolve().parents[3]  # je nachdem wie tief du bist
sys.path.append(str(PROJECT_ROOT))

from Code.FMOD.Banks import EnvironmentBank
from Code.FMOD.Model.SoundModel import SoundModel
from Code.FMOD.utils.EventBus import EventBus
from Code.FMOD.Adapters.EnvironmentAdapter import *
import pyfmodex



if __name__ == "__main__":
    bus = EventBus()

    env_bank = EnvironmentBank()
    env_bank.load()
    env_bank.prepare_event()
    events = env_bank.get_events()
    env_bank.start_events()
    env_bank.update_studio_system()

    adapter = EnvironmentAdapter(bus, env_bank, events)

    # Model starten
    model = SoundModel(bus)
    model.run()

    
