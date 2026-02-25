from enum import Enum

class RangeLevel(Enum):
    """
    Generic base class for level definitions with
    lower/upper bounds and a mapped output value.
    """
    def __init__(self, lower, upper, mapped_value):
        self.lower = lower
        self.upper = upper
        self.mapped_value = mapped_value

    def contains(self, value):
        """
        Checks whether the given value falls within this level's range.
        
        The lower bound is inclusive only if it is 0,
        otherwise it is treated as exclusive.
        """
        return self.lower < value <= self.upper if self.lower != 0 else self.lower <= value <= self.upper

    @classmethod
    def from_value(cls, value):
        """
        Returns the first level whose range contains the given value.
        Returns None if no matching level is found.
        """
        for level in cls:
            if level.contains(value):
                return level
        return None