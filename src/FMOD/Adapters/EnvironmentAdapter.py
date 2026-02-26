from src.FMOD.Banks import EnvironmentBank
from src.FMOD.utils import DataKey  
from src.FMOD.utils.DataKey import DataKey
from ..utils.EventBus import EventBus
from .RainIntensity import RainIntensity
from .WindIntensity import WindIntensity
from ..utils import RangeLevel

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
        rain_level = RainIntensity.from_value(intensity)
        if rain_level:
            value = rain_level.mapped_value  # 0,1,2,3
        else:
            print(self.__class__.__name__ + ":Invalid intensity value")
            return
        
        self.rain_event.set_parameter_by_name("regenstaerke", value)
        self.bank.update_studio_system() 

    def on_wind(self, intensity: float):    
        value = 0
        wind_level = WindIntensity.from_value(intensity)
        if wind_level:
            value = wind_level.mapped_value  # 0,1,2
        else:
            print(self.__class__.__name__ + ":Invalid intensity value")
            return
        
        self.wind_event.set_parameter_by_name("Windstaerke", value)
        self.bank.update_studio_system()