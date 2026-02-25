from pathlib import Path

FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FILE_DIR.parent
BANKS_DIR = PROJECT_ROOT / "Banks"

MOTOR_BANK_PATH = str((BANKS_DIR / "Motor_Bank").resolve())
ENVIRONMENT_BANK_PATH = str((BANKS_DIR / "Environment_Bank").resolve())