from ..Sounds.EV_Sound import *

class MotorAdapter:
    def speed_to_freq(current_velocity):
        pass

    def set_EV_sound_freq(current_velocity):
        pass

    def calculate_torque(speed, throttle):
        #Wenn Throttle 0 -> Torque 0
        if throttle == 0:
            return 0
        elif throttle > 0 and speed > 0:
            return 1
        elif throttle > 0 and speed < 0:
            return -0.8
        else:
            return 0
        
