import subprocess
import os
from pathlib import Path
import time
import sys

# Pfade definieren Laptop
# CARLA_DIR_LAPTOP = Path(r"C:\Users\jikon\CARLA\WindowsNoEditor")
# PROJEKT_ROOT_LAPTOP = Path(r"C:\Users\jikon\Dokumente\Studium\Semester_6\Projekt\Sound\Code")
# VENV_PYTHON = CARLA_DIR_LAPTOP / ".venv38" / "Scripts" / "python.exe"
# CARLA_CLIENT_VENV = PROJEKT_ROOT_LAPTOP / "Carla" / ".venv38" / "Scripts" / "python.exe"
# FMOD_VENV = PROJEKT_ROOT_LAPTOP / "FMOD" / ".venv" / "Scripts" / "python.exe"
# SCRIPT = CARLA_DIR_LAPTOP / "PythonAPI" / "examples" / "no_rendering_mode.py"
# SCRIPT2 = CARLA_DIR_LAPTOP / "PythonAPI" / "examples" / "generate_traffic.py"
# CARLA_CLIENT_SKRIPT = PROJEKT_ROOT_LAPTOP / "Carla" / "Socket.py"
# FMOD_SKRIPT = PROJEKT_ROOT_LAPTOP / "main.py"

#Pfade definieren PC
CARLA_DIR_PC = Path(r"C:\Users\jikon\CARLA\WindowsNoEditor")
PROJEKT_ROOT_PC = Path(r"C:\Users\jikon\Dokumente\Studium\Semester_6\Projekt\Sound\Code")
VENV_PYTHON = CARLA_DIR_PC / "PythonAPI" / "examples" / ".venv38" / "Scripts" / "python.exe"
CARLA_CLIENT_VENV = PROJEKT_ROOT_PC / "Carla" / ".venv38" / "Scripts" / "python.exe"
FMOD_VENV = PROJEKT_ROOT_PC / "FMOD" / ".venv" / "Scripts" / "python.exe"
#SCRIPT = CARLA_DIR_PC / "PythonAPI" / "examples" / "manual_control.py"
SCRIPT = CARLA_DIR_PC / "PythonAPI" / "examples" / "no_rendering_mode.py"
SCRIPT2 = CARLA_DIR_PC / "PythonAPI" / "examples" / "generate_traffic.py"
CARLA_CLIENT_SKRIPT = PROJEKT_ROOT_PC / "Carla" / "Socket.py"
FMOD_SKRIPT = PROJEKT_ROOT_PC / "main.py"

def wait_for_carla(host="127.0.0.1", port=2000, timeout=60):
    print(f"Pruefe Verbindung zu CARLA auf {host}:{port}...")
    start_time = time.time()
    
    check_command = [
        str(VENV_PYTHON), "-c", 
        f"import carla; client = carla.Client('{host}', {port}); client.set_timeout(10.0); client.get_world()"
    ]

    while time.time() - start_time < timeout:
        result = subprocess.run(check_command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"\nSubprocess Fehler: {result.stderr}")
        if result.returncode == 0:
            print("\n[OK] CARLA Verbindung erfolgreich hergestellt!")
            return True
        
        print(".", end="", flush=True)
        time.sleep(2)
        
    print("\n[FEHLER] Timeout: CARLA konnte nicht erreicht werden.")
    return False

if __name__ == "__main__":
    if wait_for_carla('localhost', 2000, 10):
        env = os.environ.copy()
        
        # 1. Startet No-Rendering Mode im Hintergrund (non-blocking)
        print(f"Starte Hintergrund-Prozess: {SCRIPT.name}")
        process_no_render = subprocess.Popen([str(VENV_PYTHON), str(SCRIPT)], env=env)
        
        # Kurze Pause, damit der No-Rendering Mode den Overhead reduzieren kann
        time.sleep(2)
        
        # 2. Startet Traffic Generator (blockierend oder ebenfalls Hintergrund)
        #print(f"Starte Traffic: {SCRIPT2.name}")
        # Wenn du willst, dass dieses Fenster offen bleibt, nutze run() oder ebenfalls Popen
        #process_traffic = subprocess.Popen([str(VENV_PYTHON), str(SCRIPT2),], env=env)

        time.sleep(2)

        process_carla_client = subprocess.Popen([str(CARLA_CLIENT_VENV), str(CARLA_CLIENT_SKRIPT),], env=env)

        time.sleep(2)

        process_fmod = subprocess.Popen([str(FMOD_VENV), str(FMOD_SKRIPT),], env=env)

        print("\n[INFO] Beide Skripte laufen parallel.")
        print("Druecke Strg+C in CARLA oder beende diesen Prozess, um aufzuhoeren.")
        
        # Haelt das Hauptskript am Leben, solange die Unterprozesse laufen
        try: # Das hier kostet viel performance evtl. Hauptskirpt beenden, nachdem alle Prozesse gestartet wurden
            #process_traffic.wait()
            process_no_render.wait()
            process_carla_client.wait()
            process_fmod.wait()
        except KeyboardInterrupt:
            print("\nBeende Prozesse...")
            process_no_render.terminate()
            #process_traffic.terminate()
            process_fmod.terminate()
            process_carla_client.terminate()

    else:
        print("Skript-Start abgebrochen.")
        sys.exit(1)