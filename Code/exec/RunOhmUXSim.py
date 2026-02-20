import subprocess
import os
import json
import time
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog

class SimulatorGUI:
    def __init__(self):
        self.config_path = "sim_config.json"
        # Define the roles we need paths for
        self.paths = self.load_config({
            "VENV_PYTHON": "",
            "CARLA_CLIENT_VENV": "",
            "FMOD_VENV": "",
            "MANUAL_CONTROL_SCRIPT": "",
            "TRAFFIC_SCRIPT": "",
            "CARLA_CLIENT_SCRIPT": "",
            "FMOD_SCRIPT": ""
        })

        self.root = Tk()
        self.root.title("SoundCARLA Master Launcher")
        self.root.geometry("600x500")
        
        self.processes = []
        self._build_ui()

    def load_config(self, defaults):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return defaults

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.paths, f, indent=4)

    def browse_file(self, key):
        filename = filedialog.askopenfilename(title=f"Select {key}")
        if filename:
            self.paths[key] = filename
            self.save_config()
            self.refresh_ui()

    def _build_ui(self):
        # Clear existing widgets for refresh
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frm = ttk.Frame(self.root, padding=20)
        main_frm.pack(fill=BOTH, expand=True)

        ttk.Label(main_frm, text="OHM UX Simulator - Script Management", font=("Arial", 12, "bold")).grid(row=0, columnspan=3, pady=10)

        # Create a row for each path
        for i, (key, path) in enumerate(self.paths.items()):
            ttk.Label(main_frm, text=key.replace("_", " ")).grid(column=0, row=i+1, sticky=W, pady=2)
            
            # Show shortened path or "Not Set"
            display_path = (path[:40] + '...') if len(path) > 40 else (path if path else "NOT SET")
            ttk.Label(main_frm, text=display_path, foreground="gray").grid(column=1, row=i+1, padx=10)
            
            ttk.Button(main_frm, text="Browse", command=lambda k=key: self.browse_file(k)).grid(column=2, row=i+1)

        # Launch and Stop Buttons
        btn_frm = ttk.Frame(main_frm, padding=20)
        btn_frm.grid(row=len(self.paths)+1, columnspan=3)

        ttk.Button(btn_frm, text="START ALL", command=self.launch_all).pack(side=LEFT, padx=5)
        ttk.Button(btn_frm, text="STOP ALL", command=self.stop_all).pack(side=LEFT, padx=5)

    def refresh_ui(self):
        self._build_ui()

    def launch_all(self):
        # 1. Start Manual Control / No Render
        print("Launching Manual Control...")
        p1 = subprocess.Popen([self.paths["VENV_PYTHON"], self.paths["MANUAL_CONTROL_SCRIPT"]])
        self.processes.append(p1)

        time.sleep(2)

        # 2. Start Carla Client (cmain.py)
        print("Launching Carla Client...")
        p2 = subprocess.Popen([self.paths["CARLA_CLIENT_VENV"], self.paths["CARLA_CLIENT_SCRIPT"]])
        self.processes.append(p2)

        time.sleep(2)

        # 3. Start FMOD
        print("Launching FMOD Engine...")
        p3 = subprocess.Popen([self.paths["FMOD_VENV"], self.paths["FMOD_SCRIPT"]])
        self.processes.append(p3)

    def stop_all(self):
        for p in self.processes:
            p.terminate()
        self.processes = []
        print("All processes terminated.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = SimulatorGUI()
    gui.run()