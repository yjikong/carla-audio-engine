import queue

from Code.FMOD.utils import Subscriber

class Publisher:
    def __init__(self):
        self.message_queue = queue.Queue()
        self.subscribers: Subscriber = []

    def subscribe(self, subscriber: Subscriber):
        self.subscribers.append(subscriber)

    def publish(self, message:tuple):
        self.message_queue.put(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)