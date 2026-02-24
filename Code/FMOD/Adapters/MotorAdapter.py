from pyfmodex.studio.enums import PLAYBACK_STATE

from ..Sounds.EVSound import *
from ..utils.EventBus import *
from Code.FMOD.Banks import TriggerBank
from Code.FMOD.utils import DataKey
from Code.FMOD.utils.DataKey import DataKey
from ..utils.EventBus import EventBus
from Code.FMOD.Banks import MotorBank
import keyboard


class MotorAdapter:
    def __init__(self, bus: EventBus, ev: EVSoundEngine, bank: MotorBank):
        self.ev = ev
        self.speed = 0
        self.throttle = 0
        self.bank = bank
        bus.subscribe(DataKey.SPEED, self.on_speed)
        bus.subscribe(DataKey.THROTTLE, self.on_throttle)

    def on_speed(self, speed):
        self.speed = speed
        self.update()

    def on_throttle(self, throttle):
        self.throttle = throttle
        self.update()

    def calculate_torque(self, speed, throttle):
        # Wenn Throttle 0 -> Torque 0
        if throttle == 0:
            return 0
        elif throttle > 0 and speed > 0:
            return 1
        elif throttle > 0 and speed < 0:
            return -0.8
        else:
            return 0

    def update(self):
        """Updates engine and sound states each frame"""
        if self.ev.is_running is False:
            self.ev.start()
        self.ev.update_params(self.speed, self.calculate_torque(self.speed, self.throttle))
        self.ev.system.update()

        self.bank.update()
