#set environment
import os
import time
from pathlib import Path
os.environ["PYFMODEX_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\core\lib\x64\fmod.dll"
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\studio\lib\x64\fmodstudio.dll"

import pyfmodex
from pyfmodex.studio import StudioSystem 
from pyfmodex.studio.enums import PLAYBACK_STATE
from pyfmodex.exceptions import FmodError

WARNING_EVNET_PATH = "event:/Warning"

# Resolve a sensible default bank path relative to this file so the code
# works regardless of the current working directory when the script runs.
FILE_DIR = Path(__file__).resolve().parent
# parents[3] should point to the repository root (SoundCARLA) from
# Code/FMOD/Classes/Banks -> .. (Classes) -> .. (FMOD) -> .. (Code) -> .. (SoundCARLA)
DEFAULT_BANK_PATH = str((FILE_DIR.parents[3] / 'Banks' / 'Trigger_Bank').resolve())

class TriggerBank:
    studio_system = None
    warning_sound = None
    def TriggerBank():
        #Initialize
        temp_core_system = pyfmodex.System()
        temp_core_system.init()
        temp_core_system.release() 
        TriggerBank.studio_system = StudioSystem()
        TriggerBank.studio_system.initialize(max_channels=512)
    def load(bank_path=None):
        # Use resolved default if none provided
        if bank_path is None:
            bank_path = DEFAULT_BANK_PATH
        bank_path = os.path.normpath(bank_path)
        print(f"[TriggerBank] Resolved bank path: {bank_path}")

        # Check that directory exists and that expected files are present
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

        # load Banks
        TriggerBank.studio_system.load_bank_file(os.path.join(bank_path, "Master.bank"))
        TriggerBank.studio_system.load_bank_file(os.path.join(bank_path, "Master.strings.bank"))
        # Try to load trigger-specific banks if they exist
        trigger_bank = os.path.join(bank_path, "Trigger_Bank.bank")
        if os.path.exists(trigger_bank):
            TriggerBank.studio_system.load_bank_file(trigger_bank)
        trigger_strings = os.path.join(bank_path, "Trigger_Bank.strings.bank")
        if os.path.exists(trigger_strings):
            TriggerBank.studio_system.load_bank_file(trigger_strings)
    def prepare_event():
        event_desc = TriggerBank.studio_system.get_event(WARNING_EVNET_PATH)
        TriggerBank.warning_sound = event_desc.create_instance()
        return TriggerBank.warning_sound
    def update_studio_system():
        TriggerBank.studio_system.update()
    def set_parameter():
        pass
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
    # Use default resolved bank path (robust to working directory)
    try:
        TriggerBank.load()
        TriggerBank.prepare_event()
        TriggerBank.warning_sound.start()
        TriggerBank.update_studio_system()
        time.sleep(5)
    except FileNotFoundError as e:
        print(f"[TriggerBank] Error: {e}")
    except FmodError as e:
        print(f"[TriggerBank] FMOD error: {e}")

