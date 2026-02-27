from enum import Enum

class DataKey(str, Enum):
    """
    Enumeration of simulation data keys used for system-wide communication.

    This class defines the standardized keys used by the :class:`SoundModel` 
    to identify simulation variables received from the CARLA client. By 
    inheriting from ``str``, these members act as validated constants that 
    ensure consistency between the network layer, the EventBus, and the 
    various sound adapters.
    """

    ACCELERATION = "acceleration"
    """str: Vehicle acceleration vector or magnitude."""

    BRAKE = "brake"
    """str: Brake pedal input state ranging from 0.0 to 1.0."""

    COLLISION_EVENT = "collision_event"
    """str: Trigger key for vehicle impact detections."""

    GEAR = "gear"
    """str: Current transmission gear index (e.g., -1 for Reverse, 0 for Neutral)."""

    MESSAGE = "message"
    """str: General purpose system or debug messages."""

    RAIN_INTENSITY = "rain_intensity"
    """str: Precipitation percentage (0-100) used for ambient sound modulation."""

    SPEED = "speed"
    """str: Current vehicle velocity in km/h."""

    SPEED_LIMIT = "speed_limit"
    """str: Local speed limit for the current road segment in km/h."""

    THROTTLE = "throttle"
    """str: Throttle pedal input state ranging from 0.0 to 1.0."""

    WIND_INTENSITY = "wind_intensity"
    """str: Wind speed percentage (0-100) used for ambient sound modulation."""

    HONK = "honk"
    """str: State of the vehicle's horn trigger."""

    HANDBRAKE = "handbrake"
    """str: State of the manual parking brake engagement."""