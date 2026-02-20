import time
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from Code.CARLA.Classes import *

if __name__ == '__main__':
    client = CarlaClient('localhost', 2000, 10.0)
    weather = Weather(client)
    sock = Socket()

    weather.run()

    while True:
        data_packet = client.retrieve_data()
        sock.publish_data(data_packet)
        time.sleep(0.05)