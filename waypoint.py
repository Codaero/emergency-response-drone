import commands
import time
from pymavlink import mavutil

master = commands.connect("COM7")
commands.wait_heartbeat(master)
commands.arm(master)
#commands.request_message(master, 91)
# commands.wait_heartbeat(master)
#print (master.messages["HEARTBEAT"].base_mode)
#print (master.messages["HIL_CONTROLS"].nav_mode)
#commands.waypoint(master, 0, 0)
commands.change_mode(master, 'MISSION')
