import commands
import time
from tkinter import *
from tkinter.ttk import *
import pymavlink

class SimpleGUI:
    def __init__(self, m):
        #----#
        #Instance variables
        self.root = Tk()
        self.quit = False
        self.master = m

        #----#
        #Styling
        style = Style()
        style.configure("BW.TLabel", foreground="white", background="#2a2b2e")
        #----#
        #Labels to display telemetry
        self.alt = Label(self.root, text='', style="BW.TLabel")
        self.airspd = Label(self.root, text='', style="BW.TLabel")
        self.grndspd = Label(self.root, text='', style="BW.TLabel")
        self.hdg = Label(self.root, text='', style="BW.TLabel")
        self.latLong = Label(self.root, text='', style="BW.TLabel")
        self.volt = Label(self.root, text='', style="BW.TLabel")
        self.fltMod = Label(self.root, text='', style="BW.TLabel")

        self.alt.pack()
        self.airspd.pack()
        self.grndspd.pack()
        self.hdg.pack()
        self.latLong.pack()
        self.volt.pack()
        self.fltMod.pack()

        #----#
        #Arming buttons
        self.arm = Label(self.root, text='Arm', function= lambda: commands.arm(self.master))
        self.disarm = Label(self.root, text='Arm', function= lambda: commands.disarm(self.master))

        self.arm.pack()
        self.disarm.pack()

    def quitting(self): ##to set the quit flag
        self.quit = True

    def refreshLabels(self, data):
        self.alt.configure(text = 'Altitude: ' + data["altitude"])
        self.airspd.configure(text = 'Airspeed: ' + data["airspeed"])
        self.grndspd.configure(text = 'Groundspeed: ' + data["groundspeed"])
        self.hdg.configure(text = 'Heading: ' + data["heading"])
        self.latLong.configure(text = 'Lat + Long: ' + data["latitude"] + ' , ' + data["longitude"])
        self.volt.configure(text = 'Voltage: ' + data["voltage"])
        self.fltMod.configure(text = 'Flight Mode: ' + data["flightMode"])
        #altitude, airspeed, groundspeed, heading, lat, long, voltage, flightMode
        self.alt.pack()
        self.airspd.pack()
        self.grndspd.pack()
        self.hdg.pack()
        self.latLong.pack()
        self.volt.pack()
        self.fltMod.pack()
    
    def run(self): ##main part of the application
        
        commands.wait_heartbeat(self.master)

        self.root.configure(bg="#2a2b2e") #sets the background to white rather than default gray.
        self.root.protocol("WM_DELETE_WINDOW", self.quitting) ##changes the X (close) Button to run a function instead.
        self.root.title("Visual Telemetry GUI")
        self.root.geometry("800x600")

        #############################################################
        while not self.quit: ##flag to quit the application
            self.root.update_idletasks() #updates the root. same as root.mainloop() but safer and interruptable
            self.root.update() #same as above. This lest you stop the loop or add things to the loop.
            self.refreshLabels(commands.display_data(self.master))
            time.sleep(0.1)

if __name__ == "__main__":
    master = commands.connect("COM4")
    commands.wait_heartbeat(master)
    app = SimpleGUI(master) ##creates instance of GUI class
    try:
        app.run()# starts the application
    except KeyboardInterrupt:
        app.quitting() ##safely quits the application when crtl+C is pressed
    except:
        raise #you can change this to be your own error handler if needed