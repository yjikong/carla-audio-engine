#!/usr/bin/env python3
from waapi import WaapiClient, CannotConnectToWaapiException

EVENT_ID = "{58EBC223-7952-48FA-A2E7-505C6FDD6E35}"
GAME_OBJECT_ID = 1000  # any integer is fine

try:
    with WaapiClient() as client:

        # Register a game object
        client.call("ak.wwise.core.audio.registerGameObj", {
            "gameObject": GAME_OBJECT_ID,
            "name": "PythonObj"
        })

        # Post the event
        result = client.call("ak.wwise.core.audio.postEvent", {
            "event": EVENT_ID,
            "gameObject": GAME_OBJECT_ID,
            "wait": True
        })

        print("Event posted:", result)

        # Unregister
        client.call("ak.wwise.core.audio.unregisterGameObj", {
            "gameObject": GAME_OBJECT_ID
        })

except CannotConnectToWaapiException:
    print("Could not connect to WAAPI. Is Wwise running and WAAPI enabled?")
