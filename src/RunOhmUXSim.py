"""
SoundCARLA Master Launcher

This module provides a graphical user interface (Tkinter) to control the 
entire SoundCARLA simulation environment. It acts as an orchestrator, 
launching the CARLA simulator, client scripts, the FMOD audio engine, 
and traffic managers within their respective virtual environments.

Key Features:
    * Configuration management via 'sim_config.json'.
    * Dynamic path selection for various Python interpreters (venvs).
    * Automated startup sequence including port cleanup and server health checks.
    * Support for rendering options (e.g., DirectX 11).
"""

import subprocess
import os
import json
import time
import threading
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog

class SimulatorGUI:
    """
    GUI class for managing and launching simulation processes.

    This class encapsulates the entire process management logic for the SoundCARLA 
    environment. It ensures the CARLA server is fully initialized and reachable 
    before triggering dependent clients, such as the FMOD audio engine or 
    manual control scripts.

    Attributes:
        config_path (Path): Path to the JSON configuration file ('sim_config.json').
        paths (dict): Dictionary containing all configured absolute paths to 
            executables and scripts.
        processes (list): List of currently active subprocess.Popen objects for 
            lifecycle management.
        dx11_var (BooleanVar): Tkinter variable tracking the DirectX 11 
            rendering preference. If True, the '-dx11' flag is appended to 
            the CARLA launch command.
    """
    MAX_RETRIES = 10
    def __init__(self):
        """
        Initializes the GUI window, loads saved paths from config, and 
        constructs the interface components.
        """
        base_dir = Path(__file__).resolve().parent
        self.config_path = base_dir / "sim_config.json"
        
        self.paths = self.load_config({
            "CARLA_SIM": "",
            "SIM_VENV_PYTHON": "",
            "CARLA_CLIENT_VENV_PYTHON": "",
            "FMOD_VENV_PYTHON": "",
            "MANUAL_CONTROL_SCRIPT": "",
            "TRAFFIC_SCRIPT": "",
            "CARLA_CLIENT_SCRIPT": "",
            "FMOD_SCRIPT": "",
            "USE_DX11": True
        })

        self.root = Tk()
        self.root.title("SoundCARLA Master Launcher")
        
        # Center window and lock dimensions
        width, height = 550, 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
        
        self.dx11_var = BooleanVar(value=self.paths.get("USE_DX11", True))
        self.processes = []

        # State-based UI initialization: Start with branding
        self._show_branding()

    def _show_branding(self):
        """
        Displays FMOD branding in the primary window buffer.
        """
        self.root.configure(bg='white')
        
        # Path resolution relative to source root
        logo_path = Path(__file__).resolve().parents[1] / "docs" / "source" / "diagrams" / "fmod_logo.png"
        
        try:
            self.splash_img = PhotoImage(file=str(logo_path))
            lbl = Label(self.root, image=self.splash_img, bg='white')
            lbl.pack(expand=True)
        except Exception as e:
            # Fallback for missing assets or unsupported formats
            Label(self.root, text="SOUNDCARLA\nFMOD AUDIO ENGINE",
                  font=("Inter", 16, "bold"), bg='white').pack(expand=True)

        # Trigger transition to functional UI after branding requirements met
        self.root.after(3000, self.show_main_ui)

    def show_main_ui(self, splash_window=None):
        """
        Transitions from Splash to Main UI seamlessly by syncing 
        the geometry and waiting for the main window to be ready.
        """
        # Flush branding widgets from the buffer
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg='#f0f0f0') 
        self._build_ui()
        
        # Ensure transition is seamless by forcing a draw cycle before exposure
        self.root.attributes("-alpha", 0.0)
        self.root.after(10, lambda: self._fade_in(0.0))

    def _fade_in(self, current_alpha):
        """Smoothly transitions alpha from 0 to 1."""
        if current_alpha < 1.0:
            current_alpha += 0.1 
            self.root.attributes("-alpha", current_alpha)
            self.root.after(15, lambda: self._fade_in(current_alpha))
        else:
            self.root.attributes("-alpha", 1.0)
            self.root.attributes("-topmost", False)

    def load_config(self, defaults):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    saved_conf = json.load(f)
                return {**defaults, **saved_conf}
            except Exception as e:
                print(f"Error while loading config: {e}")
                return defaults
        return defaults

    def save_config(self):
        self.paths["USE_DX11"] = self.dx11_var.get()
        with open(self.config_path, "w") as f:
            json.dump(self.paths, f, indent=4)

    def browse_file(self, key):
        filename = filedialog.askopenfilename(title=f"Select {key}")
        if filename:
            self.paths[key] = filename
            self.save_config()
            self.refresh_ui()

    def _build_ui(self):
        main_frm = ttk.Frame(self.root, padding=20)
        main_frm.pack(fill=BOTH, expand=True)

        main_frm.columnconfigure(1, weight=1)

        ttk.Label(main_frm, text="SoundCARLA Master Launcher", 
                  font=("Inter", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        row_idx = 1
        path_items = {k: v for k, v in self.paths.items() if k != "USE_DX11"}
        
        for key, path in path_items.items():
            ttk.Label(main_frm, text=key.replace("_", " "), font=("Inter", 9, "bold")).grid(column=0, row=row_idx, sticky=W, pady=5)
            
            display_text = path if path else "--- NOT SET ---"
            color = "black" if path else "red"
            ttk.Label(main_frm, text=display_text, foreground=color).grid(column=1, row=row_idx, padx=10, sticky=W)
            
            ttk.Button(main_frm, text="Browse", width=10, 
                       command=lambda k=key: self.browse_file(k)).grid(column=2, row=row_idx, pady=2)
            row_idx += 1

        ttk.Separator(main_frm, orient='horizontal').grid(row=row_idx, column=0, columnspan=3, sticky="ew", pady=10)
        row_idx += 1
        
        ttk.Checkbutton(main_frm, text="Use DirectX 11 (-dx11)", 
                        variable=self.dx11_var, command=self.save_config).grid(row=row_idx, column=0, columnspan=3, sticky=W, pady=5)
        row_idx += 1

        ttk.Separator(main_frm, orient='horizontal').grid(row=row_idx, column=0, columnspan=3, sticky="ew", pady=10)
        row_idx += 1

        self.status_var = StringVar(value="Ready")
        ttk.Label(main_frm, textvariable=self.status_var, font=("Inter", 10, "italic"), 
                  foreground="blue").grid(row=row_idx, column=0, columnspan=3, pady=5)
        row_idx += 1

        btn_frm = ttk.Frame(main_frm)
        btn_frm.grid(row=row_idx, column=0, columnspan=3)

        self.start_btn = Button(btn_frm, text="▶ START ALL", bg="#2ecc71", fg="white", font=("Inter", 10, "bold"), 
                                padx=20, pady=10, command=self.launch_all)
        self.start_btn.pack(side=LEFT, padx=10)

        Button(btn_frm, text="■ STOP ALL", bg="#e74c3c", fg="white", font=("Inter", 10, "bold"), 
               padx=20, pady=10, command=self.stop_all).pack(side=LEFT, padx=10)

        row_idx += 1
        Label(main_frm, text="⚠ After STOP ALL - Close Simulator manually!!!", 
              font=("Inter", 9, "italic bold"), fg="#d35400", pady=10).grid(column=0, row=row_idx, columnspan=3, sticky=S)

    def refresh_ui(self):
        # Full UI rebuild to maintain state synchronization
        for widget in self.root.winfo_children():
            widget.destroy()
        self._build_ui()
    
    def kill_process_on_port(self, port=2000):
        """Kills old CARLA servers which might be blocking the port 2000

        Args:
            port (int, optional): Specifies the port CARLA server uses. Defaults to 2000.
        
        Note:
            CARLA uses localhost port 2000 by default. If this is to be modified, all scripts connecting to the
            server must be adjusted.
        """
        try:
            output = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode('utf-8', errors='ignore')
            for line in output.strip().split('\n'):
                if "LISTENING" in line or "ABH" in line:
                    pid = line.strip().split()[-1]
                    os.system(f"taskkill /f /pid {pid}")
                    time.sleep(1)
        except subprocess.CalledProcessError:
            pass

    def launch_all(self):
        self.start_btn.config(state=DISABLED)
        threading.Thread(target=self._run_launch_sequence, daemon=True).start()

    def _run_launch_sequence(self):
        """
        Executes the critical launch sequence in a background thread.
        
        The sequence follows these stages:
            1. Port Cleanup: Terminates any existing processes on port 2000.
            2. Simulator Start: Launches CARLA with the optional -dx11 flag.
            3. Health Check: Polls the CARLA server until a world connection 
               is established.
            4. Orchestration: Sequentially starts Manual Control, the CARLA 
               Client (cmain.py), FMOD Engine, and Traffic Manager.
        """
        self.status_var.set("Cleaning Ports...")
        self.kill_process_on_port(2000)
        
        if self.paths["CARLA_SIM"]:
            self.status_var.set("Starting CARLA Simulator...")
            carla_folder = os.path.dirname(self.paths["CARLA_SIM"])
            cmd = [self.paths["CARLA_SIM"]]
            if self.dx11_var.get():
                cmd.append("-dx11")
                
            self.processes.append(subprocess.Popen(cmd, cwd=carla_folder))
            
            self.status_var.set("Waiting for CARLA Server...")
            connected = False
            check_script = "import carla; client = carla.Client('localhost', 2000); client.set_timeout(5.0); client.get_world()"
            
            for i in range(self.MAX_RETRIES):
                try:
                    subprocess.run([self.paths["SIM_VENV_PYTHON"], "-c", check_script], 
                                   check=True, capture_output=True, timeout=10)
                    connected = True
                    break
                except Exception:
                    self.status_var.set(f"Server-Check {i+1}/{self.MAX_RETRIES}...")
                    time.sleep(10)

            if not connected:
                self.status_var.set("Error: CARLA Timeout!")
                self.start_btn.config(state=NORMAL)
                return

        # Sequential orchestration of downstream clients
        launch_targets = [
            ("Starting Manual Control...", self.paths["SIM_VENV_PYTHON"], self.paths["MANUAL_CONTROL_SCRIPT"], 10),
            ("Starting Carla Client...", self.paths["CARLA_CLIENT_VENV_PYTHON"], self.paths["CARLA_CLIENT_SCRIPT"], 5),
            ("Starting FMOD Engine...", self.paths["FMOD_VENV_PYTHON"], self.paths["FMOD_SCRIPT"], 5),
            ("Generating Traffic...", self.paths["SIM_VENV_PYTHON"], self.paths["TRAFFIC_SCRIPT"], 0)
        ]

        for status, venv, script, delay in launch_targets:
            if venv and script:
                self.status_var.set(status)
                self.processes.append(subprocess.Popen([venv, script]))
                if delay: time.sleep(delay)

        self.status_var.set("All Systems running!")
        self.start_btn.config(state=NORMAL)

    def stop_all(self):
        self.status_var.set("Stopping all processes...")
        for p in self.processes:
            try: p.terminate()
            except: pass
        self.processes = []
        self.status_var.set("Ready")
        self.start_btn.config(state=NORMAL)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = SimulatorGUI()
    gui.run()