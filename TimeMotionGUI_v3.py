#-------------------------------------------------------------------------------
# Name:        Time-motion Workflow Data Analysis GUI
# Purpose:     For the Time-motion workflow study in Human Movement Biomechanics Lab
#	       University of Arizona
#
# Author:      Liang Gao
#
# Created:     06/24/2015
# Copyright:   (c) Liang Gao 2015
#-------------------------------------------------------------------------------

#from PIL import Image
from pylab import *

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# from Tkinter import Tk, Button, Checkbutton, Label, Entry, Frame
from Tkinter import *
import sqlite3

def GetValues(qry, sqlitefile, printvalues=0):
    con = sqlite3.connect(sqlitefile)
    con.text_factory = str
    cur = con.cursor()
    cur.execute(qry)
    vals = cur.fetchall()
    vals = ['%s' % x for x in vals]
    if printvalues == 1:
        print vals
    return vals

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

def Time2Sec(str0):
    str1 = str0[9:]
    h = int(str1[0:2])
    m = int(str1[2:4])
    s = int(str1[4:])/1000
    totalsec = 3600*h + 60*m + s
    return totalsec
        
class App:
    def __init__(self, master):

        column0_padx = 24
        row_pady = 36
        self.phy_dict = {} # list for all physicians
        
        # buttons for showing the record of observers/physicians
        lbl_Select_Phy = Label(master, text="Select Physician:",
                                  wraplength=100, anchor='w', justify='left')
        lbl_Time_Period_Y = Label(master, text="Year",
                                  wraplength=100, anchor='w', justify='left')
        lbl_Time_Period_M = Label(master, text="Month",
                                wraplength=100, justify='left')
        self.select_phy = StringVar(master)
        Phy_names = range(20)
        self.select_phy.set(Phy_names[0])
        Select_physician = OptionMenu(master, self.select_phy, *Phy_names)
        # lbl_All_Time = Label(master, text="All time",
                                # wraplength=100, justify='left')
        self.year = StringVar(master)
        Years = ['2015', '2014', '2013', '2012', '2011']
        self.year.set(Years[0])
        Time_Period_Y = OptionMenu(master, self.year, *Years)
        self.month = StringVar(master)
        Months = np.arange(12) + 1;
        self.month.set(Months[0])
        Time_Period_M = OptionMenu(master, self.month, *Months)
        # self.var_All_Time = IntVar()
        # ck_All_Time = Checkbutton(master, text = 'over all the time', width=10, variable = self.var_All_Time)
        self.btn_ShowObs = Button(master, text = "Show the Observers' Record", width=25, command=self.ShowObs)
        self.btn_ShowPhy = Button(master, text="Show the Physicians' Record", width=25, command=self.ShowPhy)

        lbl_Select_Phy.grid(row=0, column=2, padx=20, pady=12, sticky='w')
        lbl_Time_Period_Y.grid(row=0, column=3, padx=20, pady=12, sticky='w')
        lbl_Time_Period_M.grid(row=0, column=4, pady=12, sticky='w')
        # lbl_All_Time.grid(row=0, column=4, padx=20, pady=12, sticky='wn')
        self.btn_ShowObs.grid(row=1, column=0, sticky='w', padx=column0_padx)
        self.btn_ShowPhy.grid(row=1, column=1, sticky='w')
        Select_physician.grid(row=1, column=2, padx=20, sticky='w')
        Time_Period_Y.grid(row=1, column=3, padx=20, sticky='w')
        Time_Period_M.grid(row=1, column=4, sticky='w')
        # ck_All_Time.grid(row=1, column=4, padx=20, sticky='w')
        
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
        self.ExamType = StringVar(master)
        ExamTypes = ['All', '1(exam)','2(discussion)','3','4(typing)','5','6','9'];
        self.ExamType.set(ExamTypes[0])
        Type_ID = OptionMenu(master, self.ExamType, *ExamTypes)
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
        
        self.btn_TEST = Button(master, text="Show PIDs", width=15, command=self.TestButton)
        self.btn_TEST.grid(row=2, column=4, padx=20, sticky='w')
        
        # Canvas for plots, may need to remove
        # Fig_frame = Frame(master)
        # Fig_frame.grid(row=4, column=1,columnspan=5, sticky='w',padx=column0_padx)
        # canvas_width = 300
        # canvas_height = 200
        # self.cav_Plot = Canvas(Fig_frame, bg="gray", width=canvas_width, height=canvas_height)
        # self.cav_Plot.pack()
        
        # Execute SQL
        SQL_frame = Frame(master)
        SQL_frame.grid(row=5, column=0, columnspan=5, sticky='w',padx=column0_padx, pady=row_pady)
        lbl_SQL_query = Label(SQL_frame, text="SQL query:")
        lbl_SQL_query.pack(side = 'left')
        self.SQL_query = Entry(SQL_frame,width=80)
        self.SQL_query.pack(side = 'left',padx=80);
        self.btn_Execute_SQL = Button(SQL_frame, text="Execute", width=10, command=self.ExecuteSQL)
        self.btn_Execute_SQL.pack(side = 'left');
        
        
    def ShowObs(self):
        print 'Displaying the frequency for all the observers during the selected time period.'
        filename = 'MotionTimeRecorder.sqlite';
        qry = "select ZOBSERVERNAME from ZSESSION";
        obs = GetValues(qry, filename);
        BarpltString(obs)

    def ShowPhy(self):
        phy_dict = {}
        print 'Displaying the frequency for all the physicians during the selected time period.'
        filename = 'MotionTimeRecorder.sqlite';
        qry = "select ZPHYSICIANNAME from ZSESSION"
        phy = GetValues(qry, filename)
        phynames = sorted(set(phy));
        phy_dict.fromkeys(range(1, len(phy)+1))
        # print phy_dict
        for n in range(1, len(phynames)+1):
            phy_dict[n] = phynames[n-1]
        print 'you may choose the physician from the list below (or 0 for all):'
        print phy_dict
        self.phy_dict = phy_dict
        BarpltString(phy)
        
    def TestButton(self):
        print '=========This is just a test Botton.========='
        print 'you selected # %s physician.' % self.select_phy.get()
        print 'year = %s, month = %s, exam type = %s' %(self.year.get(), self.month.get(), self.ExamType.get())
        # print 'the all time check box is %d' %self.var_All_Time.get()
        print 'the all patients check box is %d' %self.var_All_Pat.get()
        print 'the current patient id is "%s"' %self.Patient_ID.get()
        print 'the all types check box is %d' %self.var_All_Type.get()
        # filename = 'MotionTimeRecorder.sqlite';
        # qry = "select zpatient from ztask"
        # PID = GetValues(qry, filename)
        # PID = sorted(set(PID))
        # print PID
        print self.phy_dict

        
    def ShowTime(self):
        phy_key = self.select_phy.get()
        print '===Displaying the time for selected patient(s) for selected type(s) during selected time.==='
        if phy_key == '0':
            print 'no particular physician was selected'
            PID = self.Patient_ID.get()
            print 'the current patient id is "%s"' % PID
            filename = 'MotionTimeRecorder.sqlite';
            qry = "select zstarttime from ztask where zpatient = " + str(PID);
            t0 = GetValues(qry, filename);
            qry = "select zstoptime from ztask where zpatient = " + str(PID)
            t1 = GetValues(qry, filename);

            tstart = []
            tstop = []
            dt = []
            for n in range(len(t0)):
                tstart.append(Time2Sec(t0[n]))
                tstop.append(Time2Sec(t1[n]))
                dt.append(tstop[n] - tstart[n])

            qry = "select ztaskid from ztask where zpatient = " + str(PID)
            taskid = GetValues(qry, filename)
            taskid = np.array([int(n) for n in taskid])/1000

            TotalTime_dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 9:0}
            for n in range(len(taskid)):
                if taskid[n] not in TotalTime_dict:
                    TotalTime_dict[taskid[n]] = dt[n]
                else:
                    TotalTime_dict[taskid[n]] = TotalTime_dict[taskid[n]] + dt[n]

            # print TotalTime_dict
            # print TotalTime_dict.keys()
            # print TotalTime_dict.values()
            f = figure()
            width = 0.5;
            x = np.array(TotalTime_dict.keys());
            y = np.array(TotalTime_dict.values());
            p1 = plt.bar(x[0:-1], y[0:-1], width)
            plt.ylabel('Time [s]')
            plt.xlabel('Task type')
            plt.title('Patient ' + PID)
            plt.xticks(x[0:-1] + width/2., x[0:-1])
            plt.show()
            close(f)
        elif int(phy_key) > len(self.phy_dict):
            print 'no such physician, please selec from the list below (or 0 for all):'
            print self.phy_dict
        else:
            phy_name = self.phy_dict[int(phy_key)]
            print 'showing the result for physician: %s' % phy_name
            filename = 'MotionTimeRecorder.sqlite';
            
            qry = "select z_pk from zsession where zphysicianname = '" + phy_name +"'"
            # print qry
            SID = GetValues(qry, filename)

            qry = "select z_pk from zpatient where zsession in (" + ','.join(SID) + ")"
            # print qry
            PID = GetValues(qry, filename)
            
            qry = "select zstarttime from ztask where zpatient in (" + ','.join(PID) + ")"
            # print qry
            t0 = GetValues(qry, filename)
            
            qry = "select zstoptime from ztask where zpatient in (" + ','.join(PID) + ")"
            # print qry
            t1 = GetValues(qry, filename)
            
            tstart = []
            tstop = []
            dt = []
            for n in range(len(t0)):
                tstart.append(Time2Sec(t0[n]))
                tstop.append(Time2Sec(t1[n]))
                dt.append(tstop[n] - tstart[n])
            
            qry = "select ztaskid from ztask where zpatient in (" + ','.join(PID) + ")"
            # print qry
            taskid = GetValues(qry, filename)
            taskid = np.array([int(n) for n in taskid])/1000

            TotalTime_dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 9:0}
            TaskType_count = {1:0.1, 2:0.1, 3:0.1, 4:0.1, 5:0.1, 6:0.1, 9:0.1}
            for n in range(len(taskid)):
                TotalTime_dict[taskid[n]] = TotalTime_dict[taskid[n]] + dt[n]
                if TaskType_count[taskid[n]] == 0.1:
                    TaskType_count[taskid[n]] = TaskType_count[taskid[n]] - 0.1 + 1
                else:
                    TaskType_count[taskid[n]] = TaskType_count[taskid[n]] + 1
                    
            # print TotalTime_dict
            # print TotalTime_dict.keys()
            # print TotalTime_dict.values()
            f = figure()
            width = 0.5;
            x = np.array(TotalTime_dict.keys());
            y = np.array(TotalTime_dict.values())*1.0/np.array(TaskType_count.values())
            p1 = plt.bar(x[0:-1], y[0:-1], width)
            plt.ylabel('Average time for each task [s]')
            plt.xlabel('Task type')
            plt.title('Physician ' + phy_key) # phy_key or phy_name
            plt.xticks(x[0:-1] + width/2., x[0:-1])
            # plt.show()
            fname = 'Physician ' + phy_key + '_1.png'
            savefig(fname)
            f.clf()
            
            # f = figure()
            width = 0.5;
            x = np.array(TotalTime_dict.keys());
            y = np.array(TotalTime_dict.values())
            p1 = plt.bar(x[0:-1], y[0:-1], width)
            plt.ylabel('Total time for each task [s]')
            plt.xlabel('Task type')
            plt.title('Physician ' + phy_key)
            plt.xticks(x[0:-1] + width/2., x[0:-1])
            # plt.show()
            fname = 'Physician ' + phy_key + '_2.png'
            savefig(fname)
            # close()
            f.clf()
            
            f = figure()
            width = 0.5;
            x = np.array(TotalTime_dict.keys());
            y = np.array(TotalTime_dict.values())*1.0/len(PID)
            p1 = plt.bar(x[0:-1], y[0:-1], width)
            plt.ylabel('Average time for each patient [s]')
            plt.xlabel('Task type')
            plt.title('Physician ' + phy_key)
            plt.xticks(x[0:-1] + width/2., x[0:-1])
            # plt.show()
            fname = 'Physician ' + phy_key + '_3.png'
            savefig(fname)
            close(f)
            
        
    def ExecuteSQL(self):
        print 'Executing the following SQL query:'
        print self.SQL_query.get()
        # con = sqlite3.connect('MotionTimeRecorder.sqlite')
        # con.text_factory = str
        # cur = con.cursor()
        # Q = ''
        # cur.execute(Q)
        filename = 'MotionTimeRecorder.sqlite';
        con = sqlite3.connect(filename)
        con.text_factory = str
        cur = con.cursor()
        cur.execute(self.SQL_query.get())
        vals = cur.fetchall()
        # vals = ['%s' % x for x in vals]
        for n in vals:
            print n
        # print vals

if __name__ == '__main__':
    root = Tk()
    root.title("Time-motion Workflow Data Analysis Tool v0.3")
    root.minsize(800, 400)
    app = App(root)
    root.mainloop()
