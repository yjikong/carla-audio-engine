from enum import Enum

class RangeLevel(Enum):
    """Allgemeine Basisklasse für Stufen mit Lower/Upper Bound und Wert"""
    def __init__(self, lower, upper, mapped_value):
        self.lower = lower
        self.upper = upper
        self.mapped_value = mapped_value

    def contains(self, value):
        """Prüft, ob der Wert in dieser Stufe liegt"""
        return self.lower < value <= self.upper if self.lower != 0 else self.lower <= value <= self.upper

    @classmethod
    def from_value(cls, value):
        """Gibt die Stufe zurück, die den Wert enthält"""
        for level in cls:
            if level.contains(value):
                return level
        return None