import commands
import time
from pymavlink import mavutil

master = commands.connect("COM5")
commands.waypoint(master, 41.782029, -88.155819, 5)
