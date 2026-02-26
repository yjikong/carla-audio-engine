import os
import time
import logging

os.environ["PYFMODEX_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\core\lib\x64\fmod.dll"
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\studio\lib\x64\fmodstudio.dll"

import pyfmodex
from pyfmodex.studio import StudioSystem 
from pyfmodex.studio.enums import PLAYBACK_STATE
from pyfmodex.exceptions import FmodError

from .config import *

class EnvironmentBank:
    DEFAULT_BANK_PATH = ENVIRONMENT_BANK_PATH
    def __init__(self):
        self.studio_system = None
        self.rain_inst = None
        self.wind_inst = None
        self.__init_studio_system()
        self.__init_events()
        self.__start_events()

    def __init_studio_system(self):
        core_system = pyfmodex.System()
        core_system.init()
        core_system.release()
        self.studio_system = StudioSystem()
        self.studio_system.initialize(max_channels=512)

    def __init_events(self, bank_path=DEFAULT_BANK_PATH):
        self._load(bank_path)
        self._prepare_events()

    def _load(self, bank_path=DEFAULT_BANK_PATH):
        if bank_path is None:
            bank_path = self.DEFAULT_BANK_PATH
        bank_path = os.path.normpath(bank_path)
        print(f"[{self.__class__.__name__}] Resolved bank path: {bank_path}")

        if not os.path.isdir(bank_path):
            logging.error(f"Bank directory not found: {bank_path}")
            raise FileNotFoundError(f"Bank directory not found: {bank_path}")
        
        expected_files = [
            "Master.bank",
            "Master.strings.bank",
            "Environment.bank"
        ]

        for f in expected_files:
            full_path = os.path.join(bank_path, f)
            if not os.path.exists(full_path):
                print(f"[{self.__class__.__name__}] Expected bank file missing: {full_path}")
                raise FileNotFoundError(f"Bank directory not found: {bank_path}")
            else:
                self.studio_system.load_bank_file(full_path)

    def _prepare_events(self):
        rain_event_desc = self.studio_system.get_event(RAIN_EVENT_PATH)
        self.rain_inst = rain_event_desc.create_instance()

        wind_event_desc = self.studio_system.get_event(WIND_EVENT_PATH)
        self.wind_inst = wind_event_desc.create_instance()
    
    def __start_events(self):
        self.rain_inst.start()
        self.wind_inst.start()

    def update_studio_system(self):
        self.studio_system.update()

    def get_events(self):
        events = {
            "rain": self.rain_inst,
            "wind": self.wind_inst
        }
        return events
    
    def shutdown(self):
        try:
            print(f'Releasing Studio System')
            self.studio_system.release()
        except AttributeError as e:
            e.add_note(f"Fehlerquelle: Die Instanz existiert nicht mehr")
            print(f"Fehler abgefangen {e}")
        else: 
            print(f"Fahre herunter")