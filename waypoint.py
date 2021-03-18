import commands
import time
from pymavlink import mavutil

master = commands.connect("COM6")
commands.wait_heartbeat(master)
commands.upload_mission(master, 417956180, -881674020, 5)



