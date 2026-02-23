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

HANDBRAKE_EVENT_PATH = "event:/HandBrake"

FILE_DIR = Path(__file__).resolve().parent
DEFAULT_BANK_PATH = str((FILE_DIR.parents[2] / 'Banks' / 'Motor_Bank').resolve())

class MotorBank:
    def __init__(self):
        self.handBrake_sound = None
        self.__init_studio_system()
        self.__init_events()

    def __init_studio_system(self):
        core_system = pyfmodex.System()
        core_system.init()
        core_system.release()
        self.studio_system = StudioSystem()
        self.studio_system.initialize(max_channels=512)

    def __init_events(self, bank_path=None):
        self._load(bank_path)
        self._prepare_events()

    def _load(self, bank_path=None):
        if bank_path is None:
            bank_path = DEFAULT_BANK_PATH
        bank_path = os.path.normpath(bank_path)
        print(f"[TriggerBank] Resolved bank path: {bank_path}")

        if not os.path.isdir(bank_path):
            raise FileNotFoundError(f"Bank directory not found: {bank_path}")

        expected_files = [
            "HandBrake.bank",
            "Maser.bank",
            "Master.strings.bank",
        ]

        self.studio_system.load_bank_file(os.path.join(bank_path, "Master.bank"))
        self.studio_system.load_bank_file(os.path.join(bank_path, "Master.strings.bank"))
        handBrake_bank = os.path.join(bank_path, "HandBrake.bank")
        if os.path.exists(handBrake_bank):
            self.studio_system.load_bank_file(handBrake_bank)

    def _prepare_events(self):
        temp_handBrake_event = self.studio_system.get_event(HANDBRAKE_EVENT_PATH)
        self.handBrake_sound = temp_handBrake_event.create_instance()

    def play_handBrake(self):
        self.handBrake_sound.start()

    def update(self):
        self.studio_system.update()

    def shutdown(self):
        try:
            print(f'Releasing Studio System')
            self.studio_system.release()
        except AttributeError as e:
            e.add_note(f"Fehlerquelle: Die Instanz existiert nicht mehr")
            print(f"Fehler abgefangen {e}")
        else:
            print(f"Fahre herunter")