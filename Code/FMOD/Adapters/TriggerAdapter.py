from ..utils import *
from ..Banks import *

class TriggerAdapter:
    def __init__(self, event_bus: EventBus, bank: MotorBank, events: dict):
        self.past_gear = None
        self.speed_trigger = False
        self.crash_trigger = False
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
            reverse_beep.play_reverse_beep()

    def on_speed(self, speed):
        if speed > 100:
            TriggerBank.warning_sound.start()
            self.speed_trigger = True
        if TriggerBank.warning_sound.playback_state == PLAYBACK_STATE.STOPPED:
            self.speed_trigger = False

    def on_crash(self, crash):
        if self.crash_trigger is False:
            TriggerBank.crash_sound.start()
            self.crash_trigger = True
        if TriggerBank.crash_sound.playback_state == PLAYBACK_STATE.STOPPED:
            self.crash_trigger = False
    
    def on_honk(self, honk):
        if keyboard.is_pressed('h'):
            TriggerBank.honk_sound.start()