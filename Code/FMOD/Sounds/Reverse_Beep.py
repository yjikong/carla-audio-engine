import os
os.environ["PYFMODEX_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\core\lib\x64\fmod.dll"
os.environ["PYFMODEX_STUDIO_DLL_PATH"] = r"C:\Program Files (x86)\FMOD SoundSystem\FMOD Studio API Windows\api\studio\lib\x64\fmodstudio.dll"
import pyfmodex
import time
from pyfmodex.enums import DSP_TYPE

class reverse_beep:
    system = None
    grundton = None
    verzerrung = None
    channel = None
    start_time = 0
    is_playing = False
    fader = None

    @staticmethod
    def init():
        if reverse_beep.system is None:
            reverse_beep.system = pyfmodex.System()
            reverse_beep.system.init()
            lautstaerke_regler = reverse_beep.system.master_channel_group
            lautstaerke_regler.volume = 0.05

    @staticmethod
    def dynamisch_Beep_erstellen():
        if reverse_beep.grundton is None:
            # 1. Oszillator erstellen
            reverse_beep.grundton = reverse_beep.system.create_dsp_by_type(DSP_TYPE.OSCILLATOR)
            reverse_beep.grundton.set_parameter_int(0, 0)#Wellenform Sinus (0 bis 3 möglich)
            reverse_beep.grundton.set_parameter_float(1, 1500.0)#Frequenz

            # 2. Verzerrung erstellen
            reverse_beep.verzerrung = reverse_beep.system.create_dsp_by_type(DSP_TYPE.DISTORTION)
            reverse_beep.verzerrung.set_parameter_float(0, 1)#Verzerrungsfaktor

            # 3. Fader erstellen
            reverse_beep.fader = reverse_beep.system.create_dsp_by_type(DSP_TYPE.FADER)
            reverse_beep.fader.set_parameter_float(0, 1)

            # 4. Kette erstellen
            reverse_beep.verzerrung.add_input(reverse_beep.grundton)
            # Verzerrung -> Fader
            reverse_beep.fader.add_input(reverse_beep.verzerrung)

            # Alle aktivieren
            reverse_beep.grundton.active = True
            reverse_beep.verzerrung.active = True
            reverse_beep.fader.active = True

    @staticmethod
    def play_reverse_beep():
        reverse_beep.init()
        reverse_beep.dynamisch_Beep_erstellen()
        
        if not reverse_beep.is_playing:
            # Wir starten jetzt ganz normal
            reverse_beep.channel = reverse_beep.system.play_dsp(reverse_beep.grundton)
            reverse_beep.channel.add_dsp(0, reverse_beep.verzerrung)
            reverse_beep.channel.add_dsp(0, reverse_beep.fader) # hört sich eventuell ohne fader besser an
            
            reverse_beep.start_time = time.time()
            reverse_beep.is_playing = True

    @staticmethod
    def update():
        if reverse_beep.is_playing and reverse_beep.channel:
            if time.time() - reverse_beep.start_time >= 0.4:
                reverse_beep.channel.stop()
                reverse_beep.is_playing = False
        
        if reverse_beep.system:
            reverse_beep.system.update()

    @staticmethod
    def shutdown():
        if reverse_beep.system:
            print(f'Räume den Reverse Beep auf')
            reverse_beep.system.release()
            reverse_beep.system = None

import keyboard

if __name__ == '__main__':
    while True:
        reverse_beep.play_reverse_beep()
            