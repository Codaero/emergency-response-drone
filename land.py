import commands
import time
from pymavlink import mavutil

master = commands.connect("COM6")
commands.wait_heartbeat(master)
commands.change_mode(master, 'LAND')
