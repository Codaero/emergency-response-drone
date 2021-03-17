from pymavlink import mavutil, mavwp
import commands
import time

# python /usr/local/bin/mavproxy.py --mav=/dev/tty.usbserial-DN01WM7R --baudrate 57600 --out udp:127.0.0.1:14540 --out udp:127.0.0.1:14550
connection_string = '127.0.0.1:14540'

mav = commands.connect("COM6")
commands.wait_heartbeat(mav)
print("HEARTBEAT OK\n")

# Make Waypoints
wp = mavwp.MAVWPLoader()

waypoints = [
        (37.5090904347, 127.045094298),
        (37.509070898, 127.048905867),
        (37.5063678607, 127.048960654),
        (37.5061713129, 127.044741936),
        (37.5078823794, 127.046914506)
        ]

home_location = waypoints[0]

seq = 0
for waypoint in enumerate(waypoints):
    frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
    seq = waypoint[0]
    lat, lon = waypoint[1]
    altitude = 15 # 15 meter
    autocontinue = 1
    current = 0
    param1 = 15.0 # minimum pitch
    if seq == 0: # first waypoint to takeoff
        current = 1
        p = mavutil.mavlink.MAVLink_mission_item_int_message(mav.target_system, mav.target_component, seq, frame, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, current, autocontinue, param1, 0, 0, 0, lat, lon, altitude)
    elif seq == len(waypoints) - 1: # last waypoint to land
        p = mavutil.mavlink.MAVLink_mission_item_int_message(mav.target_system, mav.target_component, seq, frame, mavutil.mavlink.MAV_CMD_NAV_LAND, current, autocontinue, 0, 0, 0, 0, lat, lon, altitude)
    else:
        p = mavutil.mavlink.MAVLink_mission_item_int_message(mav.target_system, mav.target_component, seq, frame, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, current, autocontinue, 0, 0, 0, 0, lat, lon, altitude)
    wp.add(p)

# Set Home location
def cmd_set_home(home_location, altitude):
    mav.mav.command_long_send(
        mav.target_system, mav.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_HOME,
        1, # set position
        0, # param1
        0, # param2
        0, # param3
        0, # param4
        home_location[0], # lat
        home_location[1], # lon
        altitude) # alt

def cmd_get_home():
    mav.mav.command_long_send(
        mav.target_system, mav.target_component,
        mavutil.mavlink.MAV_CMD_GET_HOME_POSITION,
        0, 0, 0, 0, 0, 0, 0, 0)
    msg = mav.recv_match(type=['COMMAND_ACK'],blocking=True)
    print (msg)
    msg = mav.recv_match(type=['HOME_POSITION'],blocking=True)
    return (msg.latitude, msg.longitude, msg.altitude)


# Send Home location
cmd_set_home(home_location, 0)
msg = mav.recv_match(type=['COMMAND_ACK'],blocking=True)
print (msg)
print ('Set home location: {0} {1}'.format(home_location[0], home_location[1]))
time.sleep(1)
 
# Get Home location
home_location = cmd_get_home()
print ('Get home location: {0} {1} {2}'.format(home_location[0], home_location[1], home_location[2]))
time.sleep(1)

# Send Waypoint to airframe
mav.waypoint_clear_all_send()
mav.waypoint_count_send(wp.count())

for i in range(wp.count()):
    msg = mav.recv_match(type=['MISSION_REQUEST_INT'],blocking=True)
    mav.mav.send(wp.wp(msg.seq))
    print ('Sending waypoint {0}'.format(msg.seq))       

msg = mav.recv_match(type=['MISSION_ACK'],blocking=True) # OKAY
print (msg.type)
