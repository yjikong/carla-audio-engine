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

# Triggerbankpath auflösen
FILE_DIR = Path(__file__).resolve().parent
DEFAULT_BANK_PATH = str((FILE_DIR.parents[3] / 'Banks' / 'Trigger_Bank').resolve())

class TriggerBank:
    studio_system = None
    warning_sound = None
    crash_sound = None
    honk_sound = None
    def TriggerBank():
        # Init
        temp_core_system = pyfmodex.System()
        temp_core_system.init()
        temp_core_system.release() 
        TriggerBank.studio_system = StudioSystem()
        TriggerBank.studio_system.initialize(max_channels=512)
    def load(bank_path=None):
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
        TriggerBank.studio_system.load_bank_file(os.path.join(bank_path, "Master.bank"))
        TriggerBank.studio_system.load_bank_file(os.path.join(bank_path, "Master.strings.bank"))
        trigger_bank = os.path.join(bank_path, "Trigger_Bank.bank")
        if os.path.exists(trigger_bank):
            TriggerBank.studio_system.load_bank_file(trigger_bank)
        trigger_strings = os.path.join(bank_path, "Trigger_Bank.strings.bank")
        if os.path.exists(trigger_strings):
            TriggerBank.studio_system.load_bank_file(trigger_strings)
    def prepare_events():
        temp_warning_event = TriggerBank.studio_system.get_event(WARNING_EVENT_PATH)
        temp_crash_event = TriggerBank.studio_system.get_event(CRASH_EVENT_PATH)
        temp_honk_event = TriggerBank.studio_system.get_event(HONK_EVENT_PATH)
        TriggerBank.warning_sound = temp_warning_event.create_instance()
        TriggerBank.crash_sound = temp_crash_event.create_instance()
        TriggerBank.honk_sound = temp_honk_event.create_instance()
    def update_studio_system():
        TriggerBank.studio_system.update()
    def shutdown():
        try:
            print(f'Releasing Studio System')
            TriggerBank.studio_system.release()
        except AttributeError as e:
            e.add_note(f"Fehlerquelle: Die Instanz existiert nicht mehr")
            print(f"Fehler abgefangen {e}")
        else: 
            print(f"Fahre herunter")


if __name__ == '__main__':
    TriggerBank.TriggerBank()
    try:
        TriggerBank.load()
        TriggerBank.prepare_events()
        TriggerBank.warning_sound.start()
        TriggerBank.update_studio_system()
        time.sleep(5)
    except FileNotFoundError as e:
        print(f"[TriggerBank] Error: {e}")
    except FmodError as e:
        print(f"[TriggerBank] FMOD error: {e}")

