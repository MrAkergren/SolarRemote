# Basic skeleton, playing with buttons
# Code written for Python 3.4, using TkInter

from tkinter import *

root = Tk()

w = Button(root, text="UP", bg="green", fg="white")
w.grid(row=0, column=2, pady=10, padx=10, sticky=EW)
w = Button(root, text="LEFT", bg="green", fg="white")
w.grid(row=1, column=0, pady=10, padx=10, sticky=EW)
w = Button(root, text="STOP", bg="red", fg="black")
w.grid(row=1, column=2, pady=10, padx=10, sticky=EW)
w = Button(root, text="RIGHT", bg="green", fg="white")
w.grid(row=1, column=4, pady=10, padx=10, sticky=EW)
w = Button(root, text="DOWN", bg="green", fg="white")
w.grid(row=2, column=2, pady=10, padx=10, sticky=EW)

w = Button(root, text="DATE", bg="blue", fg="white")
w.grid(row=3, column=0, pady=20)
w = Button(root, text="LOC", bg="blue", fg="white")
w.grid(row=3, column=4)

mainloop()
