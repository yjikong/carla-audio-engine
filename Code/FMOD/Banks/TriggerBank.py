import os
import time
from pathlib import Path


os.environ["PYFMODEX_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\core\lib\x64\fmod.dll"
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\studio\lib\x64\fmodstudio.dll"

import pyfmodex
from pyfmodex.studio import StudioSystem 
from pyfmodex.studio.enums import PLAYBACK_STATE
from pyfmodex.exceptions import FmodError

# Events aus FMOD Projekt deklarieren
WARNING_EVENT_PATH = "event:/Warning"
CRASH_EVENT_PATH = "event:/Crash"
HONK_EVENT_PATH = "event:/Honk"
HANDBRAKE_EVENT_PATH = "event:/HandBrake"

# Triggerbankpath auflösen
FILE_DIR = Path(__file__).resolve().parent
DEFAULT_BANK_PATH = str((FILE_DIR.parents[2] / 'Banks' / 'Trigger_Bank').resolve())

class TriggerBank:
    def __init__(self):
        self.warning_sound = None
        self.crash_sound = None
        self.honk_sound = None
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
            "Master.bank",
            "Master.strings.bank",
            "Trigger_Bank.bank",
            "Trigger_Bank.strings.bank",
        ]

        for f in expected_files:
            full = os.path.join(bank_path, f)
            if not os.path.exists(full):
                print(f"[TriggerBank] Warning: expected bank file missing: {full}")

        # Banks laden
        self.studio_system.load_bank_file(os.path.join(bank_path, "Master.bank"))
        self.studio_system.load_bank_file(os.path.join(bank_path, "Master.strings.bank"))
        trigger_bank = os.path.join(bank_path, "Trigger_Bank.bank")
        if os.path.exists(trigger_bank):
            self.studio_system.load_bank_file(trigger_bank)
        trigger_strings = os.path.join(bank_path, "Trigger_Bank.strings.bank")
        if os.path.exists(trigger_strings):
            self.studio_system.load_bank_file(trigger_strings)

    def _prepare_events(self):
        temp_warning_event = self.studio_system.get_event(WARNING_EVENT_PATH)
        temp_crash_event = self.studio_system.get_event(CRASH_EVENT_PATH)
        temp_honk_event = self.studio_system.get_event(HONK_EVENT_PATH)
        temp_handBranke_event = self.studio_system.get_event(HANDBRAKE_EVENT_PATH)
        self.warning_sound = temp_warning_event.create_instance()
        self.crash_sound = temp_crash_event.create_instance()
        self.honk_sound = temp_honk_event.create_instance()
        self.handBrake_sound = temp_handBranke_event.create_instance()
    
    def play_honk(self):
        self.honk_sound.start()
    
    def play_crash(self):
        self.crash_sound.start()
    
    def play_warning(self):
        self.warning_sound.start()

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

