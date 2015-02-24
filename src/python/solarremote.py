#! /usr/bin/python3
# Basic skeleton, playing with buttons
# Code written for Python 3, using TkInter

import sys
import tkinter as tk
import serial
import time


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
        self.startFrame = StartFrame(self)
        
        self.statusLabelText = tk.StringVar()
        self.statusLabelText.set('SolarRemote started')
        self.statusLabel = tk.Label(self, textvariable=self.statusLabelText)
        self.statusLabel.grid(row=1, column=0, sticky=(E, W))

    def serialConnect(self):
        self.connection = serial.Serial('/dev/ttyUSB0', 38400, timeout = 1)
        time.sleep(1)

    # To be used to establish serial connection
    def connectRemote(self):
        self.statusLabelText.set('Connecting...')
        if debug:
            self.launchControlFrame()
        else:
            try:
                self.serialConnect()
            except serial.SerialException:
                self.statusLabelText.set('Connection failed')
                print('Connection failed')
            else:
                if self.connection.isOpen():            
                    self.launchControlFrame()
                else:
                    self.statusLabelText.set('Serial connection is not open')

    # When serial connection is established, launch the ControlFrame
    def launchControlFrame(self):
        self.startFrame.grid_forget()
        self.startFrame.destroy()
        self.controlFrame = ControlFrame(self)
        self.statusLabelText.set('Connected')

class StartFrame(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        self.parent = master
        tk.Frame.__init__(self, self.parent, bg='green')
        self.grid(row=0, column=0, sticky=(N, S, E, W))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.startButton = tk.Button(self, text='Connect to panel', \
            command=self.parent.connectRemote)
        self.startButton.grid(row=0, column=0, sticky=(N, S, E, W))

# The control frame containing buttons to send commands to the panel        
class ControlFrame(tk.Frame):
    # Constructor
    def __init__(self, master=None):
        self.parent = master
        tk.Frame.__init__(self, self.parent, bg='red')
        self.grid(row=0, column=0, sticky=(N, S, E, W))
        self.setupControlButtons()

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
        
        self.btnDate = tk.Button(self, text='DATE', bg='grey', fg='white')
        self.btnDate.grid(row=3, column=0, pady=10, sticky=(E, W))

        self.btnLoc = tk.Button(self, text='LOC', bg='grey', fg='white', command=self.unbindButtons)
        self.btnLoc.grid(row=3, column=1, sticky=(E, W))

        self.btnSetLoc = tk.Button(self, text='SET LOC', bg='grey', fg='white', command=self.bindButtons)
        self.btnSetLoc.grid(row=3, column=2, sticky=(E, W))

        self.btnRestart = tk.Button(self, text='RESTART', bg='grey', \
            fg='white')
        self.btnRestart.grid(row=4, column=0, sticky=(E, W))
        
        self.btnSetup = tk.Button(self, text='SETUP', bg='grey', fg='white')
        self.btnSetup.grid(row=4, column=1, sticky=(E, W))

        self.btnAuto = tk.Button(self, text='AUTO', bg='grey', fg='white')
        self.btnAuto.grid(row=4, column=2, sticky=(E, W))

    # Bind the buttons to commands
    def bindButtons(self):
        # Lambda function to use for 'run stop' on button release
        stopCommand = lambda x:self.runCommand('run stop')

        self.btnUp.bind('<Button-1>', lambda x:self.runCommand('run u'))
        self.btnUp.bind('<ButtonRelease-1>', stopCommand)
        self.btnLeft.bind('<Button-1>', lambda x:self.runCommand('run l'))
        self.btnLeft.bind('<ButtonRelease-1>', stopCommand)
        self.btnStop.bind('<Button-1>', stopCommand)
        self.btnRight.bind('<Button-1>', lambda x:self.runCommand('run r'))
        self.btnRight.bind('<ButtonRelease-1>', stopCommand)
        self.btnDown.bind('<Button-1>', lambda x:self.runCommand('run d'))
        self.btnDown.bind('<ButtonRelease-1>', stopCommand)

        self.btnDate.configure(command=lambda:self.runCommand('date'))
        self.btnRestart.configure(command=lambda:self.runCommand('restart'))
        self.btnSetup.configure(command=lambda:self.runCommand('setup'))
        self.btnAuto.configure(command=lambda:self.runCommand('run auto'))

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

        self.btnDate.configure(command=lambda:self.runCommand(''))
        self.btnRestart.configure(command=lambda:self.runCommand(''))
        self.btnSetup.configure(command=lambda:self.runCommand(''))
        self.btnAuto.configure(command=lambda:self.runCommand(''))


    def runCommand(self, command):
        if debug:
            print(command)
        else:
            command += '\r'

            try:
                if self.parent.connection.write(command.encode('utf-8')) > 0:
                    self.readAndPrintSerial()
                else:
                    self.parent.statusLabelText.set('Serial write failed')
                    print('Serial write failed')
            except serial.SerialTimeoutException:
                self.parent.statusLabelText.set('Timeout on serial write')
                print('Timeout on serial write')

    def readAndPrintSerial(self):
       # while self.parent.connection.inWaiting() > 0:
            self.inData = self.parent.connection.readline()
            self.inData = self.inData.decode(encoding='utf-8')
            self.inData = self.inData.rstrip('\r\n')
            self.self.parent.statusLabelText.set(self.inData)
            print('Serial read:', self.inData)
            time.sleep(.200)


root = tk.Tk()
root.geometry('240x320')
remoteApp = SolarRemote(root)

root.mainloop()
