# Basic skeleton, playing with buttons
# Code written for Python 3.4, using TkInter

import tkinter as tk

N = tk.N
S = tk.S
E = tk.E
W = tk.W

# Main application frame
class SolarRemote(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        # Frames are color coded for debugging 
        tk.Frame.__init__(self, master, bg="blue")
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.grid(sticky=(N, S, E, W))
        self.rowconfigure(0, weight=100)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.startFrame = StartFrame(self)
        
        self.statusLabelText = tk.StringVar()
        self.statusLabelText.set("SolarRemote started")
        self.statusLabel = tk.Label(self, textvariable=self.statusLabelText)
        self.statusLabel.grid(row=1, column=0, sticky=(E, W))

    # To be used to establish serial connection
    def connectRemote(self):
        self.statusLabelText.set("Connecting...")
        self.launchControlFrame()

    # When serial connection is established, launch the ControlFrame
    def launchControlFrame(self):
        self.startFrame.grid_forget()
        self.startFrame.destroy()
        self.controlFrame = ControlFrame(self)
        self.statusLabelText.set("Connected")

class StartFrame(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        self.parent = master
        tk.Frame.__init__(self, master, bg="green")
        self.grid(row=0, column=0, sticky=(N, S, E, W))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.startButton = tk.Button(self, text="Connect to panel", \
            command=master.connectRemote)
        self.startButton.grid(row=0, column=0, sticky=(N, S, E, W))

# The control frame containing buttons to send commands to the panel        
class ControlFrame(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg="red")
        self.grid(row=0, column=0, sticky=(N, S, E, W))
        self.setupControls()

    # Setup of control buttons
    def setupControls(self):
        # Lambda function to use for 'run stop' on button release
        stopCommand = lambda x:self.runCommand("run stop")

        self.btnUp = tk.Button(self, text="UP", width=5, height=3)
        self.btnUp.grid(row=0, column=1, pady=5, padx=5, sticky=(E, W))
        self.btnUp.bind("<Button-1>", lambda x:self.runCommand("run u"))
        self.btnUp.bind("<ButtonRelease-1>", stopCommand)

        self.btnLeft = tk.Button(self, text="LEFT", width=5, height=3)
        self.btnLeft.grid(row=1, column=0, pady=5, padx=5, sticky=(E, W))
        self.btnLeft.bind("<Button-1>", lambda x:self.runCommand("run l"))
        self.btnLeft.bind("<ButtonRelease-1>", stopCommand)

        self.btnStop = tk.Button(self, text="STOP", width=5, height=3)
        self.btnStop.grid(row=1, column=1, pady=5, padx=5, sticky=(E, W))
        self.btnStop.bind("<Button-1>", stopCommand)

        self.btnRight = tk.Button(self, text="RIGHT", width=5, height=3)
        self.btnRight.grid(row=1, column=2, pady=10, padx=5, sticky=(E, W))
        self.btnRight.bind("<Button-1>", lambda x:self.runCommand("run r"))
        self.btnRight.bind("<ButtonRelease-1>", stopCommand)

        self.btnDown = tk.Button(self, text="DOWN", width=5, height=3)
        self.btnDown.grid(row=2, column=1, pady=5, padx=5, sticky=(E, W))
        self.btnDown.bind("<Button-1>", lambda x:self.runCommand("run d"))
        self.btnDown.bind("<ButtonRelease-1>", stopCommand)

        self.btnDate = tk.Button(self, text="DATE", bg="grey", fg="white", \
            command=lambda:self.runCommand("date"))
        self.btnDate.grid(row=3, column=0, pady=10, sticky=(E, W))

        self.btnLoc = tk.Button(self, text="LOC", bg="grey", fg="white")
        self.btnLoc.grid(row=3, column=1, sticky=(E, W))

        self.btnSetLoc = tk.Button(self, text="SET LOC", bg="grey", fg="white")
        self.btnSetLoc.grid(row=3, column=2, sticky=(E, W))

        self.btnRestart = tk.Button(self, text="RESTART", bg="grey", \
            fg="white", command=lambda:self.runCommand("restart"))
        self.btnRestart.grid(row=4, column=0, sticky=(E, W))
        
        self.btnSetup = tk.Button(self, text="SETUP", bg="grey", fg="white", \
            command=lambda:self.runCommand("setup"))
        self.btnSetup.grid(row=4, column=1, sticky=(E, W))

        self.btnAuto = tk.Button(self, text="AUTO", bg="grey", fg="white", \
            command=lambda:self.runCommand("run auto"))
        self.btnAuto.grid(row=4, column=2, sticky=(E, W))

    def runCommand(self, command):
        print(command)


root = tk.Tk()
root.geometry("240x320")
remoteApp = SolarRemote(root)

root.mainloop()
