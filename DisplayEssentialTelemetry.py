import commands
try: 
    master = commands.connect("COM4")
    commands.wait_heartbeat(master)
    while True:
        print (commands.display_data(master))
except KeyboardInterrupt:
    print("Program Stopped")