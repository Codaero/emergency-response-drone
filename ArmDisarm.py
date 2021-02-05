import time
# Import mavutil
from pymavlink import mavutil


def wait_heartbeat(m):
    print("Waiting for APM heartbeat")
    m.wait_heartbeat()
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_system))
def arm(m): 
    m.mav.command_long_send(
    m.target_system,
    m.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 21196, 0, 0, 0, 0, 0)
def disarm(m):
    m.mav.command_long_send(
    m.target_system,
    m.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    0, 0, 0, 0, 0, 0, 0)
def reboot(m): 
    m.mav.command_long_send(
    m.target_system,
    m.target_component,
    mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN,
    0,
    1, 0, 0, 0, 0, 0, 0)
try: 
    master = mavutil.mavlink_connection("COM4")
    wait_heartbeat(master)
    print ("Arming") 
    print (master.messages['HEARTBEAT'].base_mode)
    print (master.messages['HEARTBEAT'].system_status)
    try: 
        arm(master)
    except: 
        print ("disarming failed")
    wait_heartbeat(master)
    print (master.messages['HEARTBEAT'].base_mode)
    print (master.messages['HEARTBEAT'].system_status) 
    print ("disarming")
    try: 
        disarm(master)
    except: 
        print ("disarming failed")
    wait_heartbeat(master)
    print (master.messages['HEARTBEAT'].base_mode)
    print (master.messages['HEARTBEAT'].system_status) 
except KeyboardInterrupt:
    print("Program Stopped")
