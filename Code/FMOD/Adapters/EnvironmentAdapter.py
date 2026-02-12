from Code.FMOD.Banks import EnvironmentBank
from Code.FMOD.Model.SoundModel import SoundModel
from Code.FMOD.utils import DataKey, Subscriber  
from Code.FMOD.utils.DataKey import DataKey

class EnvironmentAdapter(Subscriber):
    def __init__(self, model: SoundModel, bank: EnvironmentBank):
        self.model = model


    def receive(self, message: tuple):
        print(f"received message: {message}")
        if message:
            pass
        

    def registerSubscriptions(self):
        self.model.addSubscriber(DataKey.RAIN_INTENSITY)
        self.model.addSubscriber(DataKey.WIND_INTENSITY)

    def evaluateWeatherChange():
        change= None
        parameter= 0
        return
    
    def param():
        #precipitation
        #wind_intesity
        pass
        
