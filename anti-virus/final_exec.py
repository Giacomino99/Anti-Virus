# execute from malfile
import sys
import os

from decimal import Decimal, InvalidOperation
from datetime import datetime

import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox


class WarnGUI():
    def __init__(self, option, filenames):
        # define basic window
        self._window = tk.Tk()
        self._window.title("MB Defender")
        # establishing other GUI frames
        # frame for the buttons
        self._text_frame = tk.Frame(self._window)
        self._text_frame.grid(row=0, column=0, columnspan=4, sticky=N)

        # popup
        tk.messagebox.showwarning("WARNING", "During our scan, we found the following files might be malicious.")
        #  text frame and label
        self._text_frame = tk.Frame(self._window)
        self._text_frame.grid(row=1, column=0, columnspan=4, sticky=NW)
        tk.Label(self._text_frame, text = "All the files below have been flagged for either a suspicious hash or binary signature.").grid(row=1, column=0)
        # active frame with variable use
        self._active_frame = tk.Frame(self._window)
        self._active_frame.grid(row=2, column=0, columnspan=8, sticky=N)
        # open file, gather all filenames
        filepath = 'malfile.txt'
        filenames = []
        fp = open(filepath, 'r')
        filenames = fp.read().split('\n')
        # create listbox
        langs_var = tk.StringVar(value=filenames)
        listbox = tk.Listbox(self._active_frame, listvariable=langs_var, height=10,width=60, selectmode='extended')
        listbox.grid(column=0, row=4, sticky='n')

        scrollbar = tk.Scrollbar(
            self._active_frame,
            orient='vertical',
            command=listbox.yview
            )
        listbox['yscrollcommand'] = scrollbar.set

        scrollbar.grid(
            column=2,
            row=4,
            sticky='w')
        if option == 0:
            tk.Label(self._text_frame, text = "Current Setting: Warn Only (Files have not been altered.)").grid(row=5, column=0)
        elif option == 1:
            tk.Label(self._text_frame, text = "Current Setting: Isolate (Files have been relocated to quarantined directory.)").grid(row=5, column=0)
        elif option == 2: 
            tk.Label(self._text_frame, text = "Current Setting: Remove (Files have been removed.)").grid(row=5, column=0)
        else:
            tk.Label(self._text_frame, text = "Option setting invalid...").grid(row=5, column=0)
        self._window.mainloop()

if __name__ == "__main__":
    # get countermeasures
    with open("counter_config.txt") as f:
        firstline = f.readline().rstrip()
    
    option = int(firstline)
    # get malfile in list
    filepath = 'malfile.txt'
    filenames = []
    if os.stat(filepath).st_size == 0:
        exit()
    fp = open(filepath, 'r')
    filenames = fp.read().split('\n')
    fp.close()

    # if argv[2] = 0, 1, 2...
    if option == 0:
        # just warn
        pass
    elif option == 1:
        #  isolate files
        for item in filenames:
            os.system("mv {} ./quarantine/".format(item))
    elif option == 2:
        #  delete files
        for item in filenames:
            os.system("rm {}".format(item))
    else:
        # default to warning
        option = 0
        pass
        
    popup = WarnGUI(option, filenames)
