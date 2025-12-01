import os

os.environ["PYFMODEX_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\core\lib\x64\fmod.dll"
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\studio\lib\x64\fmodstudio.dll"

import pyfmodex

system = pyfmodex.System()
system.init()
sound = system.create_sound("./Sounds/car-engine-ignition-fail-352768.mp3")
channel = sound.play()

while channel.is_playing:
    pass