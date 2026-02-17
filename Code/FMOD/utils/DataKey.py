from enum import Enum

class DataKey(str, Enum):
    ACCELERATION = "acceleration"
    BRAKE = "brake"
    COLLISION_EVENT = "collision_event"
    GEAR = "gear"
    MESSAGE = "message"
    RAIN_INTENSITY = "rain_intensity"
    SPEED = "speed"
    SPEED_LIMIT = "speed_limit"
    THROTTLE = "throttle"
    WIND_INTENSITY = "wind_intensity"
    TICK = 1
