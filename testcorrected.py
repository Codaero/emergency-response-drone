import time
# Import mavutil
from pymavlink import mavutil

# Create the connection
#  If using a companion computer
#  the default connection is available
#  at ip 192.168.2.1 and the port 14550
# Note: The connection is done with 'udpin' and not 'udpout'.
#  You can check in http:192.168.2.2:2770/mavproxy that the communication made for 14550
#  uses a 'udpbcast' (client) and not 'udpin' (server).
#  If you want to use QGroundControl in parallel with your python script,
#  it's possible to add a new output port in http:192.168.2.2:2770/mavproxy as a new line.
#  E.g: --out udpbcast:192.168.2.255:yourport

master = mavutil.mavlink_connection('COM7')


master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
    74, 0.01, 0, 0, 0, 0, 0, 0)


# Get some information !


while True:
    try:
        # if master.recv_match().to_dict().get('mavpackettype') == "VFR_HUD":
        print(master.recv_match().to_dict())
        print("\n \n \n")
    except:
        pass
    time.sleep(0.01)  # frequency of trying to get data
