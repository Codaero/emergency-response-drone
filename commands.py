import time
from pymavlink import mavutil
from pymavlink import mavwp

# This method opens a connection and returns an object corresponding to that connection. baud rate defaults to 57600.
# @param port the port to connect to (using "COM4")
# @return an object that corresponds to the connection between the computer and the pixhawk.


def connect(port):
    return mavutil.mavlink_connection(port, baud=57600)

# waits for a heartbeat message from the connection before continuing.
# @param m the connection


def wait_heartbeat(m):
    print("Waiting for APM heartbeat")
    m.wait_heartbeat()
    print("Heartbeat from APM (system %u component %u)" %
          (m.target_system, m.target_system))

# Requests a message from the pixhawk according to its message id
# @param m the connection
# @param id the message id requested (can be found on common.xml)


def request_message(m, id):
    try:
        m.mav.command_long_send(
            m.target_system,
            m.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
            0,
            id, 0, 0, 0, 0, 0, 0)
        return m.recv_match(type='SYS_STATUS', blocking=True)
    except Exception as e:
        print(e)
# generates essential data by requesting mavlink messages and returns the data as a python dictionary
# @param m the connection
# @return a dictionary of essential telemetry to be used by a GUI


def display_data(m):
    while True:
        wait_heartbeat(m)
        request_message(m, 24)
        request_message(m, 74)
        request_message(m, 141)
        request_message(m, 1)
        try:
            altitude = m.messages['ALTITUDE'].altitude_monotonic
        except:
            altitude = "no data given"
        try:
            airspeed = m.messages['VFR_HUD'].airspeed
        except:
            airspeed = "no data given"
        try:
            groundspeed = m.messages['VFR_HUD'].groundspeed
        except:
            groundspeed = "no data given"
        try:
            heading = m.messages['VFR_HUD'].heading
        except:
            heading = "no data given"
        try:
            gpslat = m.messages['GPS_RAW_INT'].lat
            gpslat /= 10000000.0
        except:
            gpslat = "no data given"
        try:
            gpslong = m.messages['GPS_RAW_INT'].lon
            gpslong /= 10000000.0
        except:
            gpslong = "no data given"
        try:
            volt = m.messages['SYS_STATUS'].voltage_battery
            volt /= 1000.0
        except:
            volt = "no data given"
        try:
            mode = m.messages['HEARTBEAT'].base_mode
            modeString = " "
            if mode > 128:
                modeString = "armed"
            else:
                modeString = "unarmed"
        except:
            modeString = "no data given"
        exportedData = {
            "altitude": str(altitude),
            "airspeed": str(airspeed),
            "groundspeed": str(groundspeed),
            "heading": str(heading),
            "latitude": str(gpslat),
            "longitude": str(gpslong),
            "voltage": str(volt),
            "flightMode": str(modeString)
        }
        return exportedData

# arms the drone using a command_long command
# @param m the connection


def arm(m):
    m.mav.command_long_send(
        m.target_system,
        m.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1, 21196, 0, 0, 0, 0, 0)
# disarms the drone using a command_long command
# @param m the connection


def disarm(m):
    m.mav.command_long_send(
        m.target_system,
        m.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        0, 0, 0, 0, 0, 0, 0)
# reboots the autopilot using a command_long command
# param m the connection


def reboot(m):
    m.mav.command_long_send(
        m.target_system,
        m.target_component,
        mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN,
        0,
        1, 0, 0, 0, 0, 0, 0)

# sets a waypoint on the drone given the latitude and longitude
# param m the connection
# param lat the latitude
# param long the longitude
def takeoff(m, lat, long, altitude):
    change_mode(m, 'MISSION')

def waypoint(m, lat, long, altitude):
    set_mission(m)
    m.mav.command_long_send(
        m.target_system,
        m.target_component,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        0,
        40, 2, 0, 'NaN', lat, long, altitude)


def change_mode(m, mode):
    m.set_mode(mode)
    # while True:
    #     ack_msg = m.recv_match(type='COMMAND_ACK', blocking=True)
    #     ack_msg = ack_msg.to_dict()
    #     if ack_msg['command'] != mavutil.mavlink.MAVLINK_MSG_ID_SET_MODE:
    #         continue
    #     print(mavutil.mavlink.enums['MAV_RESULT']
    #           [ack_msg['result']].description)
    #     break
def set_mission(m):
    m.mav.command_long_send(
    m.target_system, m.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
    157, 4, 4, 0, 0, 0, 0)
def set_home(m, home_location, altitude):
    print('--- ', m.target_system, ',', m.target_component)
    m.mav.command_long_send(
        m.target_system, m.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_HOME,
        1, # set position
        0, # param1
        0, # param2
        0, # param3
        0, # param4
        home_location[0], # lat
        home_location[1], # lon
        altitude) 

def upload_mission(m, lat, longit, altitude):
    altitude+=216.2
    home_location = (41.7953585787946, -88.16649693012819)
    # start a UDP connection , port #: 14550: ON HOLD 
    # create wploader object 
    wp = mavwp.MAVWPLoader()
    # create and add home waypoint 
    homewaypointItem = mavutil.mavlink.MAVLink_mission_item_int_message(m.target_system, 
    m.target_component, 0, 0 , 16, 0, 1,
    0, 2, 0, 0, 417953585, -881664969, 219.2)
    wp.add(homewaypointItem)
    # create and add takeoff mission item 
    takeoffItem = mavutil.mavlink.MAVLink_mission_item_int_message(m.target_system, m.target_component, 1, 0, 24,0, 1, 0, 0, 0.5, 0, 0, 0, 5) # may need to reset origin if this doesn't work
    wp.add(takeoffItem)
    # create and add loiter mission item (maybe do later?)
    # create and add waypoint mission item 
    waypointItem = mavutil.mavlink.MAVLink_mission_item_int_message(m.target_system, 
    m.target_component, 2, 0 , 16, 0, 1,
    0, 2, 0, 0, lat, longit, altitude)
    wp.add(waypointItem)
    # create and add land mission item 
    landItem = mavutil.mavlink.MAVLink_mission_item_int_message(m.target_system,
    m.target_component, 3, 0, 21, 0, 1, 0,0,0,0, lat, longit, 0)
    wp.add(landItem)
    # send home and receive acknowledgment message 
    set_home(m, home_location, 222.2)
    msg = m.recv_match(type = ['COMMAND_ACK'],blocking = True)
    print(msg)
    print('Set home location: {0} {1}'.format(home_location[0],home_location[1]))
    time.sleep(1)
    # clear all mission items from pixhawk via clear_all_send
    
    m.waypoint_clear_all_send()
    wait_heartbeat(m)
    m.waypoint_count_send(wp.count())
    msg = m.recv_match(type=['MISSION_ACK'], blocking=True)
    print(msg)
    for i in range(wp.count()):
        msg = m.recv_match(type=['MISSION_REQUEST'], blocking=True, timeout=250)
        print(msg)
        m.mav.send(wp.wp(msg.seq))
        # msg = m.recv_match(type=['MAV_CMD_ACK'], blocking=True, timeout=250)
        # print(msg)
        print('Sending waypoint')
    #checking if mission upload is completed
    mission_ack = m.recv_match(type=['MISSION_ACK'], blocking=True)
    print(mission_ack)