from pymavlink import mavutil, mavwp
import commands
import time

# python /usr/local/bin/mavproxy.py --mav=/dev/tty.usbserial-DN01WM7R --baudrate 57600 --out udp:127.0.0.1:14540 --out udp:127.0.0.1:14550
connection_string = '0.0.0.0:14540'

mav = commands.connect("udp:" + connection_string)
commands.wait_heartbeat(mav)
print("HEARTBEAT OK\n")

# Make Waypoints
wp = mavwp.MAVWPLoader()

waypoints = [
        (37.5090904347, 127.045094298),
        (375090708, 1270489058),
        (375063678, 1270489606),
        (375061713, 1270447419),
        (375078823, 1270469145)
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


# Read Waypoint from airframe
mav.waypoint_request_list_send()
waypoint_count = 0

msg = mav.recv_match(type=['MISSION_COUNT'],blocking=True)
waypoint_count = msg.count
print (msg.count)

for i in range(waypoint_count):
    mav.waypoint_request_send(i)
    msg = mav.recv_match(type=['MISSION_ITEM_INT'],blocking=True)
    print ('Receving waypoint {0}'.format(msg.seq))       
    print (msg)

mav.mav.mission_ack_send(mav.target_system, mav.target_component, 0) # OKAY


# Change Mission Mode
empty = 0
#PX4_MAV_MODE = 81.0;
PX4_MAV_MODE = 209.0
PX4_CUSTOM_MAIN_MODE_AUTO = 4.0
PX4_CUSTOM_SUB_MODE_AUTO_MISSION = 4.0
PX4_CUSTOM_SUB_MODE_AUTO_RTL = 5.0

mav.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
                          PX4_MAV_MODE,
                          PX4_CUSTOM_MAIN_MODE_AUTO, PX4_CUSTOM_SUB_MODE_AUTO_MISSION, 0, 0, 0, 0)

msg = mav.recv_match(type=['COMMAND_ACK'],blocking=True)
print (msg)

# Send Heartbeat
mav.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 192, 0, 4)

# ARM
mav.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
                          1,
                          0, 0, 0, 0, 0, 0)
msg = mav.recv_match(type=['COMMAND_ACK'],blocking=True)
print (msg)


# Monitor mission progress
nextwaypoint = 0

def handle_mission_current(msg, nextwaypoint):
    if msg.seq > nextwaypoint:
        print ("Moving to waypoint %s" % msg.seq)
        nextwaypoint = msg.seq + 1
        print ("Next Waypoint %s" % nextwaypoint)
    return nextwaypoint

def handle_global_position_int(msg):
    #print " Latitude: ", msg.lat / 100.0
    #print " Longitude: ", msg.lon / 100.0
    #print " Altitude: ", msg.relative_alt / 1000.0
    #Break and return from function just below target altitude.        
    #if msg.relative_alt>=15*1000*0.95: 
    #    print "Reached target altitude"
    return

relative_alt = 0

while True:
    msg = mav.recv_match(type=['GLOBAL_POSITION_INT', 'MISSION_CURRENT', 'MISSION_COUNT', 'HEARTBEAT'],blocking=True,timeout=0.5)
    try:
        if msg.get_type() == 'HEARTBEAT':
            mav.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 192, 0, 4)
        #if msg.get_type() == 'MISSION_COUNT':
            #waypoint_count = msg.count
        #print "waypoint_count %s" % waypoint_count
        if msg.get_type() == 'GLOBAL_POSITION_INT':
            handle_global_position_int(msg)
            relative_alt = msg.relative_alt
        if msg.get_type() == 'MISSION_CURRENT':
            nextwaypoint = handle_mission_current(msg, nextwaypoint)
            #print 'Next Waypoint %s' % nextwaypoint
            if nextwaypoint >= waypoint_count - 1:
                if relative_alt<=1*1000*0.05: 
                    print ("Reached land altitude")
                    break
        time.sleep(0.1)
        mav.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 192, 0, 4) # send heart beat to airframe per 1 sec

    except KeyboardInterrupt:
        break

# DISARM
mav.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
                          0,
                          0, 0, 0, 0, 0, 0)
msg = mav.recv_match(type=['COMMAND_ACK'],blocking=True)
print (msg)

time.sleep(1)