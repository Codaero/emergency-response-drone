import commands
import master
import time

m = commands.connect("COM5")

commands.wait_heartbeat(m)
time.sleep(2)
commands.upload_mission(m, 41.790762, -88.106582, 5)
