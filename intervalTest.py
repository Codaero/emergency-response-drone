import time
# Import mavutil
from pymavlink import mavutil


master = mavutil.mavlink_connection('COM4')
master.mav.command_long_send(master.target_system, master.target_component, 246, 0, 1, 0, 0,0,0,0,0)
try:
    print (master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_GET_MESSAGE_INTERVAL,0, 33 ,0,0,0,0,0,0))
except: 
    print ("This did not work")

master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0, 33, 2000, 0,0,0,0,0)

try:
    print (master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_GET_MESSAGE_INTERVAL,0, 33 ,0,0,0,0,0,0))
except: 
    print ("This did not work")