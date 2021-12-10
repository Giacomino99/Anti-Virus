import sys
import os

from decimal import Decimal, InvalidOperation
from datetime import datetime

from crontab import CronTab

import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
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
        self._options_frame.grid(row=0, column=0, columnspan=5, sticky=N)
        
        # buttons
        tk.Button(self._options_frame,
                text = "Manage Allowlist",
                command = self._allowlist).grid(row=0, column=2, sticky=W)
        tk.Button(self._options_frame,
                text = "Manage Target Signatures",
                command = self._targets).grid(row=0, column=3,sticky=W)
        tk.Button(self._options_frame,
                text = "Change Countermeasures",
                command = self._countermeasures).grid(row=0, column=4)
        tk.Button(self._options_frame,
                text = "Manage scanlist",
                command = self._scanlist).grid(row=0, column=1)
        tk.Button(self._options_frame,
                text = "Schedule Scan",highlightbackground='green',
                command = self._scan).grid(row=0, column=0)

                
        #  text frame and label
        self._text_frame = tk.Frame(self._window)
        self._text_frame.grid(row=1, column=0, columnspan=4, sticky=NW)
        tk.Label(self._text_frame, text = "Welcome to MB Defender! Please select an option above.").grid(row=1, column=0)
        # active frame with variable use
        self._active_frame = tk.Frame(self._window)
        self._active_frame.grid(row=2, column=0, columnspan=8, sticky=W)
        self._window.mainloop()


    def _allowlist(self):

        def select_files():
            filetypes = (
                # ('text files', '*.txt'),
                # ('exec files', '*.exe'),
                ('any files', '*'),
                ('All files', '*.*')
            )

            filenames = fd.askopenfilenames(
                title='Open a file',
                initialdir='./',
                filetypes=filetypes)
            
            # add files to allowlist
            f1 = open("file_allow", 'a+')
            for x in filenames:
                f1.write("\n" + x)
            f1.close()
            self._allowlist()
        
        def delete_file():
            # print (listbox.curselection())
            sel_list = []
            for index in listbox.curselection():
                sel_list.append(listbox.get(index))
            with open("file_allow", "r") as f:
                lines = f.readlines()
            with open("file_allow", "w") as f:
                for line in lines:
                    if line.strip("\n") not in sel_list:
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
        
        open_button = tk.Button(
            self._active_frame,
            text='Add Files to Allowlist',
            command=select_files
            )
        open_button.grid(row=1, column = 0)
        submitbutton3 = tk.Button(self._active_frame, text = "Delete Selected File",highlightbackground='green', command=delete_file)
        submitbutton3.grid(row = 5, column = 0)

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

    def _targets(self):
        # allows user to submit files with target hashes
        def select_files():
            filetypes = (
                # ('text files', '*.txt'),
                # ('exec files', '*.exe'),
                ('any files', '*'),
                ('All files', '*.*')
            )

            filenames = fd.askopenfilenames(
                title='Open a file',
                initialdir='./',
                filetypes=filetypes)
            
            # add hashes to target
            f1 = open("hash_db", 'a+')
            for x in filenames:
                a = open(x,'r')
                f1.write(a.read())
                a.close()
            f1.close()
            self._targets()
            
        def select_files_regx():
            filetypes = (
                # ('text files', '*.txt'),
                # ('exec files', '*.exe'),
                ('any files', '*'),
                ('All files', '*.*')
            )

            filenames = fd.askopenfilenames(
                title='Open a file',
                initialdir='./',
                filetypes=filetypes)
            
            # add hashes to target
            f1 = open("regx_db", 'a+')
            for x in filenames:
                a = open(x,'r')
                f1.write(a.read())
                a.close()
            f1.close()
            self._targets()
        

        # function to add a file
        # delete old widgets in text frame and active frame
        for widget in self._text_frame.winfo_children():
            widget.destroy()
        for widget in self._active_frame.winfo_children():
            widget.destroy()

        # text frame
        # update text frame
        tk.Label(self._text_frame, text = "MBDefender finds malware using hash signatures and binary regex- you can add your own signatures to our database below.").grid(row=1, column=0, sticky=NW)
        # update active frame:
        submitbutton = tk.Button(self._active_frame, text = "Add file of MD5 hashes",highlightbackground='green', command=select_files)
        submitbutton.grid(row = 2, column = 2, sticky=NW)
        # other button
        # update active frame:
        submitbutton2 = tk.Button(self._active_frame, text = "Add file containing binary signature (in hex)",highlightbackground='green', command=select_files_regx)
        submitbutton2.grid(row = 3, column = 2, sticky=NW)

    def _countermeasures(self):
        # allows user to configure counter_config file
        def sel():
            with open("counter_config.txt", "w") as myfile:
                myfile.write(str(var.get()))
            self._countermeasures()
        

        # delete old widgets in text frame and active frame
        for widget in self._text_frame.winfo_children():
            widget.destroy()
        for widget in self._active_frame.winfo_children():
            widget.destroy()

        # text frame
        # update text frame
        tk.Label(self._text_frame, text = "Select Countermeasure Procedure Preference:").grid(row=1, column=0)
        # update active frame:
        var = IntVar()
        # get value from file
        with open("counter_config.txt") as f:
            firstline = f.readline().rstrip()
        var.set(int(firstline))
        R1 = Radiobutton(self._active_frame, text="Warning Mode: Alert user when malicious file found.", variable=var, value=0,
                  command=sel)      
        R1.grid(column=0,
            row=2,
            sticky='w')
        R2 = Radiobutton(self._active_frame, text="Isolate Mode: Quarantine malicious files when found.", variable=var, value=1,
                  command=sel)
        R2.grid(column=0,
            row=3,
            sticky='w')
        R3 = Radiobutton(self._active_frame, text="Delete Mode: Delete malicious files when found.", variable=var, value=2,
                  command=sel)
        R3.grid(column=0,
            row=4,
            sticky='w')
        
    def _scanlist(self):
        def select_files():
            filetypes = (
                # ('text files', '*.txt'),
                # ('exec files', '*.exe'),
                ('any files', '*'),
                ('All files', '*.*')
            )

            filenames = fd.askopenfilenames(
                title='Open a file',
                initialdir='./',
                filetypes=filetypes)
            
            # add files to scan_db
            f1 = open("scan_db", 'a+')
            for x in filenames:
                if os.stat("scan_db").st_size == 0:
                    f1.write(x)
                else:
                    f1.write("\n" + x)
            f1.close()
            self._scanlist()
        
        def select_dir():

            dirname = fd.askdirectory(
                title='Open a file',
                initialdir='/')
            
            # add dirs to scan_db
            f1 = open("scan_db", 'a+')
            
            f1.write("\n" + dirname)
            f1.close()
            self._scanlist()
        
        def delete_file():
            # print (listbox.curselection())
            sel_list = []
            for index in listbox.curselection():
                sel_list.append(listbox.get(index))
            with open("scan_db", "r") as f:
                lines = f.readlines()
            with open("scan_db", "w") as f:
                for line in lines:
                    if line.strip("\n") not in sel_list:
                        f.write(line)
            self._scanlist()
            
            
            
        # function to add a file
        # delete old widgets in text frame and active frame
        for widget in self._text_frame.winfo_children():
            widget.destroy()
        for widget in self._active_frame.winfo_children():
            widget.destroy()
        
        # update text frame
        tk.Label(self._text_frame, text = "Schedule scans and configure which files should be scanned.").grid(row=1, column=0)
        # update active frame:
        
        open_button = tk.Button(
            self._active_frame,
            text='Add Files to be Scanned',
            command=select_files
            )
        open_button.grid(row=2, column = 0, sticky="w")
        open_button2 = tk.Button(
            self._active_frame,
            text='Add Directory to be Scanned',
            command=select_dir
            )
        open_button2.grid(row=2, column = 0, sticky="e")
        submitbutton3 = tk.Button(self._active_frame, text = "Delete Selected File",highlightbackground='green', command=delete_file)
        submitbutton3.grid(row = 5, column = 0)

        # add list of files to active frame
        # open file, gather all filenames
        filepath = 'scan_db'
        filenames = []
        fp = open(filepath, 'r')
        filenames = fp.read().split('\n')
        # create listbox
        langs_var = tk.StringVar(value=filenames)
        box_label = tk.Label(self._active_frame, text = "Current scanlist:")
        box_label.grid(row = 3, column = 0)
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
    
    def _scan(self):
        def _sub():
            # update the crontab file
            # print("hi")
            cron = CronTab(user=True)
            cron.remove_all()
            job = cron.new(command='python3 final_exec.py')
            if var.get() == 0:
                # schedule every day
                job.day.on(0,1,2,3,4,5,6)
            elif var.get() == 1:
                # schedule every week on friday
                job.day.on(5)
            elif var.get() == 2:
                job.every().month()
            cron.write()
    
        def _run():
            # scan files, updating malfile.txt
            print(var.get())
            os.system("python3 scan2.py -s")
            # grab countermeasure setting
            os.system("python3 final_exec.py")
            self._scan()

        # delete old widgets in text frame and active frame
        for widget in self._text_frame.winfo_children():
            widget.destroy()
        for widget in self._active_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self._text_frame, text = "Update Scheduling Preferences here: this automatically scans files listed in scan_db.").grid(row=1, column=0)
        var = IntVar()
        R1 = Radiobutton(self._active_frame, text="Daily Scan", variable=var, value=0)      
        R1.grid(column=0,
            row=2,
            sticky='w')
        R2 = Radiobutton(self._active_frame, text="Weekly Scan", variable=var, value=1)
        R2.grid(column=0,
            row=3,
            sticky='w')
        R3 = Radiobutton(self._active_frame, text="Monthly Scan", variable=var, value=2)
        R3.grid(column=0,
            row=4,
            sticky='w')

        tk.Button(self._active_frame,
                text = "Update Preferences",highlightbackground='green',
                command = _sub).grid(row=5, column=0)
        
        tk.Button(self._active_frame,
                text = "Immediate Scan",highlightbackground='red',
                command = _run).grid(row=6, column=0)
        # select scheduling preference




if __name__ == "__main__":
    # try:
    
        a = MenuGUI()
