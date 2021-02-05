import commands
try: 
    master = commands.connect("COM4")
    commands.wait_heartbeat(master)
    print ("Arming") 
    print (master.messages['HEARTBEAT'].base_mode)
    print (master.messages['HEARTBEAT'].system_status)
    try: 
        commands.arm(master)
    except: 
        print ("disarming failed")
    commands.wait_heartbeat(master)
    print (master.messages['HEARTBEAT'].base_mode)
    print (master.messages['HEARTBEAT'].system_status) 
    print ("disarming")
    try: 
        commands.disarm(master)
    except: 
        print ("disarming failed")
    commands.wait_heartbeat(master)
    print (master.messages['HEARTBEAT'].base_mode)
    print (master.messages['HEARTBEAT'].system_status) 
except KeyboardInterrupt:
    print("Program Stopped")
