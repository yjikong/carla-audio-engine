import time
from threading import Thread
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from Code.CARLA.Classes import *

def carla_data_loop(client, sock):
    while True:
        data_packet = client.retrieve_data()
        sock.publish_data(data_packet)
        time.sleep(0.05)

if __name__ == '__main__':
    client = CarlaClient('localhost', 2000, 30.0)
    weather = Weather(client)
    sock = Socket()
    carla_thread = Thread(target=carla_data_loop, args=(client, sock), daemon=True)
    carla_thread.start()
    weather.run()