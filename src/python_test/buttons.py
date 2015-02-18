# Basic skeleton, playing with buttons
# Code written for Python 3.4, using TkInter

import tkinter as tk
import time

N = tk.N
S = tk.S
E = tk.E
W = tk.W

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
        self.startFrame = tk.Frame(self, bg="green")
        self.startFrame.grid(row=0, column=0, sticky=(N, S, E, W))
        self.startFrame.startButton = tk.Button(self.startFrame, text="Connect to panel", command=self.connectRemote)
        self.startFrame.startButton.grid(row=0, column=0, sticky=(N, S, E, W))

        self.statusLabelText = tk.StringVar()
        self.statusLabelText.set("SolarRemote program started")
        self.statusLabel = tk.Label(self, textvariable=self.statusLabelText)
        self.statusLabel.grid(row=1, column=0, sticky=S)

    def connectRemote(self):
        self.statusLabelText.set("Connecting...")
        self.launchControlFrame()

    def launchControlFrame(self):
        #time.sleep(2)
        self.startFrame.grid_forget()
        self.startFrame.destroy()
        self.controlFrame = ControlFrame(self)
        self.statusLabelText.set("Connected")
        #self.statusLabel.grid(row=4, column=0)


class ControlFrame(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg="red")
        self.grid(row=0, column=0, sticky=(N, S, E, W))
        self.setupControls()

    def setupControls(self):
        tk.Button(self, text="UP", width=5, height=3).grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        tk.Button(self, text="LEFT", width=5, height=3).grid(row=1, column=0, pady=5, padx=5, sticky=tk.EW)
        tk.Button(self, text="STOP", width=5, height=3).grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        tk.Button(self, text="RIGHT", width=5, height=3).grid(row=1, column=2, pady=10, padx=5, sticky=tk.EW)
        tk.Button(self, text="DOWN", width=5, height=3).grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)

        tk.Button(self, text="DATE", bg="grey", fg="white").grid(row=3, column=0, pady=20)
        tk.Button(self, text="LOC", bg="grey", fg="white").grid(row=3, column=1)
        tk.Button(self, text="SET LOC", bg="grey", fg="white").grid(row=3, column=2)


root = tk.Tk()
root.geometry("240x320")
remoteApp = SolarRemote(root)

root.mainloop()
