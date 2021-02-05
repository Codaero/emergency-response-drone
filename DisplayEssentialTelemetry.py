import commands
import time
from tkinter import *
from tkinter.ttk import *
import pymavlink

class SimpleGUI:
    def __init__(self):
        #----#
        self.root = Tk()
        self.quit = False
        #----#
        style = Style()
        style.configure("BW.TLabel", foreground="white", background="#2a2b2e")
        #----#
        self.altVar = StringVar()
        self.alt = Label(self.root, text=self.altVar, style="BW.TLabel")
        
        self.airspdVar = StringVar()
        self.airspd = Label(self.root, text=self.airspdVar, style="BW.TLabel")

        self.grndspdVar = StringVar()
        self.grndspd = Label(self.root, text=self.grndspdVar, style="BW.TLabel")

        self.hdgVar = StringVar()
        self.hdg = Label(self.root, text=self.hdgVar, style="BW.TLabel")

        self.latLongVar = StringVar()
        self.latLong = Label(self.root, text=self.latLongVar, style="BW.TLabel")
        
        self.voltVar = StringVar()
        self.volt = Label(self.root, text=self.voltVar, style="BW.TLabel")

        self.fltModVar = StringVar()
        self.fltMod = Label(self.root, text=self.fltModVar, style="BW.TLabel")

        self.alt.pack()
        self.airspd.pack()
        self.grndspd.pack()
        self.hdg.pack()
        self.latLong.pack()
        self.volt.pack()
        self.fltMod.pack()

    def quitting(self): ##to set the quit flag
        self.quit = True

    def refreshLabels(self, data):
        self.altVar = 'Altitude: ' + data["altitude"]
        self.airspdVar = 'Airspeed: ' + data["airspeed"]
        self.grndspdVar = 'Groundspeed: ' + data["groundspeed"]
        self.hdgVar = 'Heading: ' + data["heading"]
        self.latVar = 'Lat + Long: ' + data["latitude"] + ' , ' + data["longitude"]
        self.voltVar = 'Voltage: ' + data["voltage"]
        self.fltModVar = 'Flight Mode: ' + data["flightMode"]
        #altitude, airspeed, groundspeed, heading, lat, long, voltage, flightMode
    
    def run(self): ##main part of the application
        self.root.configure(bg="#2a2b2e") #sets the background to white rather than default gray.
        self.root.protocol("WM_DELETE_WINDOW", self.quitting) ##changes the X (close) Button to run a function instead.
        self.root.title("Visual Telemetry GUI")
        self.root.geometry("800x600")

        master = commands.connect("COM4")
        commands.wait_heartbeat(master)

        #############################################################
        while not self.quit: ##flag to quit the application
            self.root.update_idletasks() #updates the root. same as root.mainloop() but safer and interruptable
            self.root.update() #same as above. This lest you stop the loop or add things to the loop.
            self.refreshLabels(commands.display_data(master))
            time.sleep(0.6)

if __name__ == "__main__":
    app = SimpleGUI() ##creates instance of GUI class
    try:
        app.run()# starts the application
    except KeyboardInterrupt:
        app.quitting() ##safely quits the application when crtl+C is pressed
    except:
        raise #you can change this to be your own error handler if needed