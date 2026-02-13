from Code.FMOD.Banks import EnvironmentBank
from Code.FMOD.utils import DataKey  
from Code.FMOD.utils.DataKey import DataKey
from ..utils.EventBus import EventBus

import pyfmodex
from pyfmodex.studio import StudioSystem 


class EnvironmentAdapter:
    def __init__(self, event_bus: EventBus, event):
        self.event = event

        event_bus.subscribe(DataKey.RAIN_INTENSITY, self.on_rain)
        event_bus.subscribe(DataKey.WIND_INTENSITY, self.on_wind)

    def on_rain(self, intensity: float):
        value = 0
        if (intensity > 50) and intensity <= 100:
            value = 1
        elif ((intensity <= 50) and (intensity >= 0)):
            value = 0
        else:
            return
        self.event.set_parameter_by_name(DataKey.RAIN_INTENSITY, value)

    def on_wind(self, intensity: float):    
        value = 0
        if (intensity > 50) and intensity <= 100:
            value = 1
        elif ((intensity <= 50) and (intensity >= 0)):
            value = 0
        else:
            return
        self.event.set_parameter_by_name(DataKey.WIND_INTENSITY, value)

        
