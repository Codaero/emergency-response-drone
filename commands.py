import time
from pymavlink import mavutil


def connect(port):
    return mavutil.mavlink_connection(port, baud=57600)


def wait_heartbeat(m):
    print("Waiting for APM heartbeat")
    m.wait_heartbeat()
    print("Heartbeat from APM (system %u component %u)" %
          (m.target_system, m.target_system))


def request_message(m, id):
    try:
        m.mav.command_long_send(
            m.target_system,
            m.target_component,
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
            0,
            id, 0, 0, 0, 0, 0, 0)
    except:
        print("interval not requested")


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
