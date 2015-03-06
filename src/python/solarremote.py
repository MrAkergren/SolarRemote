#! /usr/bin/python3
# -*- coding: UTF-8 -*-

# Solar Remote prototype code
# Group members:    Johan Strand
#                   Pär Svedberg
#                   Oskar Åkergren
# Written for the project course DAT065 in Chalmers University of Technology
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
        tk.Frame.__init__(self, self.tkRoot)
        self.tkRoot.rowconfigure(0, weight=1)
        self.tkRoot.columnconfigure(0, weight=1)
        self.grid(sticky=(N, S, E, W))
        self.rowconfigure(0, weight=100)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Initiate frames and start the first frame, the steering controls
        self.commandFrame = CommandFrame(self)
        self.controlFrame = ControlFrame(self)
        self.controlFrame.showFrame()
        
        self.statusLabelText = tk.StringVar()
        self.statusLabelText.set('Welcome to SolarRemote\nApplication started')
        self.statusLabel = tk.Label(self, textvariable=self.statusLabelText, height=2)
        self.statusLabel.grid(row=1, column=0, sticky=(E, W))

        # Used finding 'junk strings' returned from the panel: isJunkString()
        self.ignoreStrings = ['run', 'restart', 'date', 'setup', '#', 'Usage', 'lon', 'lat']

        # Used when checking delay in serial read: readSerial()
        self.steeringStrings = ['up', 'down', 'left', 'right']

        self.connection = None

    # Switch the visible frame in the GUI
    def switchFrame(self, command):
        if command == 'launchControl':
            self.commandFrame.grid_forget()
            self.controlFrame.showFrame()
        if command == 'launchCommand':
            self.controlFrame.grid_forget()
            self.commandFrame.showFrame()

    # Create serial connection
    def serialConnect(self):
        if self.connection is not None:
            self.connection.close()
        self.connection = serial.Serial('/dev/ttyUSB0', 38400, timeout = 1)
        time.sleep(1)

    # To be used to establish serial connection
    def connectRemote(self):
        self.statusLabelText.set('Connecting...')
        if debug:
            self.controlFrame.bindButtons()
            self.commandFrame.bindButtons()
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
                    self.connection.flushInput()
                    self.connection.flushOutput()
                    self.runCommand('\r\n')
                    self.controlFrame.bindButtons()
                    self.commandFrame.bindButtons()
                    self.statusLabelText.set('Connection established')
                else:
                    self.statusLabelText.set('Serial connection is not open')

    # Sends a given command over serial connection
    def runCommand(self, command):
        self.lastcmd = command
        if debug:
            print(command)
        else:
            command += '\r'

            try:
                if self.connection.write(command.encode('utf-8')) > 0:
                    if 'lon' not in self.lastcmd and 'lat' not in self.lastcmd:
                        self.readAndPrintSerial()
                else:
                    self.statusLabelText.set('Serial write failed')
                    print('Serial write failed')
            except serial.SerialTimeoutException:
                self.statusLabelText.set('Timeout on serial write')
                print('Timeout on serial write')
            except serial.SerialException:
                self.statusLabelText.set('Serial communication failed')
                print('Serial communication failed')

    # Reads information from the serial connection
    def readAndPrintSerial(self):
        self.serialDelay()
        while self.connection.inWaiting() > 0:
            newText = self.readSerial()
            if newText:
                self.updateStatusbar(self.indata)

    # Performs a delay appropriate to the last command sent to the panel,
    # in order to synchronize the serial read
    def serialDelay(self):
        if self.lastcmd.startswith('run') and 'stop' not in self.lastcmd:
            time.sleep(.001)
            print('Steering string!')
        elif self.lastcmd.startswith('lon') or self.lastcmd.startswith('lat'):
            time.sleep(.03)
        else:
            time.sleep(.015)

    # Reads a line/string from serial input. If the string contains date info,
    # insert newline character to the string
    # Returns true if a new (useful) line is read
    # Returns false if the string is considered 'junk' info the panel
    def readSerial(self):
        self.indata = self.connection.readline()
        self.indata = self.indata.decode(encoding='utf-8')
        self.indata = self.indata.rstrip('\r\n')
        if self.isJunkString(self.indata):
            return False
        if self.lastcmd == 'date' and 'Current date' in self.indata:
            self.indata = self.indata.replace(': ', ':\n')
        return True

    # Updates the status bar in the GUI
    def updateStatusbar(self, text):
        self.statusLabelText.set(text)
        print('Serial read:', text)

    # Gets information about the panels location in longitude and latitude,
    # which is then shown in the GUI's status bar
    def getLocation(self):
        if debug:
            print('lon\nlat')
        else:
            self.runCommand('lon')
            self.runCommand('lat')
            self.serialDelay()
            positions = []
            while self.connection.inWaiting() > 0:
                newText = self.readSerial()
                if newText and self.indata.startswith('Current l'):
                    positions.append(self.indata)
            self.updateStatusbar('\n'.join(positions))

    # Checks if a string is considered 'junk'. This is used to for checking
    # strings returned from the panel, and this function filters out strings
    # that are not supposed to be viewed in the GUI's status bar.
    # Here 'junk' is defines as empty strings, echoes of commands etc,
    # as defined in the ignoreStrings list.
    def isJunkString(self, inputString):
        ignoreString = False
        for cmdString in self.ignoreStrings:
            if inputString.startswith(cmdString):
                ignoreString = True
        if ignoreString or len(inputString) == 0 or inputString.isspace():
            return True
        else:
            return False

# The control frame containing buttons to send commands to the panel        
class ControlFrame(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        self.master = master
        tk.Frame.__init__(self, self.master, bg='black')
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
class CommandFrame(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        self.master = master
        tk.Frame.__init__(self, self.master, bg='black')
        self.setupButtons()

    # Adds the frame to its master
    def showFrame(self):
        self.grid(row=0, column=0, sticky=(N, S, E, W))

    # Create command buttons
    def setupButtons(self):
        self.btnDate = tk.Button(self, text='DATE', width=5, height=3)
        self.btnDate.grid(row=1, column=0, pady=5, padx=5, sticky=(E, W))

        self.btnLoc = tk.Button(self, text='LOC', width=5, height=3)
        self.btnLoc.grid(row=1, column=1, pady=5, padx=5, sticky=(E, W))

        self.btnStopcmd = tk.Button(self, text='STOP', width=5, height=3)
        self.btnStopcmd.grid(row=1, column=2, pady=5, padx=5, sticky=(E, W))

        self.btnRestart = tk.Button(self, text='RESTART', width=5, height=3)
        self.btnRestart.grid(row=2, column=0, pady=5, padx=5, sticky=(E, W))
        
        self.btnSetup = tk.Button(self, text='SETUP', width=5, height=3)
        self.btnSetup.grid(row=2, column=1, pady=5, padx=5, sticky=(E, W))

        self.btnAuto = tk.Button(self, text='AUTO', width=5, height=3)
        self.btnAuto.grid(row=2, column=2, pady=5, padx=5, sticky=(E, W))

        self.btnBack = tk.Button(self, text='BACK TO\nCONTROL', height=3, \
            width=5, command=lambda:self.master.switchFrame('launchControl'))
        self.btnBack.grid(row=3, column=1, pady=40, padx=5, sticky=(E, W))        

    # Enable button bindings
    def bindButtons(self):
        self.btnDate.configure(command=lambda:self.master.runCommand('date'))
        self.btnRestart.configure(command=lambda:self.master.runCommand('restart'))
        self.btnSetup.configure(command=lambda:self.master.runCommand('setup'))
        self.btnAuto.configure(command=lambda:self.master.runCommand('run auto'))
        self.btnLoc.configure(command=self.master.getLocation)
        self.btnStopcmd.bind('<Button-1>', lambda x:self.master.runCommand('run stop'))

    # Disable button bindings
    def unbindButtons(self):
        self.btnDate.configure(command='')
        self.btnRestart.configure(command='')
        self.btnSetup.configure(command='')
        self.btnAuto.configure(command='')
        self.btnLoc.configure(command='')
        self.btnStopcmd.unbind('<Button-1>')

root = tk.Tk()
root.geometry('240x320')
root.wm_title('Solar Panel Remote')
remoteApp = SolarRemote(root)

root.mainloop()
