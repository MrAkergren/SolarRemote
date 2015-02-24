#! /usr/bin/python3
# Basic skeleton, playing with buttons
# Code written for Python 3, using TkInter

import sys
import tkinter as tk
import serial
import time

# For ease of use and readability
N = tk.N
S = tk.S
E = tk.E
W = tk.W

debug = False
for arg in sys.argv:
    if arg == 'd':
        debug = True

# Main application frame
class SolarRemote(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        # Frames are color coded for debugging 
        self.tkRoot = master
        tk.Frame.__init__(self, self.tkRoot, bg='blue')
        self.tkRoot.rowconfigure(0, weight=1)
        self.tkRoot.columnconfigure(0, weight=1)
        self.grid(sticky=(N, S, E, W))
        self.rowconfigure(0, weight=100)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Initiate frames and start the first frame, the steering controls
        self.commandFrame = ButtonFrame(self)
        self.controlFrame = ControlFrame(self)
        self.controlFrame.showFrame()
        
        self.statusLabelText = tk.StringVar()
        self.statusLabelText.set('Welcome to SolarRemote\nApplication started')
        self.statusLabel = tk.Label(self, textvariable=self.statusLabelText, height=2)
        self.statusLabel.grid(row=1, column=0, sticky=(E, W))

    def switchFrame(self, command):
        if command == 'launchControl':
            self.commandFrame.grid_forget()
            self.controlFrame.showFrame()
        if command == 'launchCommand':
            self.controlFrame.grid_forget()
            self.commandFrame.showFrame()

    def serialConnect(self):
        self.connection = serial.Serial('/dev/ttyUSB0', 38400, timeout = 1)
        time.sleep(1)

    # To be used to establish serial connection
    def connectRemote(self):
        self.statusLabelText.set('Connecting...')
        if debug:
            self.controlFrame.bindButtons()
            self.statusLabelText.set('Debug mode')
            print('Debug mode')
        else:
            try:
                self.serialConnect()
            except serial.SerialException:
                self.statusLabelText.set('Connection failed')
                print('Connection failed')
            else:
                if self.connection.isOpen():            
                    self.controlFrame.bindButtons()
                    self.statusLabelText.set('Connection established')
                else:
                    self.statusLabelText.set('Serial connection is not open')

    # Sends a given command over serial connection
    def runCommand(self, command):
        if debug:
            print(command)
        else:
            command += '\r'

            try:
                if self.connection.write(command.encode('utf-8')) > 0:
                    self.readAndPrintSerial()
                else:
                    self.statusLabelText.set('Serial write failed')
                    print('Serial write failed')
            except serial.SerialTimeoutException:
                self.statusLabelText.set('Timeout on serial write')
                print('Timeout on serial write')

    # Reads information from the serial connection
    def readAndPrintSerial(self):
       # while self.connection.inWaiting() > 0:
            self.inData = self.connection.readline()
            self.inData = self.inData.decode(encoding='utf-8')
            self.inData = self.inData.rstrip('\r\n')
            self.statusLabelText.set(self.inData)
            print('Serial read:', self.inData)
            time.sleep(.200)

# The control frame containing buttons to send commands to the panel        
class ControlFrame(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        self.master = master
        tk.Frame.__init__(self, self.master, bg='red')
        
        self.setupControlButtons()

    # Adds the frame to its master
    def showFrame(self):
        self.grid(row=0, column=0, sticky=(N, S, E, W))

    # Setup of control buttons
    def setupControlButtons(self):
        self.btnUp = tk.Button(self, text='UP', width=5, height=3)
        self.btnUp.grid(row=0, column=1, pady=5, padx=5, sticky=(E, W))

        self.btnLeft = tk.Button(self, text='LEFT', width=5, height=3)
        self.btnLeft.grid(row=1, column=0, pady=5, padx=5, sticky=(E, W))
        
        self.btnStop = tk.Button(self, text='STOP', width=5, height=3)
        self.btnStop.grid(row=1, column=1, pady=5, padx=5, sticky=(E, W))
        
        self.btnRight = tk.Button(self, text='RIGHT', width=5, height=3)
        self.btnRight.grid(row=1, column=2, pady=10, padx=5, sticky=(E, W))
        
        self.btnDown = tk.Button(self, text='DOWN', width=5, height=3)
        self.btnDown.grid(row=2, column=1, pady=5, padx=5, sticky=(E, W))

        self.btnCon = tk.Button(self, text='CONNECT', width=5, \
            command=self.master.connectRemote)
        self.btnCon.grid(row=3, column=0, pady=30, padx=5, sticky=(E, W))

        self.btnCommands = tk.Button(self, text='COMMAND', width=5, \
            command=lambda:self.master.switchFrame('launchCommand'))
        self.btnCommands.grid(row=3, column=2, pady=30, padx=5, sticky=(E, W))

    # Bind the control buttons to commands
    def bindButtons(self):
        # Lambda function to use for 'run stop' on button release
        stopCommand = lambda x:self.master.runCommand('run stop')

        self.btnUp.bind('<Button-1>', lambda x:self.master.runCommand('run u'))
        self.btnUp.bind('<ButtonRelease-1>', stopCommand)
        self.btnLeft.bind('<Button-1>', lambda x:self.master.runCommand('run l'))
        self.btnLeft.bind('<ButtonRelease-1>', stopCommand)
        self.btnStop.bind('<Button-1>', stopCommand)
        self.btnRight.bind('<Button-1>', lambda x:self.master.runCommand('run r'))
        self.btnRight.bind('<ButtonRelease-1>', stopCommand)
        self.btnDown.bind('<Button-1>', lambda x:self.master.runCommand('run d'))
        self.btnDown.bind('<ButtonRelease-1>', stopCommand)

    # Unbind the commands from the control buttons
    def unbindButtons(self):
        self.btnUp.unbind('<Button-1>')
        self.btnUp.unbind('<ButtonRelease-1>')
        self.btnLeft.unbind('<Button-1>')
        self.btnLeft.unbind('<ButtonRelease-1>')
        self.btnStop.unbind('<Button-1>')
        self.btnRight.unbind('<Button-1>')
        self.btnRight.unbind('<ButtonRelease-1>')
        self.btnDown.unbind('<Button-1>')
        self.btnDown.unbind('<ButtonRelease-1>')

# Frame containing the command buttons (non-steering)
class ButtonFrame(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        self.master = master
        tk.Frame.__init__(self, self.master, bg='yellow')
        self.setupButtons()
        self.bindButtons()

    # Adds the frame to its master
    def showFrame(self):
        self.grid(row=0, column=0, sticky=(N, S, E, W))

    # Create command buttons
    def setupButtons(self):
        self.btnDate = tk.Button(self, text='DATE', height=3, width=5)
        self.btnDate.grid(row=1, column=0, pady=5, padx=5, sticky=(E, W))

        self.btnLoc = tk.Button(self, text='LOC', height=3, width=5)
        self.btnLoc.grid(row=1, column=1, pady=5, padx=5, sticky=(E, W))

        self.btnSetLoc = tk.Button(self, text='SET LOC', height=3, width=5)
        self.btnSetLoc.grid(row=1, column=2, pady=5, padx=5, sticky=(E, W))

        self.btnRestart = tk.Button(self, text='RESTART', height=3, width=5)
        self.btnRestart.grid(row=2, column=0, pady=5, padx=5, sticky=(E, W))
        
        self.btnSetup = tk.Button(self, text='SETUP', height=3, width=5)
        self.btnSetup.grid(row=2, column=1, pady=5, padx=5, sticky=(E, W))

        self.btnAuto = tk.Button(self, text='AUTO', height=3, width=5)
        self.btnAuto.grid(row=2, column=2, pady=5, padx=5, sticky=(E, W))

        self.btnBack = tk.Button(self, text='BACK TO\nCONTROL', height=3, \
            width=5, command=lambda:self.master.switchFrame('launchControl'))
        self.btnBack.grid(row=3, column=1, pady=40, padx=5, sticky=(E, W))        

    # Enable button bindings
    def bindButtons(self):
        if debug or self.master.connection.isOpen():
            self.btnDate.configure(command=lambda:self.master.runCommand('date'))
            self.btnRestart.configure(command=lambda:self.master.runCommand('restart'))
            self.btnSetup.configure(command=lambda:self.master.runCommand('setup'))
            self.btnAuto.configure(command=lambda:self.master.runCommand('run auto'))

    # Disable button bindings
    def unbindButtons(self):
        self.btnDate.configure(command=lambda:self.master.runCommand(''))
        self.btnRestart.configure(command=lambda:self.master.runCommand(''))
        self.btnSetup.configure(command=lambda:self.master.runCommand(''))
        self.btnAuto.configure(command=lambda:self.master.runCommand(''))

root = tk.Tk()
root.geometry('240x320')
remoteApp = SolarRemote(root)

root.mainloop()
