# drones

The drone software contained here has several functions. One function is to communicate with the drone to display important information as well as allow a user to arm and disarm with the click of a button in a GUI. In essence, this is a very basic ground control solution. We are currently working on developing programs to command a waypoint, deliver an AED, and stream live video. 
## Requirements
Python 2.8 or later, which can be downloaded from their website. 

The requirements.txt file that can be found in the repository. 
## Installation

Navigate to the directory where the requirements.txt document is stored using the cd command. Install all requirements using pip install.

```bash
pip install -r requirements.txt
```

## Usage

```bash
C:\__PATH_TO_VENV_FOLDER_\Scripts\activate.bat #activate the virtual environment
C:\_PATH_TO_DRONE_REPOSITORY_\DisplayEssentialTelemetry.py #run the ground control GUI
```
## Features
### Current Features: 
Displays telemetry, such as airspeed, groundspeed, battery level, heading, altitude, and GPS coordinates. Future updates will include number of satellites. 

Arm and Disarm with a single button. WARNING: As of right now, it forces arm. DO NOT FLY in current configuration. Future releases will address this.  
### Future Features: 
The ability to command a waypoint by inputting latitude and longitude coordinates or clicking a location on a map. 

The ability to stream live video from the drone using either wifi connection or an LTE connection to reduce latency. 

## Contributors 
Aditya Tolia, 
Arjun Shah, 
Robert Azarcon, 
Venkata Edupulapati
