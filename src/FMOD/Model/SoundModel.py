import socket
from ..utils import DataKey
from ..utils import EventBus
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

class SoundModel:
    def __init__(self, event_bus: EventBus):
        self.bus = event_bus
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))

        self.client_data: dict[str, object] = {}

    def _decode(self) -> dict[str, object]:
        data, _ = self.sock.recvfrom(2048)
        # JSON-String to dictionary
        return json.loads(data.decode())
    
    def _calculate_diff(self, new_values: dict[str, object], old_values: dict[str, object]) -> dict[DataKey, object]:
        diff: dict[DataKey, object] = {}
        for key_str, value in new_values.items():
            if old_values.get(key_str) != value:
                try:
                    key_enum = DataKey(key_str)  # String -> Enum
                    diff[key_enum] = value
                except ValueError:
                    print(f"Unknown key received: {key_str}")
        return diff

    def on_tick(self) -> None:      
        old_data = self.client_data.copy()
        self.client_data = self._decode()

        diff = self._calculate_diff(self.client_data, old_data)

        for key, value in diff.items():
            self.bus.publish(key, value)

