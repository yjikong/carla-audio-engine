import os
import time

os.environ["PYFMODEX_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\core\lib\x64\fmod.dll"
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\studio\lib\x64\fmodstudio.dll"

import pyfmodex

from pyfmodex.studio import StudioSystem 

# ... (DLL path setup) ...

# -------------------------------
# 2. Initialize FMOD Studio System
# -------------------------------
# Replace the old initialization:
# system = pyfmodex.System() 
# system.init()

# With the correct Studio System initialization:
studio_system = StudioSystem()
studio_system.initialize()

# Use the new variable name for subsequent calls
# -------------------------------
# 3. Load soundbanks
# -------------------------------
BANK_PATH = r"C:\Users\ozanm\1_Code\Projekt_Carla_Sound_Semester_6\FMOD\CARLA_Sound\Build\Desktop"

# Use 'studio_system' instead of 'system'
print("Loading Sound bank")
studio_system.load_bank_file(os.path.join(BANK_PATH, "Master.bank"))
studio_system.load_bank_file(os.path.join(BANK_PATH, "Master.strings.bank"))
studio_system.load_bank_file(os.path.join(BANK_PATH, "Test.bank"))

# -------------------------------
# 4. Get event and create instance
# -------------------------------
print("Also hier sollten jetzt die Events kommen")
EVENT_PATH = "event:/Ignition"
# Use 'studio_system' here too
event_desc = studio_system.get_event(EVENT_PATH)
event_inst = event_desc.create_instance()

# -------------------------------
# 5. Play event and Update loop
# -------------------------------
event_inst.start()

# Update loop (~4 seconds)
for _ in range(200):
    # Use 'studio_system' update
    studio_system.update()
    time.sleep(0.02)

# -------------------------------
# 6. Cleanup
# -------------------------------
event_inst.release()
studio_system.release() # Release the studio system