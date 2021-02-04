import time
# Import mavutil
from pymavlink import mavutil

def wait_heartbeat(m):
    print("Waiting for APM heartbeat")
    m.wait_heartbeat()
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_system))

def show_messages(m):
    '''show incoming mavlink messages'''
    
    while True:
        msg = m.recv_match()
        if not msg:
            return
        if msg.get_type() == "BAD_DATA":
           return
        
                
        try: 
            altitude = master.messages['ALTITUDE'].altitude_monotonic
        except: altitude = "no data given"
        try:
            airspeed = master.messages['VFR_HUD'].airspeed
        except: airspeed = "no data given"
        try: 
            groundspeed = master.messages['VFR_HUD'].groundspeed
        except: groundspeed = "no data given"
        try: 
            heading = master.messages['VFR_HUD'].heading
        except: heading = "no data given"
        try: 
            gpslat = master.messages['GLOBAL_POSITION_INT'].lat
            gpslat /=10000000.0
        except: gpslat = "no data given"
        try:
            gpslong = master.messages['GLOBAL_POSITION_INT'].lon
            gpslong /=10000000.0
        except: gpslong = "no data given"
        try:
            volt = master.messages['SYS_STATUS'].voltage_battery
            volt /= 10000.0
        except: volt = "no data given"
        try: 
            mode = master.messages['HEARTBEAT'].base_mode
            modeString = " "
            if mode > 128: 
                modeString = "armed"
            else: 
                modeString = "unarmed"
        except: modeString = "no data given"
        try:
            print("altitude:     "  + str(altitude))
            print("airspeed:     " + str (airspeed))
            print("groundspeed:  " + str(groundspeed))
            print("heading:      " + str(heading))
            print("lat, long:    " + str(gpslat) + " , " + str(gpslong))
            print("voltage:      " + str(volt))
            print ("Flight mode: " + str(modeString))
        except:
            print ("No data recieved")
        
 
        time.sleep(0.01)
try: 
    master = mavutil.mavlink_connection("COM4")
    wait_heartbeat(master)

    print ("Sending Stream request")

    while True: 
        show_messages(master)
except KeyboardInterrupt:
    print("Program Stopped")