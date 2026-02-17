from ..utils import *
from ..Banks import *
from ..Sounds import *
import keyboard
import time

import pyfmodex
from pyfmodex.studio import StudioSystem 
from pyfmodex.studio.enums import PLAYBACK_STATE
from pyfmodex.exceptions import FmodError

'''
Erklärung für self.honk_counter:
In SoundModel.py wird bei jeder Änderung des Wertes von Honk der Wert veröffentlicht.
Bei einem Tastendruckt wurde also honk immer doppelt getriggert.
durch die Einführung des Zählers und der Abfrage ob der Zähler gerade ist, wird 
das Event nur noch korrekt ein einziges Mal abgespielt
'''

class TriggerAdapter:
    def __init__(self, event_bus: EventBus, bank: TriggerBank, events: dict):
        self.past_gear = None
        self.speed_trigger = False
        self.crash_trigger = False
        self.honk_trigger = False
        self.reverse_beep = ReverseBeep()
        self.bank = bank
        self.honk_counter = 0
        event_bus.subscribe(DataKey.GEAR, self.on_reverse)
        event_bus.subscribe(DataKey.COLLISION_EVENT, self.on_crash)
        event_bus.subscribe(DataKey.SPEED, self.on_speed)
        event_bus.subscribe(DataKey.TICK, self.on_tick)
        event_bus.subscribe(DataKey.HONK, self.on_honk)

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

    def on_tick(self, tick):
        self.reverse_beep.update()
        self.bank.update()

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
        if self.honk_trigger is False and self.honk_counter % 2 == 0:
            self.bank.play_honk()
            self.crash_trigger = True
        if self.bank.honk_sound.playback_state == PLAYBACK_STATE.STOPPED:
            self.honk_trigger = False
        self.honk_counter = self.honk_counter + 1