import commands
import time
from pymavlink import mavutil

master = commands.connect("COM7")
commands.waypoint(master, 41.782090, -88.156301, 5)
