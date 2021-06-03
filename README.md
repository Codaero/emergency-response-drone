# Drones

The drone software contained here has several functions. One function is to communicate with the drone to display important information as well as allow a user to arm and disarm with the click of a button in a GUI. In essence, this is a very basic ground control solution. The fully featured version of our software allows a potential first responder user to type in an adresss, click a spot on a map, and immediately deploy a drone to that location. In addition, telemetry and live video are streamed live; telemetry to the GUI and live video to a separate tab. 
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

The ability to command a waypoint by inputting latitude and longitude coordinates or clicking a location on a map. 

The ability to stream live video from the drone using either wifi connection or an LTE connection to reduce latency. 
### Future Features: 
Stream live video to the same GUI used for sending waypoints

Onboard Raspberry Pi running computer vision to identify objects from a height

Home location automatically set upon arm using drone's location rather than hard coded. 

Arming with Prearm checks and displaying corresponding acknowledgment messages
## Known Issues: 
Sometimes mission acknowledgment messages are not received properly after MISSION_REQUEST_INT messages. For now, changing MISSION_REQUEST_INT to MISSION_REQUEST, running the program again, and then changing it back fixes the problem. 

Sometimes, the waypoint shows that it is set below the home location. See Future Feature three for the soon-to-be-implemented fix for this. 
## Contributors 
Aditya Tolia, 
Arjun Shah, 
Robert Azarcon, 
Venkata Edupulapati
