#-------------------------------------------------------------------------------
# Name:        Time-motion Workflow Data Analysis GUI
# Purpose:     For the Time-motion workflow study in Human Movement Biomechanics Lab
#	       University of Arizona
#
# Author:      Liang Gao
#
# Created:     24/06/2015
# Copyright:   (c) Liang Gao 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#from PIL import Image
#from numpy import *
from pylab import *
#import imtools

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# from Tkinter import Tk, Button, Checkbutton, Label, Entry, Frame
from Tkinter import *
import sqlite3

def BarpltString(s):
        labels, values = zip(*Counter(s).items())
        # print(labels)
        # print(values)
        indexes = np.arange(len(labels))
        width = 1
        f = figure()
        plt.bar(indexes, values, width)
        plt.xticks(indexes + width * 0.5, labels)
        plt.show()
        return f

class App:
    def __init__(self, master):
        
        # self.ShowObs()
        # self.ShowPhy()
        # self.TestButton()
        # self.ShowTime()
        # self.ExecuteSQL()
        column0_padx = 24
        row_pady = 36
        
        # buttons for showing the record of observers/physicians
        lbl_Time_Period_Y = Label(master, text="Year",
                                  wraplength=100, anchor='w', justify='left')
        lbl_Time_Period_M = Label(master, text="Month",
                                wraplength=100, justify='left')
        # lbl_All_Time = Label(master, text="All time",
                                # wraplength=100, justify='left')
        # Time_Period_Y = Entry(master)
        self.year = StringVar(master)
        Years = ['2015', '2014', '2013', '2012', '2011']
        self.year.set(Years[0])
        Time_Period_Y = OptionMenu(master, self.year, *Years)
        # Time_Period_M = Entry(master)
        self.month = StringVar(master)
        Months = np.arange(12) + 1;
        self.month.set(Months[0])
        Time_Period_M = OptionMenu(master, self.month, *Months)
        self.var_All_Time = IntVar()
        ck_All_Time = Checkbutton(master, text = 'over all the time', width=10, variable = self.var_All_Time)
        self.btn_ShowObs = Button(master, text = "Show the Observers' Record", width=25, command=self.ShowObs)
        self.btn_ShowPhy = Button(master, text="Show the Physicians' Record", width=25, command=self.ShowPhy)

        lbl_Time_Period_Y.grid(row=0, column=2, padx=20, pady=12, sticky='w')
        lbl_Time_Period_M.grid(row=0, column=3, pady=12, sticky='w')
        # lbl_All_Time.grid(row=0, column=4, padx=20, pady=12, sticky='wn')
        self.btn_ShowObs.grid(row=1, column=0, sticky='w', padx=column0_padx)
        self.btn_ShowPhy.grid(row=1, column=1, sticky='w')
        Time_Period_Y.grid(row=1, column=2, padx=20, sticky='w')
        Time_Period_M.grid(row=1, column=3, sticky='w')
        ck_All_Time.grid(row=1, column=4, padx=20, sticky='w')
        
        # buttons for showing the patient time for different types of exame
        lbl_Patient_ID = Label(master, text="Patient ID:",
                            wraplength=100, anchor='w', justify='left')
        self.Patient_ID = Entry(master)
        lbl_All_Patient=Label(master, text="or check",
                            wraplength=100, anchor='w', justify='left')
        self.var_All_Pat = IntVar()
        ck_All_Patients=Checkbutton(master, text = "for all Patients.", width=10,variable = self.var_All_Pat)
        lbl_Type_ID = Label(master, text="Select the exam type:",
                            wraplength=100, anchor='w', justify='left')
        # Type_ID = Entry(master)
        self.type = StringVar(master)
        Types = np.arange(5) + 1;
        self.type.set(Types[0])
        Type_ID = OptionMenu(master, self.type, *Types)
        lbl_All_Types=Label(master, text="or check",
                            wraplength=200, anchor='w', justify='left')
        self.var_All_Type = IntVar()
        ck_All_Types=Checkbutton(master, text = "for all types.", width=10, variable = self.var_All_Type)
        self.btn_Pat_Time=Button(master, text="Show time", width=15, command=self.ShowTime)
        
        lbl_Patient_ID.grid(row = 2, column = 0,  sticky='w', padx=column0_padx)
        self.Patient_ID.grid(row=2, column=1, sticky='w')
        lbl_All_Patient.grid(row=2, column=2, padx=20, sticky='w')
        ck_All_Patients.grid(row=2, column=3, sticky='w')
        lbl_Type_ID.grid(row = 3, column = 0,  sticky='w', padx=column0_padx)
        Type_ID.grid(row=3, column=1, sticky='w')
        lbl_All_Types.grid(row=3, column=2, padx=20, sticky='w')
        ck_All_Types.grid(row=3, column=3, sticky='w')
        self.btn_Pat_Time.grid(row=3, column=4, padx=20, sticky='w')
        
        self.btn_TEST = Button(master, text="Test Button", width=25, command=self.TestButton)
        self.btn_TEST.grid(row=2, column=4, padx=20, sticky='w')
        
        # Canvas for plots
        Fig_frame = Frame(master)
        Fig_frame.grid(row=4, column=1,columnspan=5, sticky='w',padx=column0_padx)
        canvas_width = 300
        canvas_height = 200
        self.cav_Plot = Canvas(Fig_frame, bg="gray", width=canvas_width, height=canvas_height)
        self.cav_Plot.pack()
        
        # Execute SQL
        SQL_frame = Frame(master)
        SQL_frame.grid(row=5, column=0, columnspan=5, sticky='w',padx=column0_padx, pady=row_pady)
        lbl_SQL_query = Label(SQL_frame, text="SQL query:")
        lbl_SQL_query.pack(side = 'left')
        self.SQL_query = Entry(SQL_frame,width=50)
        self.SQL_query.pack(side = 'left',padx=80);
        self.btn_Execute_SQL = Button(SQL_frame, text="Execute", width=10, command=self.ExecuteSQL)
        self.btn_Execute_SQL.pack(side = 'left');
        
        
    def ShowObs(self):
        print 'Displaying the frequency for all the observers during the selected time period.'
        con = sqlite3.connect('MotionTimeRecorder.sqlite')
        con.text_factory = str
        cur = con.cursor()
        cur.execute("select ZOBSERVERNAME from ZSESSION")
        obs = cur.fetchall()
        obs = ['%s' % x for x in obs]
        # print(obs[0:5])
        BarpltString(obs)

    def ShowPhy(self):
        print 'Displaying the frequency for all the physicians during the selected time period.'
        con = sqlite3.connect('MotionTimeRecorder.sqlite')
        con.text_factory = str
        cur = con.cursor()
        cur.execute("select ZPHYSICIANNAME from ZSESSION")
        phy = cur.fetchall()
        phy = ['%s' % x for x in phy]
        # print(phy[0:5])
        BarpltString(phy)  

    def TestButton(self):
        print '=========This is just a test Bottom.========='
        print 'year = %s, month = %s, exam type = %s' %(self.year.get(), self.month.get(), self.type.get())
        print 'the all time check box is %d' %self.var_All_Time.get()
        print 'the all patients check box is %d' %self.var_All_Pat.get()
        print 'the current patient id is "%s"' %self.Patient_ID.get()
        print 'the all types check box is %d' %self.var_All_Type.get()

    def ShowTime(self):
        print 'Displaying the time for selected patient(s) for selected type(s) during selected time.'
        
    def ExecuteSQL(self):
        print 'Executing the following SQL query:'
        print self.SQL_query.get()
        # con = sqlite3.connect('MotionTimeRecorder.sqlite')
        # con.text_factory = str
        # cur = con.cursor()
        # Q = ''
        # cur.execute(Q)

if __name__ == '__main__':
    root = Tk()
    root.title("Time-motion Workflow Data Analysis Tool v0.2")
    root.minsize(800, 400)
    app = App(root)
    root.mainloop()
