import commands
import time
from tkinter import *
from tkinter.ttk import *
import pymavlink


class SimpleGUI:
    def __init__(self, m):
        #----#
        # Instance variables
        self.root = Tk()
        self.quit = False

        # communcation established
        self.comsEstablished = True

        # comm port selection
        self.comPortSelected = False
        self.comPortNum = StringVar()
<<<<<<< Updated upstream
        comPorts = ['2', '3', '4', '5', '6', '7', '8']
=======
        comPorts = ['2','3','4','5','6','7','8']
>>>>>>> Stashed changes

        self.popupMenu = OptionMenu(
            self.root, self.comPortNum, comPorts[2], *comPorts)
        self.popupMenu.pack()

        # attempt to establish connection
        self.errComs = Label(
            self.root, text='Communication not established. Trying again.', style="BW.TLabel")
        try:
            self.master = commands.connect("COM" + self.comPortNum.get())
            self.errComs.pack_forget()
            self.popupMenu.pack_forget()
            self.arm.pack()
            self.disarm.pack()
        except:
            self.errComs.pack()
            self.popupMenu.pack()
            self.comsEstablished = False
            print("COM" + self.comPortNum.get())

        #----#
        # Styling
        style = Style()
        style.configure("BW.TLabel", foreground="white", background="#2a2b2e")
        #----#
        # Labels to display telemetry
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
        # Arming buttons
        self.arm = Button(self.root, text='Arm',
                          command=lambda: commands.arm(self.master))
        self.disarm = Button(self.root, text='Disarm',
                             command=lambda: commands.disarm(self.master))

    def quitting(self):  # to set the quit flag
        self.quit = True

    def refreshLabels(self, data):
        self.alt.configure(text='Altitude: ' + data["altitude"])
        self.airspd.configure(text='Airspeed: ' + data["airspeed"])
        self.grndspd.configure(text='Groundspeed: ' + data["groundspeed"])
        self.hdg.configure(text='Heading: ' + data["heading"])
        self.latLong.configure(text='Lat + Long: ' +
                               data["latitude"] + ' , ' + data["longitude"])
        self.volt.configure(text='Voltage: ' + data["voltage"])
        self.fltMod.configure(text='Flight Mode: ' + data["flightMode"])
        #altitude, airspeed, groundspeed, heading, lat, long, voltage, flightMode
        self.alt.pack()
        self.airspd.pack()
        self.grndspd.pack()
        self.hdg.pack()
        self.latLong.pack()
        self.volt.pack()
        self.fltMod.pack()

    def run(self):  # main part of the application
        if self.comsEstablished:
            commands.wait_heartbeat(self.master)

        #self.master = commands.connect("COM4")
        # commands.wait_heartbeat(self.master)

        # sets the background to white rather than default gray.
        self.root.configure(bg="#2a2b2e")
        # changes the X (close) Button to run a function instead.
        self.root.protocol("WM_DELETE_WINDOW", self.quitting)
        self.root.title("Visual Telemetry GUI")
        self.root.geometry("800x600")

        #############################################################
        while not self.quit:  # flag to quit the application
            # updates the root. same as root.mainloop() but safer and interruptable
            self.root.update_idletasks()
            # same as above. This lest you stop the loop or add things to the loop.
            self.root.update()

            # checks for established communications
            if self.comsEstablished:
                try:
                    # will refresh labels if communications exist
                    self.refreshLabels(commands.display_data(self.master))
                except:
                    print('Error. Attempting to retry.')
                    self.comsEstablished = False
            else:
                try:  # if there is no connection, it attempts to make one
                    self.master = commands.connect(
                        "COM" + self.comPortNum.get())
                    commands.wait_heartbeat(self.master)
                    self.errComs.pack_forget()
                    self.popupMenu.pack_forget()
                    self.arm.pack()
                    self.disarm.pack()
                    self.errComs.pack_forget()
                    # if there is a connection is established, everything goes back to normal
                    self.comsEstablished = True
                except:  # if an error occurs making the connection, it tries again every .1 second
                    self.errComs.pack()
                    self.popupMenu.pack()
                    self.comsEstablished = False
                    print("COM" + self.comPortNum.get())
                time.sleep(0.5)


if __name__ == "__main__":
    app = SimpleGUI("COM4")  # creates instance of GUI class
    try:
        app.run()  # starts the application
    except KeyboardInterrupt:
        app.quitting()  # safely quits the application when crtl+C is pressed
    except:
        raise  # you can change this to be your own error handler if needed
