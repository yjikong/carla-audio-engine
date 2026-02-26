import os
import time
import logging

from pathlib import Path
os.environ["PYFMODEX_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\core\lib\x64\fmod.dll"
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\studio\lib\x64\fmodstudio.dll"

import pyfmodex
from pyfmodex.studio import StudioSystem
from pyfmodex.studio.enums import PLAYBACK_STATE
from pyfmodex.exceptions import FmodError

from config import *

class ExampleBank:
    EXAMPLE_EVENT_PATH = "event:/Example"
    
    def __init__(self):
        self.__init_studio_system()
        self.__init_events()

    def __init_studio_system(self):
        core_system = pyfmodex.System()
        core_system.init()
        core_system.release()
        self.studio_system = StudioSystem()
        self.studio_system.initialize(max_channels=512)

    def __init_events(self, bank_path=EXAMPLE_EVENT_PATH):
        self._load(bank_path)
        self._prepare_events()

    def _load(self, bank_path=EXAMPLE_EVENT_PATH):
        # if bank_path is None:
        #     bank_path = DEFAULT_BANK_PATH
        # bank_path = os.path.normpath(bank_path)
        # print(f"[{self.__class__.__name__}] Resolved bank path: {bank_path}")

        # if not os.path.isdir(bank_path):
        #     raise FileNotFoundError(f"Bank directory not found: {bank_path}")

        # expected_files = [
        #     "Master.bank",
        #     "Master.strings.bank",
        #     "Example.bank"
        # ]

        # for f in expected_files:
        #     full_path = os.path.join(bank_path, f)
        #     if not os.path.exists(full_path):
        #         print(f"[{self.__class__.__name__}] Expected bank file missing: {full_path}")
        #     else:
        #         self.studio_system.load_bank_file(full_path)
        pass

    def _prepare_events(self):
        # example_event = self.studio_system.get_event(EXAMPLE_EVENT_PATH)
        # self.example_sound = example_event.create_instance()
        pass

    def update_studio_system(self):
        self.studio_system.update()

    def get_events():
        events = {
            # See EnvironmentBank for example
        }
        return events

    def shutdown(self):
        try:
            print(f'Releasing Studio System')
            self.studio_system.release()
        except AttributeError as e:
            e.add_note(f"Source of error: Instance does not exist anymore")
            print(f"Error: {e}")
        else:
            print(f"Shutdown")