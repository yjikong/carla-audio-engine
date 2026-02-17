import subprocess
import os
from pathlib import Path
import time

env = os.environ.copy()

CARLA_DIR = Path(r"C:\Users\jikon\CARLA\WindowsNoEditor")
#CARLA_EXE = CARLA_DIR / "CarlaUE4.exe"
CARLA_EXE = CARLA_DIR / "CarlaUE4" / "Binaries" / "Win64" / "CarlaUE4-Win64-Shipping.exe"
SCRIPT = CARLA_DIR / "PythonAPI" / "examples" / "no_rendering_mode.py"
VENV_PYTHON = CARLA_DIR / "PythonAPI" / "examples" /"venv38" / "Scripts" / "python.exe"

print("EXE exists:", CARLA_EXE.exists())

subprocess.Popen(
    [str(CARLA_EXE), "-dx11"],
    cwd=str(CARLA_DIR),
    env=env,
    creationflags=subprocess.CREATE_NEW_CONSOLE
)

time.sleep(60)

subprocess.run([str(VENV_PYTHON), str(SCRIPT)])