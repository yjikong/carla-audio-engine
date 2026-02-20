from Code.FMOD.Banks import EnvironmentBank
from Code.FMOD.utils import DataKey  
from Code.FMOD.utils.DataKey import DataKey
from ..utils.EventBus import EventBus

import pyfmodex
from pyfmodex.studio import StudioSystem 


class EnvironmentAdapter:
    def __init__(self, event_bus: EventBus, bank: EnvironmentBank):
        self.bank = bank
        events = self.bank.get_events()
        
        self.rain_event = events["rain"]
        self.wind_event = events["wind"]

        event_bus.subscribe(DataKey.RAIN_INTENSITY, self.on_rain)
        event_bus.subscribe(DataKey.WIND_INTENSITY, self.on_wind)

    def on_rain(self, intensity: float):
        value = 0
        if (intensity > 55) and intensity <= 100:
            value = 2
        elif ((intensity > 10) and (intensity <= 55)):
            value = 1
        elif ((intensity <= 10) and (intensity >= 0)):
            value = 0
        else:
            return
        
        self.rain_event.set_parameter_by_name("regenstaerke", value)
        self.bank.update_studio_system()
    
        

    def on_wind(self, intensity: float):    
        value = 0
        if (intensity > 66) and intensity <= 100:
            value = 2
        elif ((intensity > 33) and (intensity <= 66)):
            value = 1
        elif ((intensity <= 33) and (intensity >= 0)):
            value = 0
        else:
            return
        
        self.wind_event.set_parameter_by_name("Windstaerke", value)
        self.bank.update_studio_system()