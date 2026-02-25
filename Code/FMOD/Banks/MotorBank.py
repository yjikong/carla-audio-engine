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


#Declare Events from FMOD Project

#Path for Bank


class MotorBank:
    pass