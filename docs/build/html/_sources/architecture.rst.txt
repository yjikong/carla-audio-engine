Architecture
============

The system is designed as a decoupled dual-subsystem environment consisting of **Carla** and **FMOD**. 

* **Carla Subsystem:** Handles the simulation environment, vehicle physics, and state sensing.
* **FMOD Subsystem:** Manages spatial audio, procedural sound generation, and event-based playback.

.. contents:: Table of Contents
   :depth: 2
   :local:

---

1. Carla Subsystem
------------------

The **Carla part** is responsible for connecting to the Carla simulator and providing the simulation data used by the FMOD subsystem. It consists of a lightweight client that monitors the "hero" vehicle and periodically sends state information via UDP as JSON to a local receiver.

Folder Structure
~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - File/Folder
     - Description
   * - ``cmain.py``
     - Entry point. Starts the data loop and the weather adjustment UI.
   * - ``Classes/``
     - Core logic for connectivity, sensing, and data transport.
   * - ``Classes/CarlaClient.py``
     - Manages server connection, "hero" vehicle tracking, and data polling.
   * - ``Classes/CollisionSensor.py``
     - Monitors impact intensity and counts to trigger crash events.
   * - ``Classes/Socket.py``
     - UDP wrapper for local JSON transmission (127.0.0.1).
   * - ``Classes/Weather.py``
     - Tkinter-based GUI for real-time rain and wind manipulation.
   * - ``generate_traffic.py``
     - Utility script to populate the simulation with NPC vehicles.
   * - ``requirements.txt``
     - Python dependencies for the Carla environment.

Data Flow
~~~~~~~~~

1. **Initialization:** ``cmain.py`` initializes the client and the sender loop.
2. **Detection:** ``CarlaClient`` locates the ego vehicle and attaches the ``CollisionSensor``.
3. **Polling:** The system reads vehicle motion, speed limits, weather, and discrete events (honks/crashes).
4. **Transmission:** ``Socket`` serializes the state into JSON and broadcasts it via UDP.

---

2. FMOD Subsystem
-----------------

The **FMOD part** handles audio logic. It utilizes an **MVC-style** split: **Model** (data receiving/diffing), **Adapters** (logic/controllers), and **Banks/Sounds** (audio resources).

Folder Structure
~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - File/Folder
     - Description
   * - ``fmain.py``
     - Subsystem entry point. Initializes the EventBus, Banks, and SoundModel.
   * - ``Model/SoundModel.py``
     - Receives UDP packets and computes the **difference** (diffing) between states.
   * - ``utils/``
     - Infrastructure tools: ``EventBus`` (Pub/Sub), ``DataKey`` (Enums), and ``RangeLevel``.
   * - ``Adapters/``
     - Translation layer. Subscribes to ``DataKeys`` to trigger audio actions.
   * - ``Banks/``
     - Interface for loading ``.bank`` files and managing FMOD Studio events.
   * - ``Sounds/``
     - Procedural audio generators (EV motor synthesis and reverse beeps).

Data Flow & Processing
~~~~~~~~~~~~~~~~~~~~~~

The FMOD subsystem operates on a reactive "diffing" principle to optimize performance:

1. **Bootstrapping:** ``fmain.py`` creates the ``EventBus`` and loads FMOD Banks.
2. **Ingestion:** ``SoundModel`` listens for JSON packets.
3. **Diffing:** To reduce overhead, the model compares the new packet to the previous state. **Only changed values** are published to the ``EventBus``.
4. **Reaction:**
    * **Continuous Values:** (e.g., Speed) updated as FMOD parameters or DSP frequencies.
    * **Trigger Values:** (e.g., Collision) handled via gating logic to prevent double-triggering.
5. **Update Loop:** The main loop ticks the FMOD Studio engine to keep audio in sync with the simulation.

.. note::
   The procedural EV motor sound is handled primarily via ``Sounds/EVSound.py`` rather than a static bank to allow for dynamic frequency shifts based on simulated torque.

---