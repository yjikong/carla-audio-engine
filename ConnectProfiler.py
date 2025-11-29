#!/usr/bin/env python3
from waapi import WaapiClient, CannotConnectToWaapiException
from pprint import pprint

try:
    # Connecting to Waapi using default URL
    with WaapiClient() as client:
        
        # Beispiel 1: Projektinfo abrufen
        project_info = client.call("ak.wwise.core.getInfo")
        print("\n=== Projektinfo ===")
        pprint(project_info)

        # Beispiel 2: Alle Soundbanks abrufen
        soundbanks = client.call("ak.wwise.core.soundbank.getList")
        print("\n=== Soundbanks im Projekt ===")
        pprint(soundbanks)

except CannotConnectToWaapiException:

    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")