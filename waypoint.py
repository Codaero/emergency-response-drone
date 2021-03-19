import commands
import time
from pymavlink import mavutil

master = commands.connect("COM6")
commands.wait_heartbeat(master)
# commands.upload_mission(master, 417957240, -881662980, 5)
commands.set_mission(master)



