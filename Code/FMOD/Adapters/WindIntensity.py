from ..utils import RangeLevel

class WindIntensity(RangeLevel):
    NONE = (0, 10, 0)
    LOW = (10, 55, 1)
    HIGH = (55, 100, 2)