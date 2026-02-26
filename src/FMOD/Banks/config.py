from pathlib import Path

FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FILE_DIR.parent
BANKS_DIR = PROJECT_ROOT / "Banks"

TRIGGER_BANK_PATH = str((BANKS_DIR / "Trigger_Bank").resolve())
ENVIRONMENT_BANK_PATH = str((BANKS_DIR / "Environment_Bank").resolve())

# Environment Bank events
RAIN_EVENT_PATH = "event:/Rain"
WIND_EVENT_PATH = "event:/Wind"

# Trigger Bank events
WARNING_EVENT_PATH = "event:/Warning"
CRASH_EVENT_PATH = "event:/Crash"
HONK_EVENT_PATH = "event:/Honk"
HANDBRAKE_EVENT_PATH = "event:/HandBrake"