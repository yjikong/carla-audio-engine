from collections import defaultdict
from typing import Callable, Any
from src.FMOD.utils.DataKey import DataKey


class EventBus:
    def __init__(self):
        self._subscribers: dict[DataKey, list[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, key: DataKey, callback: Callable[[Any], None]) -> None:
        self._subscribers[key].append(callback)

    def unsubscribe(self, key: DataKey, callback: Callable[[Any], None]) -> None:
        self._subscribers[key].remove(callback)

    def publish(self, key: DataKey, data: Any) -> None:
        for callback in self._subscribers[key]:
            callback(data)
