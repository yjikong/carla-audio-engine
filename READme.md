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
C:\Users\user\yourFolderWhereCarlaIs\WindowsNoEditor\PythonAPI\examples>.venv38\Scripts\activate
````

In the active venv you have to install a _requirements.txt_.
````Console
(.venv38) C:\Users\user\yourFolderWhereCarlaIs\WindowsNoEditor\PythonAPI\examples> pip install -r requirements.txt
````

This will take a while until all packages are installed. After that you have to install manualy carla in the venv.
````Console
(.venv38) C:\Users\user\yourFolderWhereCarlaIs\WindowsNoEditor\PythonAPI\examples> pip install carla
````

After that you can check with the command `pip list` if everything is installed correctly. And you can deactivate the venv.


>[!IMPORTANT]
> The next two venvs have to be created in the code structure of the project. So you have to clone the project into your IDE if not already done.
### 2. Carla Code Venv:


### 3. FMOD Code Venv:


## Acknowledgments

This project uses the following third-party library:

- [__PYFMODEX__](https://github.com/tyrylu/pyfmodex)  
  Licensed under the [MIT License](https://opensource.org/licenses/MIT).  

Please ensure you comply with the MIT license terms when using or modifying this project.