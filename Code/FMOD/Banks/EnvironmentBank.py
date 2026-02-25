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

REGEN_EVENT_PATH = "event:/Rain"
WIND_EVENT_PATH = "event:/Wind"
FILE_DIR = Path(__file__).resolve().parent
DEFAULT_BANK_PATH = str((FILE_DIR.parents[2] / 'Banks' / 'Environment_Bank').resolve()) # Auf drei referenzieren gefährlich -> gebundene Ordnerstruktur

'''
Idee: Alle Banks in eine Klasse Bank
- Alles was geladen werden muss wird in einer Datei oder so definiert
- Durch diese durch iterieren um alle zu laden 
- Dann vllt static

Bei dieser Idee müsste man also globale Parameter und instanzparam beachten
ich bräuchte damit eine Liste der zuordnung welcher Parameter zu welcher Instanz
gehört bzw. ob er global ist.
Wenn die funktion set param(name, value) aufgerufen wird, muss erstens sicher sein,
dass es keine zwei parameter mit dem gleichen namen gibt, das wäre SEHR problematisch
der name müsste dann mit der liste abgeglichen werden und je nach parametername würde dann
entweder studio_system.set_parameter_by_name oder event_instance.set...

Aus den Bank dateien könnten die entsprechenden Parameter rausgelesen werden und überprüft
werden ob sie global oder zum event gehören.

Diese Idee würde den Vorteil bringen, dass die Bank Klasse praktisch nicht mehr
"gepflegt" werden müsste, sondern alles automatisiert abläuft, durch skripte, die man bspw.
in der main aufgerufen werden.
Die Bank klasse könnte eine Methode haben wie "set_banks" und "receive_param" um alles nötige
zu erhalten.

Erstmal mit verschiedenen Bank klassen probieren und dann mal refactorn und schauen
'''

'''
Es könnte interessant sein, folgende Werte zu publishen
| Event                     | Wert                 | Beschreibung                                                             |
| ------------------------- | -------------------- | ------------------------------------------------------------------------ |
| `event_started`           | Event-Name oder ID   | Signalisiert, dass ein Sound-Event gestartet wurde                       |
| `event_stopped`           | Event-Name oder ID   | Signalisiert, dass ein Event gestoppt wurde                              |
| `event_error`             | Fehlermeldung        | Wenn FMOD einen Fehler wirft                                             |
| `event_parameter_changed` | Parametername + Wert | Falls du dynamische Parameter im Event setzt                             |
| `bank_loaded`             | Bankname             | Optional, falls Monitoring benötigt                                      |
| `studio_updated`          | Timestamp / Counter  | Optional, falls Subscriber wissen wollen, dass Studio aktualisiert wurde |
'''
class EnvironmentBank:
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
            bank_path = DEFAULT_BANK_PATH
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
                print(f"Expected bank file missing: {full_path}")
                raise FileNotFoundError(f"Bank directory not found: {bank_path}")
            else:
                self.studio_system.load_bank_file(full_path)

    def _prepare_events(self):
        rain_event_desc = self.studio_system.get_event(REGEN_EVENT_PATH)
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

if __name__ == "__main__":
    tb = EnvironmentBank()
    try:
        tb._load()
        tb._prepare_events()
        tb.warning_sound.start()
        tb.update_studio_system()
        time.sleep(5)
    except FileNotFoundError as e:
        print(f"[TriggerBank] Error: {e}")
    except FmodError as e:
        print(f"[TriggerBank] FMOD error: {e}")
    finally:
        tb.shutdown()
