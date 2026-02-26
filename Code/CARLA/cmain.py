"""
CARLA Operations Handler
========================
This module manages core CARLA operations, including client initialization, 
simulation data retrieval, and dynamic weather configuration.
"""

import time
from threading import Thread
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from Code.CARLA.Classes import *

def carla_data_loop(client, sock):
    """
    Executes a continuous data retrieval loop.

    Fetches the latest simulation state from the CARLA server and 
    broadcasts it via the specified UDP socket.

    Args:
        client (CarlaClient): Active instance of the CARLA client.
        sock (Socket): UDP socket instance used for publishing simulation packets.
    """
    while True:
        data_packet = client.retrieve_data()
        sock.publish_data(data_packet)
        time.sleep(0.05)

def main():
    """
    Main entry point for CARLA operations.

    Initializes the client and weather modules, then spawns a background 
    thread to handle the continuous data retrieval loop.
    """
    client = CarlaClient('localhost', 2000, 20.0)
    weather = Weather(client)
    sock = Socket()
    carla_thread = Thread(target=carla_data_loop, args=(client, sock), daemon=True)
    carla_thread.start()
    weather.run() 

if __name__ == '__main__':
    main()