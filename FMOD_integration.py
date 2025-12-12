import os
import time
import keyboard

os.environ["PYFMODEX_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\core\lib\x64\fmod.dll"
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\studio\lib\x64\fmodstudio.dll"

import pyfmodex

from pyfmodex.studio import StudioSystem 
from pyfmodex.studio.enums import PLAYBACK_STATE
from pyfmodex.exceptions import FmodError

# FMOD Soundbank Path (Location of your built banks)
BANK_PATH = r"C:\Users\ozanm\1_Code\Projekt_Carla_Sound_Semester_6\FMOD\CARLA_Sound\Build\Desktop"
EVENT_PATH = "event:/Ignition" # The event to control
Background_music_Event_path = "event:/Background"
Honk_path = "event:/Honk"

# --- FMOD Initialization ---
studio_system = None
event_inst = None
is_running = True

try:
    # 1. Initialize Systems
    temp_core_system = pyfmodex.System()
    temp_core_system.init()
    temp_core_system.release() 
    
    studio_system = StudioSystem()
    studio_system.initialize(max_channels=512)
    print("FMOD Studio System initialized successfully.")
    
    # 2. Load Banks (Master.strings.bank is key for name lookup!)
    print("Loading soundbanks...")
    studio_system.load_bank_file(os.path.join(BANK_PATH, "Master.bank"))
    studio_system.load_bank_file(os.path.join(BANK_PATH, "Master.strings.bank"))
    studio_system.load_bank_file(os.path.join(BANK_PATH, "Test.bank"))
    print("All necessary soundbanks loaded.")
    
    # 3. Prepare the Event
    print(f"Retrieving event: {EVENT_PATH}")
    event_desc = studio_system.get_event(EVENT_PATH)
    event_inst = event_desc.create_instance()

    #Background event
    background_music = studio_system.get_event(Background_music_Event_path)
    background_music_inst = background_music.create_instance()

    honk = studio_system.get_event(Honk_path)
    honk_inst = honk.create_instance()
    
    print("\n--- CONTROL READY ---")
    print(f"Press [SPACE] to PLAY '{EVENT_PATH}'")
    print("Press [X] to STOP the event.")
    print("Press [Q] to QUIT the program.")
    
    # 4. Main Update Loop (The heartbeat of FMOD)
    while is_running:

        if keyboard.is_pressed('h'):
            honk_inst.start()
            time.sleep(0.2)

        if keyboard.is_pressed('b'):
            background_music_inst.start()
            time.sleep(0.2)

        # --- Check for Play Command ---
        if keyboard.is_pressed('space'):
            # Check if the event is stopped before starting it
            
            event_inst.start()
            print(f"[PLAY] Event started.")
            # Debounce: wait a moment so it doesn't try to restart immediately
            time.sleep(0.2) 

        # --- Check for Stop Command ---
        if keyboard.is_pressed('x'):
            # Check if the event is playing before stopping it
            # Use FMOD_STUDIO_STOP_IMMEDIATE for instant cut-off
            background_music_inst.stop()
            print(f"[STOP] Event stopped.")
            # Debounce
            time.sleep(0.2) 
            
        # --- Check for Quit Command ---
        if keyboard.is_pressed('q'):
            print("\n[QUIT] Exiting program...")
            is_running = False
            
        # --- FMOD Update ---
        studio_system.update()
        
        # Control loop speed (20 milliseconds sleep)
        time.sleep(0.02) 

    
# --- Cleanup ---
finally:
    print("Starting cleanup...")
    try:
        if event_inst:
            event_inst.release()
        if studio_system:
            studio_system.release()
    except Exception as e:
        print(f"Cleanup error (FMOD may already be released): {e}")
    
    print("FMOD system released. Script finished.")