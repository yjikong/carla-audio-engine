# Sound Implementation for CARLA

This repository contains the implementation of basic sound functionaliy 
for the CARLA simulator. The project was developed as part of an academic assignment and aims 
to enhance the realism of the simulation environment.

CARLA, widely used in research for autonomous driving and user experience (UX) 
design in automotive contexts, lacks built-in support for sound. Our contribution 
introduces a simple sound system for CARLA, intended to serve as a foundation for 
others who wish to implement basic sound effects. While not designed for full-fledged 
game audio, this code can be used as:

- A reference template to enable basic sounds for more immersive simulations.
- A starting point for understanding how sound integration in CARLA can be realized.

We hope this implementation will be helpful for researchers, students, and developers exploring the
integration of audio in the CARLA simulator.


## Implemented Sounds
This implementation introduces several basic sounds to enhance
the realism of CARLA´s simulation environment.
The following sounds are implemented:

- __Ambient Sounds__: Simulates environmental sounds such as wind and rain.
- __Crash Sounds__: Plays a sound to simulate collisions between vehicles and objects.
- __Speed Limit Alert__: Triggers a sound when exceeding 100 km/h.
- __Reverse Gear Alert__: Plays a sound upon switching to reverse gears.
- __Handbrake Sound__: Features the tire squealing when the handbreak is applied.
- __EV Sound__: Simulates the characteristic audio of an Electrical-Car for operations.

>[!NOTE]
>All sounds included in this repository are improvised and gathered from online sources.
They were not professionally designed and may vary in quality. This implementation is primarily intended 
as a proof of concept or starting point for further development.


## Installation and Setup

>[!TIP]
>Everything you need to know about what has to be installed and
> how to set up the project that every thing runs right is explained in
> this video: https://www.youtube.com/watch?v=hypM038aNzE
> >[!NOTE]
> >Video is in German so you might have to use subtitles.

First, you need to install FMOD Studio 2.02 and Engine 2.02, Carla version 0.9.15, and Python 3.8 and 3.12.
Use the following links to download the necessary files:
- [FMOD-STUDIO 2.02](https://www.fmod.com/download#fmodstudio)
- [FMOD-ENGINE 2.02](https://www.fmod.com/download#fmodengine)
- [CARLA 0.9.15](https://github.com/carla-simulator/carla/releases/tag/0.9.15/)
- [PYTHON 3.8 and 3.12](https://www.python.org/downloads/windows/)

After the installations are complete you can _clone_ the repository into your own IDE. 
Know you have to creat three different venvs for the project.

### 1. Carla Client Venv
For the Carla Client Venv you have to go into the Carla folder where the _Carla4UE.exe_ lies and start 
there a terminal or you directly navigate to the folder via the terminal.

After that you have to naviagte into the _PythonAPI_ and then into the _examples_ folder.
````Console
C:\Users\user\yourFolderWhereCarlaIs\WindowsNoEditor> cd PythonAPI\examples
````

Here you have to creata a venv with __Pyhton 3.8__.
````Console
C:\Users\user\yourFolderWhereCarlaIs\WindowsNoEditor\PythonAPI\examples> py -3.8 venv .venv38
````

After the venv is created you have to activate it. 
````Console
C:\Users\user\yourFolderWhereCarlaIs\WindowsNoEditor\PythonAPI\examples> .\.venv38\Scripts\activate
````

In the active venv you have to install a _requirements.txt_.
````Console
(.venv38) C:\Users\user\yourFolderWhereCarlaIs\WindowsNoEditor\PythonAPI\examples> pip install -r requirements.txt
````

This will take a while until all packages are installed. After that you have to install manualy carla in the venv.
````Console
(.venv38) C:\Users\user\yourFolderWhereCarlaIs\WindowsNoEditor\PythonAPI\examples> pip install carla
````

After that you can check with the command `pip list` if everything is installed correctly. And you can `deactivate` the venv.


>[!IMPORTANT]
> The next two venvs have to be created in the code structure of the project. So you have to clone the project into your IDE if not already done.
### 2. Carla Code Venv:
This venv has to be created in the _CARLA_ folder of our project. This part of the code connects with Carla 
and sends/receives data from the simulator.  
To create this venv you have to open a terminal in your IDE and direct to the Carla folder.
````Console
C:\Users\user\yourProjectFolder> cd Code\CARLA
````

Here you must now create a venv with __Python 3.8__, as for the Carla simulator.
````Console
C:\Users\user\yourProjectFolder\Code\CARLA> py -3.8 venv .venv38
````

And as with the venv for the simulator we have to activate it and install the _requirements.txt_.
````Console
C:\Users\user\yourProjectFolder\Code\CARLA> .\.venv38\Scripts\activate
````
````Console
(.venv38) C:\Users\user\yourProjectFolder\Code\CARLA> pip install -r requirements.txt
````


After the installation is complete you can `deactivate` the venv.

### 3. FMOD Code Venv:
This venv has to be created in the _FMOD_ folder of our project. This part of the code is responisble
for playing the sounds in the right events.  
To creat it you have to follow the same steps a befor:
- direct to the right folder
````Console
C:\Users\user\yourProjectFolder> cd Code\FMOD 
````
- create the venv with __Python 3.12__
````Console
C:\Users\user\yourProjectFolder\Code\FMOD> py -3.12 venv .venv38
````
- activate it
````Console
C:\Users\user\yourProjectFolder\Code\FMOD> .\.venv38\Scripts\activate
````
- install the requirements.txt
````Console
(.venv38) C:\Users\user\yourProjectFolder\Code\FMOD> pip install -r requirements.txt
````
- `deactivate` it


## Architecture
The system is divided into two parts—Carla and FMOD. The Carla part essentially handles the setup of 
and communication with the Carla simulator. The FMOD part handles sound playback.

### 1. Carla
The __CARLA part__ is responsible for connecting to the Carla simulator and providing the __simulation data__ that is later used by the 
FMOD subsystem for audio playback. Technically, it consists of a lightweight client that connects to the running Carla server,
locates/monitors the "hero" vehicle reads relevant state information, and __periodically sends it via UDP as JSON__ to a local receiver.

#### Folder structure
- `cmain.py`  
  Entry point for the Carla client. Starts the data loop (polling simulation values) and sends data packets at a fixed interval.
  It also launches a small weather UI to adjust weather parameters during runtim.
- `Classes\`  
  Contains the cor calsses for connecting, sensing, data transport, and UI:
  - `__init__.py`
  Exposes the main classes as package imports.
  - `CarlaClient.py`
  Encapsulates the Carla server connection, retrieves the `world`, searches for a vehicle, and continuously reads vehicle and environment data.
  It also attaches a collision sensor and produces a compact data packet (relevant for the sound logic).
  - `CollisionSensor.py`
  Implements a Carla collision sensor that counts collisions and measures their intensity, used to trigger crash events.
  - `Socket.py`
  Minimal UDP wrapper for sending JSON data (locally to 127.0.0.1 on a fix port)
  - `Weather.py`
  Small Tkinter GUI used to set rain and wind intensity in the running simulation.
- `generate_traffic.py`
Script to generate traffic in the simulator.
- `requirements.txt`
Python dependencies that are required for the Carla client (will be installed into a venv).

#### Data flow
1. `cmain.py` starts the client and the sender loop.
2. `CarlaClient` connects to the simulator, finds the ego/hero vehicle, and attaches a `CollisionSensor`.
3. At short intervals, it reads relevant states (vehicle motion/control, speed/speed limit, wheather, events like collisions/honk)
4. `Socket` serializes the values as JSON and sends them via UDP to the local receiver (FMOD subsystem).

__Goal of this module:__
Provide a robust and easily extensible interface between the Carla simulation and the sound system, without embedding sound logic directly inside the Carla side.


### 2. FMOD
The FMOD subsystem is based on an MVC architecture. This can be seen in the model and adapter classes.  
There are packages for adapters, banks, models, sounds, and utilities.

The model handles the retrieval and decoding of data relevant to the sound system, which is provided by a socket in the provided Carla Client.
The relevant data includes:
- Acceleration
- Brake
- Gear
- Speed 
- Speed eimit
- Handbrake
- Horn
- Collision event
- Message
- Rain intensity
- Wind intensity

Furthermore, the model compares this data for inequality. If a difference is detected, the change is published via an 
EventBus and the function registered by the subscribers is executed. The EventBus works similarly to the Publisher–Subscriber 
design pattern.

__Adapters__ subscribe to the data and provide functions that are executed when changes occur. They are divided into _Environment_ (for ambient sounds),
_Motor_ (for engine and braking sounds), and _Trigger_ (for events such as honking or collisions). In general, the adapters are responsible for playing 
the sounds with the correct parameters. This is done either through parameter changes and events in FMOD or through programmatically generated sounds in Python.

__Banks__ represent the Python interface for FMOD events. Within the respective classes, the events are initialized, played, and their parameters modified. 
The sounds for an electric vehicle and the reverse gear tone are generated using oscillators. They are located in the Sound package.

The __utils__ package contains the helper classes DataKey and EventBus. _DataKey_ manages ENUMs for the names of the data values. This ensures improved 
maintainability, scalability, a centralized interface definition, and the avoidance of typos. The _EventBus_ class distributes events without requiring 
senders and receivers to know each other. It enables loose coupling, better scalability, and—compared to the Observer or Pub-Sub pattern—offers 
the advantage that multiple senders and receivers can communicate through a single bus.

## Acknowledgments

This project uses the following third-party library:

- [__PYFMODEX__](https://github.com/tyrylu/pyfmodex)  
  Licensed under the [MIT License](https://opensource.org/licenses/MIT).  

Please ensure you comply with the MIT license terms when using or modifying this project.