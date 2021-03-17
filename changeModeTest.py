import commands
import time
from pymavlink import mavutil

master = commands.connect("COM6")
commands.wait_heartbeat(master)
commands.arm(master)
print('arming')
master.set_mode('MANUAL')
print('Changing into Manual mode')
time.sleep(10)
master.set_mode('ACRO')
print('Changing into acro mode')
time.sleep(10)
master.set_mode('MISSION')
print('Changing into Mission mode')
time.sleep(10)
commands.disarm(master); 

