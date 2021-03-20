  
import commands
import time
from pymavlink import mavutil

master = commands.connect("COM6")
commands.wait_heartbeat(master)
# commands.upload_mission(master, 417829610, -881561630, 217)
commands.change_mode(master, 'TAKEOFF')
commands.change_mode(master, 'MISSION')