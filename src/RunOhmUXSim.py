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

class SplashScreen:
    """
    A borderless, centered top-level window used for FMOD branding.

    This class displays the FMOD logo during the application startup sequence. 
    It is a prerequisite for using the FMOD backend in SoundCARLA. The window 
    remains visible for a fixed duration before automatically destroying itself 
    and triggering the main GUI.

    Attributes:
        parent (Tk): The root window to which this splash screen belongs.
        callback (callable): Function to execute show_main_ui() once 
        the splash duration expires.
        splash (Toplevel): borderless window instance.
        photo (PhotoImage): FMOD logo from the official website.
    """
    def __init__(self, parent, callback):
        """
        Initializes the splash screen, loads the logo, and centers the window.

        Args:
            parent (Tk): The root Tkinter window.
            callback (callable): The method to call after the splash screen finishes.
        """
        self.parent = parent
        self.callback = callback 

        self.splash = Toplevel(parent)
        # We removed overrideredirect(True) to keep the Titlebar consistent
        self.splash.title("SoundCARLA Master Launcher")
        self.splash.attributes("-topmost", True)    
        self.splash.configure(bg='white')

        # Match exact dimensions of the main UI
        width, height = 550, 600
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.splash.geometry(f'{width}x{height}+{x}+{y}')
        self.splash.resizable(False, False)

        # 1. Load the PNG
        logo_path = Path(__file__).resolve().parents[1] / "docs" / "source" / "diagrams" / "fmod_logo.png"
        try:
            self.photo = PhotoImage(file=str(logo_path))
            lbl = Label(self.splash, image=self.photo, bg='white')
            # Pack with expand=True to keep it centered in the 600px height
            lbl.pack(expand=True, fill=BOTH)
        except Exception as e:
            print(f"Logo error: {e}")
            Label(self.splash, text="SOUNDCARLA\nFMOD AUDIO ENGINE",
                  font=("Inter", 16, "bold"), bg='white').pack(expand=True)

        # 2. Prevent user from closing splash prematurely
        self.splash.protocol("WM_DELETE_WINDOW", lambda: None)

        # 3. Timing: 3 seconds branding, then transform
        self.splash.after(3000, self.finish)

    def finish(self):
        """Signals the main UI to take over the existing space."""
        self.callback(self.splash)

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
        self.root.withdraw() # Start hidden
        self.root.title("SoundCARLA Master Launcher")
        self.root.geometry("550x600")
        self.root.resizable(False, False)
        
        self.dx11_var = BooleanVar(value=self.paths.get("USE_DX11", True))
        self.processes = []

        # Start synchronized Splash Screen
        SplashScreen(self.root, self.show_main_ui)

    def show_main_ui(self, splash_window):
        """
        Transitions from Splash to Main UI seamlessly by syncing 
        the geometry before destroying the splash.
        """
        self._build_ui()
        
        # Match coordinates of the splash exactly
        width, height = 550, 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Prepare for fade
        self.root.attributes("-alpha", 0.0)
        self.root.deiconify()
        
        # The key to "no plop": Destroy splash only after deiconify
        splash_window.destroy()
        self._fade_in(0.0)

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
                for key in defaults:
                    if key not in saved_conf:
                        saved_conf[key] = defaults[key]
                return saved_conf
            except Exception as e:
                print(f"Fehler beim Laden der Config: {e}")
                return defaults
        return defaults

    def save_config(self):
        # Update the dict with the current checkbox value before saving
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
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frm = ttk.Frame(self.root, padding=20)
        main_frm.pack(fill=BOTH, expand=True)

        main_frm.columnconfigure(0, weight=0)
        main_frm.columnconfigure(1, weight=1)
        main_frm.columnconfigure(2, weight=0)

        ttk.Label(main_frm, text="SoundCARLA Master Launcher", font=("Inter", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        row_idx = 1
        # Filter out the boolean setting from the path-browsing list
        path_items = {k: v for k, v in self.paths.items() if k != "USE_DX11"}
        
        for key, path in path_items.items():
            ttk.Label(main_frm, text=key.replace("_", " "), font=("Inter", 9, "bold")).grid(column=0, row=row_idx, sticky=W, pady=5)
            
            display_text = path if path else "--- NOT SET ---"
            color = "black" if path else "red"
            ttk.Label(main_frm, text=display_text, foreground=color).grid(column=1, row=row_idx, padx=10, sticky=W)
            
            ttk.Button(main_frm, text="Browse", width=10, command=lambda k=key: self.browse_file(k)).grid(column=2, row=row_idx, pady=2)
            row_idx += 1

        # --- Checkbox Section ---
        ttk.Separator(main_frm, orient='horizontal').grid(row=row_idx, column=0, columnspan=3, sticky="ew", pady=10)
        row_idx += 1
        
        dx_check = ttk.Checkbutton(main_frm, text="Use DirectX 11 (-dx11)", variable=self.dx11_var, command=self.save_config)
        dx_check.grid(row=row_idx, column=0, columnspan=3, sticky=W, pady=5)
        row_idx += 1

        ttk.Separator(main_frm, orient='horizontal').grid(row=row_idx, column=0, columnspan=3, sticky="ew", pady=10)
        row_idx += 1

        self.status_var = StringVar(value="Bereit")
        ttk.Label(main_frm, textvariable=self.status_var, font=("Inter", 10, "italic"), foreground="blue").grid(row=row_idx, column=0, columnspan=3, pady=5)
        row_idx += 1

        btn_frm = ttk.Frame(main_frm)
        btn_frm.grid(row=row_idx, column=0, columnspan=3)

        self.start_btn = Button(btn_frm, text="▶ START ALL", bg="#2ecc71", fg="white", font=("Inter", 10, "bold"), 
                                padx=20, pady=10, command=self.launch_all)
        self.start_btn.pack(side=LEFT, padx=10)

        stop_btn = Button(btn_frm, text="■ STOP ALL", bg="#e74c3c", fg="white", font=("Inter", 10, "bold"), 
                          padx=20, pady=10, command=self.stop_all)
        stop_btn.pack(side=LEFT, padx=10)

        row_idx += 1
        
        warning_lbl = Label(main_frm, text="⚠ After STOP ALL - Close Simulator manually!!!", 
                            font=("Inter", 9, "italic bold"), fg="#d35400", pady=10)
        warning_lbl.grid(column=0, row=row_idx, columnspan=3, sticky=S)

    def refresh_ui(self):
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
        thread = threading.Thread(target=self._run_launch_sequence, daemon=True)
        thread.start()

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
        
        # 1. Start Carla Sim
        if self.paths["CARLA_SIM"]:
            self.status_var.set("Starting CARLA Simulator...")
            carla_folder = os.path.dirname(self.paths["CARLA_SIM"])
            
            # Build arguments list dynamically
            cmd = [self.paths["CARLA_SIM"]]
            if self.dx11_var.get():
                cmd.append("-dx11")
                
            p0 = subprocess.Popen(cmd, cwd=carla_folder)
            self.processes.append(p0)
            
            self.status_var.set("Waiting for CARLA Server...")
            connected = False
            max_retries = 12
            check_script = "import carla; client = carla.Client('localhost', 2000); client.set_timeout(5.0); client.get_world()"
            
            for i in range(max_retries):
                try:
                    subprocess.run([self.paths["SIM_VENV_PYTHON"], "-c", check_script], 
                                   check=True, capture_output=True, timeout=10)
                    connected = True
                    break
                except Exception:
                    self.status_var.set(f"Server-Check {i+1}/{max_retries}...")
                    time.sleep(10)

            if not connected:
                self.status_var.set("Fehler: CARLA Timeout!")
                self.start_btn.config(state=NORMAL)
                return

        # ... (Rest of the manual control, client, and traffic logic remains the same)
        if self.paths["SIM_VENV_PYTHON"] and self.paths["MANUAL_CONTROL_SCRIPT"]:
            self.status_var.set("Starting Manual Control...")
            p1 = subprocess.Popen([self.paths["SIM_VENV_PYTHON"], self.paths["MANUAL_CONTROL_SCRIPT"]])
            self.processes.append(p1)
            time.sleep(10)

        if self.paths["CARLA_CLIENT_VENV_PYTHON"] and self.paths["CARLA_CLIENT_SCRIPT"]:
            self.status_var.set("Starting Carla Client (cmain.py)...")
            p2 = subprocess.Popen([self.paths["CARLA_CLIENT_VENV_PYTHON"], self.paths["CARLA_CLIENT_SCRIPT"]])
            self.processes.append(p2)
            time.sleep(5)

        if self.paths["FMOD_VENV_PYTHON"] and self.paths["FMOD_SCRIPT"]:
            self.status_var.set("Starting FMOD Engine...")
            p3 = subprocess.Popen([self.paths["FMOD_VENV_PYTHON"], self.paths["FMOD_SCRIPT"]])
            self.processes.append(p3)
            time.sleep(5)

        if self.paths["SIM_VENV_PYTHON"] and self.paths["TRAFFIC_SCRIPT"]:
            self.status_var.set("Generating Traffic...")
            p4 = subprocess.Popen([self.paths["SIM_VENV_PYTHON"], self.paths["TRAFFIC_SCRIPT"]])
            self.processes.append(p4)

        self.status_var.set("All Systemes running!")
        self.start_btn.config(state=NORMAL)

    def stop_all(self):
        self.status_var.set("Stopping all processes...")
        for p in self.processes:
            try:
                p.terminate()
            except:
                pass
        self.processes = []
        print("Ready")
        self.status_var.set("Ready")
        self.start_btn.config(state=NORMAL)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = SimulatorGUI()
    gui.run()