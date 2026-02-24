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
- __Speed Limit Alert__: Triggers a sound when exceeding 100km/h.
- __Reverse Gear Alert__: Plays a sound upon switching to reverse gears.
- __Handbrake Sound__: Features the tire squealing when the handbreak is applied.
- __EV Sound__: Simulates the characteristic audio of an Electrical-Car for operations.

>[!NOTE]
>*All sounds included in this repository are improvised and gathered from online sources.
They were not professionally designed and may vary in quality. This implementation is primarily intended 
as a proof of concept or starting point for further development.*
 


