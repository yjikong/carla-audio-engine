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
            "CARLA_SIM":"",
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
        self.root.geometry("500x500")
        
        self.processes = []
        self._build_ui()

    def load_config(self, defaults):
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    saved_conf = json.load(f)
                # Merge: Use saved values, but keep defaults for missing keys
                for key in defaults:
                    if key not in saved_conf:
                        saved_conf[key] = defaults[key]
                return saved_conf
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

        # Main Container
        main_frm = ttk.Frame(self.root, padding=20)
        main_frm.pack(fill=BOTH, expand=True)

        # Title
        ttk.Label(main_frm, text="SoundCARLA Master Launcher", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Path Rows
        row_idx = 1
        for key, path in self.paths.items():
            # Label for the key
            ttk.Label(main_frm, text=key.replace("_", " "), font=("Arial", 9, "bold")).grid(column=0, row=row_idx, sticky=W, pady=5)
            
            # Shortened path display
            display_text = (path[:30] + '...') if len(path) > 30 else (path if path else "--- NOT SET ---")
            color = "black" if path else "red"
            ttk.Label(main_frm, text=display_text, foreground=color).grid(column=1, row=row_idx, padx=10, sticky=W)
            
            # Browse Button
            ttk.Button(main_frm, text="Browse", width=10, command=lambda k=key: self.browse_file(k)).grid(column=2, row=row_idx, pady=2)
            
            row_idx += 1

        # Separator line
        ttk.Separator(main_frm, orient='horizontal').grid(row=row_idx, column=0, columnspan=3, sticky="ew", pady=20)
        row_idx += 1

        # Control Buttons Frame
        btn_frm = ttk.Frame(main_frm)
        btn_frm.grid(row=row_idx, column=0, columnspan=3)

        # Big Action Buttons
        start_btn = Button(btn_frm, text="▶ START ALL", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), 
                           padx=20, pady=10, command=self.launch_all)
        start_btn.pack(side=LEFT, padx=10)

        stop_btn = Button(btn_frm, text="■ STOP ALL", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), 
                          padx=20, pady=10, command=self.stop_all)
        stop_btn.pack(side=LEFT, padx=10)

        row_idx += 1
        
        # Warning Label placed dynamically below the buttons
        warning_lbl = Label(
            main_frm, 
            text="⚠ After STOP ALL - Close Simulator manually!!!", 
            font=("Arial", 9, "italic bold"),
            fg="#d35400",  # Dark orange for a warning look
            pady=10
        )
        # columnspan=3 centers it across the whole window
        warning_lbl.grid(column=0, row=row_idx, columnspan=3, sticky=S)

    def refresh_ui(self):
        self._build_ui()
    
    def kill_process_on_port(self, port):
            """Finds and kills whatever is sitting on the specified port."""
            try:
                # Wir nutzen errors='ignore', um Encoding-Konflikte (Umlaute) zu vermeiden
                output = subprocess.check_output(
                    f"netstat -ano | findstr :{port}", 
                    shell=True
                ).decode('utf-8', errors='ignore')
                
                for line in output.strip().split('\n'):
                    # Suche nach LISTENING (Englisch) oder ABHÖREN (Deutsch)
                    if "LISTENING" in line or "ABH" in line: # 'ABH' reicht für Abhören
                        pid = line.strip().split()[-1]
                        print(f"Killing zombie process {pid} on port {port}...")
                        os.system(f"taskkill /f /pid {pid}")
                        time.sleep(1)
            except subprocess.CalledProcessError:
                # Port ist frei
                pass

    def launch_all(self):
        self.kill_process_on_port(2000)
       
        if self.paths["CARLA_SIM"]:
            print("Launching CARLA Simulator...")
            carla_folder = os.path.dirname(self.paths["CARLA_SIM"])
            p0 = subprocess.Popen([self.paths["CARLA_SIM"], "-dx11"], cwd=carla_folder)
            self.processes.append(p0)
            
            # --- NEW: Connection Validation Check ---
            print("Verifying CARLA server connectivity...")
            connected = False
            max_retries = 10
            
            # Simple python snippet to test the connection
            check_script = "import carla; carla.Client('localhost', 2000).get_world()"
            
            for i in range(max_retries):
                try:
                    # Run the check using the venv python
                    subprocess.run(
                        [self.paths["VENV_PYTHON"], "-c", check_script],
                        check=True, 
                        capture_output=True,
                        timeout=5
                    )
                    print("CARLA Client successfully connected!")
                    connected = True
                    break
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    print(f"Attempt {i+1}/{max_retries}: Server not ready yet, retrying...")
                    time.sleep(2)

            if not connected:
                print("Error: Could not connect to CARLA server. Aborting launch.")
        else:
            print("Warning: CARLA_SIM path not set. Skipping simulator launch.")

        # 2. Start Manual Control / No Render
        if self.paths["VENV_PYTHON"] and self.paths["MANUAL_CONTROL_SCRIPT"]:
            print("Launching Manual Control...")
            p1 = subprocess.Popen([self.paths["VENV_PYTHON"], self.paths["MANUAL_CONTROL_SCRIPT"]])
            self.processes.append(p1)

        time.sleep(2)

        # 3. Start Carla Client (cmain.py)
        if self.paths["CARLA_CLIENT_VENV"] and self.paths["CARLA_CLIENT_SCRIPT"]:
            print("Launching Carla Client...")
            p2 = subprocess.Popen([self.paths["CARLA_CLIENT_VENV"], self.paths["CARLA_CLIENT_SCRIPT"]])
            self.processes.append(p2)

        time.sleep(2)

        # 4. Start FMOD
        if self.paths["FMOD_VENV"] and self.paths["FMOD_SCRIPT"]:
            print("Launching FMOD Engine...")
            p3 = subprocess.Popen([self.paths["FMOD_VENV"], self.paths["FMOD_SCRIPT"]])
            self.processes.append(p3)

        if self.paths["VENV_PYTHON"] and self.paths["TRAFFIC_SCRIPT"]:
            print("Generating Traffic")
            p4 = subprocess.Popen([self.paths["VENV_PYTHON"], self.paths["TRAFFIC_SCRIPT"]])
            self.processes.append(p4)

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