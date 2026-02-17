from ..utils import *
from ..Banks import *
from ..Sounds import *
import keyboard
import time

import pyfmodex
from pyfmodex.studio import StudioSystem 
from pyfmodex.studio.enums import PLAYBACK_STATE
from pyfmodex.exceptions import FmodError

class TriggerAdapter:
    def __init__(self, event_bus: EventBus, bank: TriggerBank, events: dict):
        self.past_gear = None
        self.speed_trigger = False
        self.crash_trigger = False
        self.reverse_beep = ReverseBeep()
        self.bank = bank
        event_bus.subscribe(DataKey.GEAR, self.on_reverse)
        event_bus.subscribe(DataKey.COLLISION_EVENT, self.on_crash)
        event_bus.subscribe(DataKey.SPEED, self.on_speed)

    def on_reverse(self, current_gear):
        val = None
        if current_gear == -1 and self.past_gear == None:
            val = True
        elif current_gear == -1 and self.past_gear !=-1:
            val = True
        elif current_gear == -1 and self.past_gear == -1:
            val = False
        self.past_gear = current_gear
        if val == True:
            self.reverse_beep.play()
        self.reverse_beep.update()

    def on_speed(self, speed=0):
        self.reverse_beep.update()
        if speed > 100 and self.speed_trigger is False:
            self.bank.play_warning()
            self.speed_trigger = True
        if self.bank.warning_sound.playback_state == PLAYBACK_STATE.STOPPED:
            self.speed_trigger = False

    def on_crash(self, crash):
        if self.crash_trigger is False:
            self.bank.play_crash()
            self.crash_trigger = True
        if self.bank.crash_sound.playback_state == PLAYBACK_STATE.STOPPED:
            self.crash_trigger = False
    
    def on_honk(self, honk):
        if keyboard.is_pressed('h'):
            self.bank.play_honk()