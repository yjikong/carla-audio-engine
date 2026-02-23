from ..utils import RangeLevel

class RainIntensity(RangeLevel):
    NONE = (0, 10, 0)
    LOW = (10, 44, 1)
    MEDIUM = (44, 77, 2)
    HIGH = (77, 100, 3)