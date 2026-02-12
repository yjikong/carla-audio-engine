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

WARNING_EVENT_PATH = "event:/Warning"
FILE_DIR = Path(__file__).resolve().parent # Was macht das
DEFAULT_BANK_PATH = str((FILE_DIR.parents[3] / 'Banks' / 'Test').resolve()) # Auf drei referenzieren gefährlich -> gebundene Ordnerstruktur

logging.basicConfig(
    filename='loagfile.log',
    filemode='a',
    level=logging.INFO,
    foarmat='%(asctime)s - %(levelname)s - %(message)s'
    )

'''
Idee: Alle Banks in eine Klasse Bank
- Alles was geladen werden muss wird in einer Datei oder so definiert
- Durch diese durch iterieren um alle zu laden 
- Dann vllt static
'''

class EnvironmentBank:
    def __init__(self):
        self.studio_system = None
        self.warning_sound = None
        self._init_studio_system()

    def initaliaze(self):
        self.temp_core_system = pyfmodex.System()
        self.temp_core_system.init()
        self.temp_core_system.release()

        self.studio_system = StudioSystem()
        self.studio_system.initialize(max_channels=512)

    def load(self, bank_path=None):
        if bank_path is None:
            logging.info("Kein Pfad angegeben")
            bank_path = DEFAULT_BANK_PATH
        bank_path = os.path.normpath(bank_path)

        if not os.path.isdir(bank_path):
            logging.error(f"Bank directory not found: {bank_path}")
            raise FileNotFoundError(f"Bank directory not found: {bank_path}")
            # Dann sollten wir doch aus dem Programm raus
        
        # Vllt hier auch ein zentrales dictionary oder enum
        expected_files = [
            "Master.bank",
            "Master.strings.bank",
            "Test.bank",
            "Test.strings.bank"
        ]

        for f in expected_files:
            full = os.path.join(bank_path, f)
            if not os.path.exists(full):
                logging.warning(f"Expected bank file missing: {full}")
                # Sollten wir dann nicht exiten

        # Load Master bank
        self.studio_system.load_bank_file(os.path.join(bank_path, "Master.bank"))
        self.studio_system.load_bank_file(os.path.join(bank_path, "Master.strings.bank"))

        # Try to load specific bank if they exist
        trigger_bank = os.path.join(bank_path, "Trigger_Bank.bank")
        if os.path.exists(trigger_bank):
            self.studio_system.load_bank_file(trigger_bank)
        trigger_strings = os.path.join(bank_path, "Trigger_Bank.strings.bank")
        if os.path.exists(trigger_strings):
            self.studio_system.load_bank_file(trigger_strings)

    def prepare_event(self):
        event_desc = self.studio_system.get_event(WARNING_EVENT_PATH)
        self.warning_sound = event_desc.create_instance()
        return self.warning_sound