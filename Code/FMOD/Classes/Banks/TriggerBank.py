#set environment
import os
os.environ["PYFMODEX_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\core\lib\x64\fmod.dll"
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\studio\lib\x64\fmodstudio.dll"

import pyfmodex
from pyfmodex.studio import StudioSystem 
from pyfmodex.studio.enums import PLAYBACK_STATE
from pyfmodex.exceptions import FmodError

BANK_PATH = r"..\..\..\..\Banks\Trigger_Bank"
EVENT_PATH = "event:/Warning"

class TriggerBank:
    studio_system = None
    event_inst = None
    def TriggerBank():
        #Initialize
        temp_core_system = pyfmodex.System()
        temp_core_system.init()
        temp_core_system.release() 
        TriggerBank.studio_system = StudioSystem()
        TriggerBank.studio_system.initialize(max_channels=512)
    def load():
        #load Banks
        TriggerBank.studio_system.load_bank_file(os.path.join(BANK_PATH, "Master.bank"))
        TriggerBank.studio_system.load_bank_file(os.path.join(BANK_PATH, "Master.strings.bank"))
        TriggerBank.studio_system.load_bank_file(os.path.join(BANK_PATH, "Trigger_Bank.bank"))
    def prepare_event():
        event_desc = TriggerBank.studio_system.get_event(EVENT_PATH)
        TriggerBank.event_inst = event_desc.create_instance()
        return TriggerBank.event_inst
    def set_parameter():
        pass

if __name__ == '__main__':
