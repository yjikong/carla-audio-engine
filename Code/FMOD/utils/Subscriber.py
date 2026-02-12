from abc import ABC, abstractmethod

class Subscriber(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def receive(self, message: tuple):
        pass