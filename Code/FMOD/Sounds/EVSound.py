import os
import time
import keyboard
import math as m

os.environ["PYFMODEX_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\core\lib\x64\fmod.dll"
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\studio\lib\x64\fmodstudio.dll"

import pyfmodex
from pyfmodex.enums import DSP_TYPE

class EVSoundEngine:
    def __init__(self):
        self.system = pyfmodex.System()
        self.system.init(maxchannels=32)
        
        # Channel Groups
        self.master_group = self.system.create_channel_group("Master")
        self.motor_group = self.system.create_channel_group("Motor")
        self.road_group = self.system.create_channel_group("Road")
        
        # 1. MOTOR (Inverter)
        self.motor_dsp = self.system.create_dsp_by_type(DSP_TYPE.OSCILLATOR) #Grundfrequenz
        self.motor_dsp.set_parameter_int(0, 0) # Sinus
        self.motor_dsp_oberwelle = self.system.create_dsp_by_type(DSP_TYPE.OSCILLATOR)#1. Oberwelle
        self.motor_dsp_oberwelle.set_parameter_int(0,0)
        self.motor_dsp_oberwelle2 = self.system.create_dsp_by_type(DSP_TYPE.OSCILLATOR)#2. Oberwelle
        self.motor_dsp_oberwelle2.set_parameter_int(0,0)
        
        # 2. ROAD BASE (Das rohe Rauschen)
        self.road_base_dsp = self.system.create_dsp_by_type(DSP_TYPE.OSCILLATOR)
        self.road_base_dsp.set_parameter_int(0, 4) # White Noise
        
        # 3. WIND / HISS
        self.hiss_dsp = self.system.create_dsp_by_type(DSP_TYPE.OSCILLATOR)
        self.hiss_dsp.set_parameter_int(0, 4) # White Noise
        
        # FILTER
        # Reifen-Resonanz (Peak/Wummern)
        self.tire_resonance = self.system.create_dsp_by_type(DSP_TYPE.LOWPASS)
        self.tire_resonance.set_parameter_float(0, 200.0) 
        self.tire_resonance.set_parameter_float(1, 4.0)   # Resonance/Q-Faktor
        
        # Schalldämmung (Cabin)
        self.cabin_filter = self.system.create_dsp_by_type(DSP_TYPE.LOWPASS)
        self.cabin_filter.set_parameter_float(0, 1800.0) 

        self.is_running = False

    def start(self):

        # 1. Grundwelle starten
        self.motor_ch = self.system.play_dsp(self.motor_dsp)
        self.motor_ch.channel_group = self.motor_group

        # 1. OBERWELLE in einem eigenen Channel starten
        # Wir weisen sie ebenfalls der motor_group zu
        self.motor_oberwelle_ch = self.system.play_dsp(self.motor_dsp_oberwelle)

        # 2. Oberwelle starten
        self.motor_oberwelle2_ch = self.system.play_dsp(self.motor_dsp_oberwelle2)

        # Hier nutzen wir road_base_dsp für den Reifen-Sound
        self.road_ch = self.system.play_dsp(self.road_base_dsp)
        self.road_ch.channel_group = self.road_group
        
        self.hiss_ch = self.system.play_dsp(self.hiss_dsp)
        self.hiss_ch.channel_group = self.road_group

        # Hierarchien setzen
        self.master_group.add_group(self.motor_group)
        self.master_group.add_group(self.road_group)
        
        # DSP Kette: Road Noise -> Tire Resonance Filter
        self.road_group.add_dsp(0, self.tire_resonance)
        # Alles zusammen -> Cabin Filter
        self.master_group.add_dsp(0, self.cabin_filter)
        
        self.is_running = True

    def update_params(self, speed_kmh, torque, road_roughness=0.01):
        if not self.is_running: return
        
        # MOTOR FREQUENZ
        motor_freq = 200 + (speed_kmh * 3)
        if speed_kmh == 0:
            motor_freq = 0
        self.motor_dsp.set_parameter_float(1, motor_freq)
        self.motor_dsp_oberwelle.set_parameter_float(1, motor_freq + 15)
        self.motor_dsp_oberwelle2.set_parameter_float(1, motor_freq + 60)
        self.motor_ch.volume = abs(torque) * 0.05
        self.motor_oberwelle_ch.volume = abs(torque) * 0.04
        self.motor_oberwelle2_ch.volume = abs(torque) * 0.005

        # ROAD TEXTURE (Reifenrollen)
        # Lautstärke basierend auf Speed & Straßenzustand
        road_vol = min(speed_kmh / 140.0, 0.5) * road_roughness
        self.road_ch.volume = road_vol
        
        # Das Wummern wird bei Speed schneller/heller
        dynamic_road_freq = 120 + (speed_kmh * 1.5)
        self.tire_resonance.set_parameter_float(0, min(dynamic_road_freq, 600))

        # WIND / HISS (Zischen ab 60 km/h)
        hiss_freq = 1000
        self.hiss_dsp.set_parameter_float(1, hiss_freq)
        hiss_vol = max(0, (speed_kmh - 60) / 200.0)
        self.hiss_ch.volume = hiss_vol * 0.2

    def stop(self):
        if self.system:
            self.system.release()

if __name__ == '__main__':
    tesla = EVSoundEngine()
    tesla.start()
    
    speed = 0.0
    torque = 0.0
    last_time = time.time()
    
    print("Tesla Interior Sound Engine (Fixed Hierarchie)")
    print("W/S: Fahren | ESC: Beenden")

    while not keyboard.is_pressed('ESC'):
        dt = time.time() - last_time
        last_time = time.time()
        
        if keyboard.is_pressed('w'): 
            speed = min(speed + 20 * dt, 200)
            torque = 1.0
        elif keyboard.is_pressed('s'): 
            speed = max(speed - 40 * dt, 0)
            torque = -0.8 # Rekuperation
        else:
            speed = max(speed - 5 * dt, 0)
            torque *= 0.1 # Ausrollen
            
        tesla.update_params(speed, torque)
        tesla.system.update()
        
        print(f"\rSpeed: {speed:5.1f} km/h | Motor-Load: {torque:4.1f}", end="")
        time.sleep(0.01)
    
    tesla.stop()