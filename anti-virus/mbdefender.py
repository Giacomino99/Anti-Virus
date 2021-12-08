import sys
import os

from decimal import Decimal, InvalidOperation
from datetime import datetime

import tkinter as tk
from tkinter import *
from tkcalendar import Calendar
from tkinter import messagebox



class MenuGUI():
    def __init__(self):
        # countermeasure param
        self._countermeasure = 0  # 0 = warning, 1 = isolate, 2 = remove
        # define basic window
        self._window = tk.Tk()
        self._window.title("MB Defender")
        # establishing other GUI frames
        # frame for the buttons
        self._options_frame = tk.Frame(self._window)
        self._options_frame.grid(row=0, column=0, columnspan=4, sticky=NW)
        
        # buttons
        tk.Button(self._options_frame,
                text = "Manage Allowlist",
                command = self._allowlist).grid(row=0, column=1, sticky=W)
        tk.Button(self._options_frame,
                text = "Manage Target Signatures",
                ).grid(row=0, column=2,sticky=W)
        tk.Button(self._options_frame,
                text = "Configure Countermeasures",
                ).grid(row=0, column=3,sticky=W)
        tk.Button(self._options_frame,
                text = "Launch Scan",highlightbackground='green'
                ).grid(row=0, column=0)
        #  text frame and label
        self._text_frame = tk.Frame(self._window)
        self._text_frame.grid(row=1, column=0, columnspan=4, sticky=NW)
        tk.Label(self._text_frame, text = "Welcome to MB Defender! Please select an option above.").grid(row=1, column=0)
        # active frame with variable use
        self._active_frame = tk.Frame(self._window)
        self._active_frame.grid(row=2, column=0, columnspan=8, sticky=W)
        self._window.mainloop()


    def _allowlist(self):
        def add_file():
            # add filename to allowlist
            newstring = "\n" + subbox.get()
            file1 = open("file_allow", "a")
            file1.write(newstring)
            file1.close()
            # clear frames by restarting allowlist display
            self._allowlist()
        
        def add_filelist():
            if not os.path.isfile(subbox2.get()):
                tk.messagebox.showinfo("MB DEFENDER",  "Submitted file does not exist, try again.")
                self._allowlist()
            else:
                # else file does exist
                f1 = open("file_allow", 'a+')
                f2 = open(subbox2.get(), 'r')
                f1.write("\n" + f2.read())
                f1.close()
                f2.close()
                self._allowlist()
        
        def delete_file():
            with open("file_allow", "r") as f:
                lines = f.readlines()
            with open("file_allow", "w") as f:
                for line in lines:
                    if line.strip("\n") != subbox3.get():
                        f.write(line)
            self._allowlist()
            
            
            
        # function to add a file
        # delete old widgets in text frame and active frame
        for widget in self._text_frame.winfo_children():
            widget.destroy()
        for widget in self._active_frame.winfo_children():
            widget.destroy()
        
        # update text frame
        tk.Label(self._text_frame, text = "Manage the allowlist below. Add a new file/directory path or remove an existing one.").grid(row=1, column=0)
        # update active frame:
        sub_label = tk.Label(self._active_frame, text = "Add file or directory name:")
        sub_label.grid(row = 1, column = 0)
        subbox = tk.Entry(self._active_frame)
        subbox.grid(row = 1, column = 1)
        submitbutton = tk.Button(self._active_frame, text = "Submit Filename",highlightbackground='green', command=add_file)
        submitbutton.grid(row = 1, column = 2)

        # field for list of files instead
        sub_label2 = tk.Label(self._active_frame, text = "Add text file containing list of file/directory names:")
        sub_label2.grid(row = 2, column = 0)
        subbox2 = tk.Entry(self._active_frame)
        subbox2.grid(row = 2, column = 1)
        submitbutton2 = tk.Button(self._active_frame, text = "Submit Filename",highlightbackground='green', command=add_filelist)
        submitbutton2.grid(row = 2, column = 2)

        # field for file to delete:
        sub_label3 = tk.Label(self._active_frame, text = "Name of file to remove:")
        sub_label3.grid(row = 5, column = 0)
        subbox3 = tk.Entry(self._active_frame)
        subbox3.grid(row = 5, column = 1)
        submitbutton3 = tk.Button(self._active_frame, text = "Submit Filename",highlightbackground='green', command=delete_file)
        submitbutton3.grid(row = 5, column = 2)

        # add list of files to active frame
        # open file, gather all filenames
        filepath = 'file_allow'
        filenames = []
        fp = open(filepath, 'r')
        filenames = fp.read().split('\n')
        # create listbox
        langs_var = tk.StringVar(value=filenames)
        box_label = tk.Label(self._active_frame, text = "Current Allowlist:")
        box_label.grid(row = 3, column = 0)
        listbox = tk.Listbox(self._active_frame, listvariable=langs_var, height=6, selectmode='extended')
        listbox.grid(column=1, row=4, sticky='e')

        scrollbar = tk.Scrollbar(
            self._active_frame,
            orient='vertical',
            command=listbox.yview
            )
        listbox['yscrollcommand'] = scrollbar.set

        scrollbar.grid(
            column=1,
            row=4,
            sticky='nw')




if __name__ == "__main__":
    # try:
    
        a = MenuGUI()
