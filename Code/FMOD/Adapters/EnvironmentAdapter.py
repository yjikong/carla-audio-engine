import Code.FMOD.Classes.Model.SoundModel as SoundModel
from Code.FMOD.utils import Subscriber  

class EnvironmentAdapter(Subscriber):
    model = None

    def EnvironmentAdapter(self, model: SoundModel):
        self.model = model


    def receive(self, message):
        print(f"{self.name} received message: {message}")

    def evaluateWeatherChange():
        change= None
        parameter= 0
        return
