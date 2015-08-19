#-------------------------------------------------------------------------------
# Name:        Time-motion Workflow Data Analysis GUI
# Purpose:     For the Time-motion workflow study in Human Movement Biomechanics Lab
#	       University of Arizona
#
# Author:      Liang Gao
# updated:     08/18/2015
# Created:     06/24/2015
# Copyright:   (c) Liang Gao 2015
#-------------------------------------------------------------------------------

#from PIL import Image
from pylab import *
from datetime import datetime
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import csv
# from Tkinter import Tk, Button, Checkbutton, Label, Entry, Frame
from Tkinter import *
from tkFileDialog import askopenfilename
import sqlite3

def GetValues(qry, sqlitefile, printvalues=0):  # run SQL query and get values
    con = sqlite3.connect(sqlitefile)
    con.text_factory = str
    cur = con.cursor()
    cur.execute(qry)
    vals = cur.fetchall()
    vals = ['%s' % x for x in vals]
    if printvalues == 1:
        print vals
    return vals

def BarpltString(s,filename = 0):        # bar plot for list of strings
    labels, values = zip(*Counter(s).items())
    values = [y for (x,y) in sorted(zip(labels,values), key=lambda pair: pair[0])]
    labels = sorted(labels)
    indexes = np.arange(len(labels))
    width = 1
    f = figure()
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    if filename!=0:
        plt.xticks(indexes + width * 0.5, range(1,len(labels)+1))
        plt.ylabel('Number of appearances')
        plt.xlabel(filename)
        plt.title(filename + '_appearances')
        f.savefig(filename + '_appearances.png')
        print('Image file (' + filename + '_appearances.png) saved')
        resultFile = open(filename + '_appearances.csv','wb')
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows([indexes+1, labels, values])
        print('data for this plot have been saved to ' + filename +'_appearances.csv')
    plt.show()
    return f

def Str2Time(str0):         # convert string to datetime
    return datetime.strptime(str0, '%Y%m%d %H%M%S%f')
        
def IndexInList(x0, l):     # return the indices for element x0 in list l
    return [i for i , x in enumerate(l) if x == x0]

        
class App:
    def __init__(self, master):

        column0_padx = 24
        row_pady = 36
        self.phy_dict = {} # list for all physicians
        self.filename = 'MotionTimeRecorder.sqlite'
        # self.Patient_ID = ''
        
        plt.xkcd()                                  # make the plots xkcd-style

        # buttons for showing the record of observers/physicians
        self.btn_ChooseFile = Button(master, text = "Load file", width=25, command=self.ChooseFile)
        lbl_Select_Phy = Label(master, text="Select Physician:",
                                  wraplength=100, anchor='w', justify='left')
        lbl_Time_Period_Y = Label(master, text="Year",
                                  wraplength=100, anchor='w', justify='left')
        lbl_Time_Period_M = Label(master, text="Month (no use)",
                                wraplength=100, justify='left')
        self.select_phy = StringVar(master)
        Phy_names = range(1,20);
        Phy_names.insert(0, 'All');
        self.select_phy.set(Phy_names[0])
        Select_physician = OptionMenu(master, self.select_phy, *Phy_names)
        # lbl_All_Time = Label(master, text="All time",
                                # wraplength=100, justify='left')
        self.year = StringVar(master)
        Years = ['All', '2015', '2014', '2013', '2012', '2011']
        self.year.set(Years[0])
        Time_Period_Y = OptionMenu(master, self.year, *Years)
        self.month = StringVar(master)
        Months = range(1,13);
        Months.insert(0,'All');
        self.month.set(Months[0])
        Time_Period_M = OptionMenu(master, self.month, *Months)
        self.btn_ShowObs = Button(master, text = "Show the Observers' Record", width=25, command=self.ShowObs)
        self.btn_ShowPhy = Button(master, text="Show the Physicians' Record", width=25, command=self.ShowPhy)
        
        self.btn_ChooseFile.grid(row=0, column=0, pady=12, sticky='w', padx=column0_padx)
        lbl_Select_Phy.grid(row=0, column=2, padx=20, pady=12, sticky='w')
        lbl_Time_Period_Y.grid(row=0, column=3, padx=20, pady=12, sticky='w')
        lbl_Time_Period_M.grid(row=0, column=4, pady=12, sticky='w')
        self.btn_ShowObs.grid(row=1, column=0, sticky='w', padx=column0_padx)
        self.btn_ShowPhy.grid(row=1, column=1, sticky='w')
        Select_physician.grid(row=1, column=2, padx=20, sticky='w')
        Time_Period_Y.grid(row=1, column=3, padx=20, sticky='w')
        Time_Period_M.grid(row=1, column=4, sticky='w')
        
        # buttons for showing the patient time for different types of task
        lbl_Patient_ID = Label(master, text="Patient ID:",
                            wraplength=100, anchor='w', justify='left')
        self.Patient_ID = Entry(master)     
        
        lbl_Type_ID = Label(master, text="Select task type:",
                            wraplength=100, anchor='w', justify='left')
        self.TaskType = StringVar(master)
        TaskTypes = ['All', '1-(Review and Exam)','2-(Discussion)','3-(Prescriptions)',
                        '4-(Typing)','5-(Activities)','6-(Start and Finish)','9-(Idle)'];
        self.TaskType.set(TaskTypes[0])
        Type_ID = OptionMenu(master, self.TaskType, *TaskTypes)
        lbl_Save_data=Label(master, text="Save data?",
                            wraplength=100, anchor='w', justify='left')
        self.var_Save_Data = IntVar()
        ck_Save_data=Checkbutton(master, text = "Save data", width=10, variable = self.var_Save_Data)
        self.btn_Pat_Time=Button(master, text="Show time", width=15, command=self.ShowTime)
        
        lbl_Visit_Type = Label(master, text="Select visit type:",
                            wraplength=100, anchor='w', justify='left')
        self.VisitType = StringVar(master)
        VisitTypes = ['All', '1-(New - Att)','2-(New - Res/PA)','3-(Return - Att)',
                        '4-(Return - Res/PA)','5-(Post Op - Att)','6-(Post Op - Res/PA)'];
        self.VisitType.set(VisitTypes[0])
        Visit_Type = OptionMenu(master, self.VisitType, *VisitTypes)      

        self.btn_TimeByVisitType = Button(master, text="Show Time By Visit Type", width=25, command=self.TimeByVisitType)
        
        lbl_Patient_ID.grid(row = 2, column = 0,  sticky='w', padx=column0_padx)
        self.Patient_ID.grid(row=2, column=1, sticky='w')
        # lbl_Visit_Type.grid(row = 2, column = 2,  sticky='w')
        # Visit_Type.grid(row=2, column=3, padx=20, sticky='w')
        lbl_Type_ID.grid(row = 3, column = 0,  sticky='w', padx=column0_padx)
        Type_ID.grid(row=3, column=1, sticky='w')
        lbl_Save_data.grid(row=3, column=2, padx=20, sticky='w')
        ck_Save_data.grid(row=3, column=3, sticky='w')
        self.btn_Pat_Time.grid(row=3, column=4, padx=20, sticky='w')
        lbl_Visit_Type.grid(row = 4, column = 0,  sticky='w', padx=column0_padx)
        Visit_Type.grid(row=4, column=1, sticky='w')
        self.btn_TimeByVisitType.grid(row=4, column=2, padx=20, sticky='w')
        
        self.btn_TEST = Button(master, text="TestButton", width=15, command=self.TestButton)
        self.btn_TEST.grid(row=2, column=4, padx=20, sticky='w')
        
        # Execute SQL
        SQL_frame = Frame(master)
        SQL_frame.grid(row=6, column=0, columnspan=5, sticky='w',padx=column0_padx, pady=row_pady)
        lbl_SQL_query = Label(SQL_frame, text="SQL query:")
        lbl_SQL_query.pack(side = 'left')
        self.SQL_query = Entry(SQL_frame,width=80)
        self.SQL_query.pack(side = 'left',padx=80);
        self.btn_Execute_SQL = Button(SQL_frame, text="Execute", width=10, command=self.ExecuteSQL)
        self.btn_Execute_SQL.pack(side = 'left');
        
    def ChooseFile(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        if filename[-7:] != '.sqlite':
            print "Please choose a '.sqlite' file"
            print "Or the program will try to load file '" + self.filename + "' in the current folder"
        else:
            self.filename = filename
            print("====== SQL file to be loaded: " + self.filename + " ======")
    
    def ShowObs(self):
        print 'Displaying the frequency for all the observers during the selected time period.'
        # filename = 'MotionTimeRecorder.sqlite';
        filename = self.filename
        qry = "select ZOBSERVERNAME from ZSESSION";
        obs = GetValues(qry, filename);
        BarpltString(obs, 'observer')

    def ShowPhy(self):
        phy_dict = {}
        print 'Displaying the frequency for all the physicians during the selected time period.'
        # filename = 'MotionTimeRecorder.sqlite';
        filename = self.filename
        qry = "select ZPHYSICIANNAME from ZSESSION"
        phy = GetValues(qry, filename)
        phynames = sorted(set(phy));
        phy_dict.fromkeys(range(1, len(phy)+1))
        for n in range(1, len(phynames)+1):
            phy_dict[n] = phynames[n-1]
        print 'you may choose the physician from the list below (or All):'
        print phy_dict
        self.phy_dict = phy_dict
        BarpltString(phy, 'Physician')
        
    def TestButton(self):
        print '=========This is just a test Botton.========='
        print 'you selected # %s physician.' % self.select_phy.get()
        print 'year = %s, month = %s, task type = %s' %(self.year.get(), self.month.get(), self.TaskType.get())
        # print 'the all time check box is %d' %self.var_All_Time.get()
        # print 'the all patients check box is %d' %self.var_All_Pat.get()
        print 'the current patient id is "%s"' %self.Patient_ID.get()
        print 'the save data check box is %d' %self.var_Save_Data.get()
        print self.phy_dict
        print 'the current visit type is "%s"' % self.VisitType.get()

        
    def ShowTime(self):
        phy_key = self.select_phy.get()
        year_key = self.year.get()
        month_key = self.month.get()
        TaskType_key = self.TaskType.get()
        PID = self.Patient_ID.get()
        print '===Displaying the time for selected patient(s) for selected type(s) during selected time.==='
        if phy_key == 'All' or self.Patient_ID.get() != '':
            # PID = self.Patient_ID.get()
            print 'the current patient id is "%s"' % PID
            # filename = 'MotionTimeRecorder.sqlite';
            print '!!! IMPORTANT: please clear the patient ID before making other plots !!!'
            filename = self.filename
            qry = "select zstarttime from ztask where zpatient = " + str(PID);
            t0 = GetValues(qry, filename);
            qry = "select zstoptime from ztask where zpatient = " + str(PID)
            t1 = GetValues(qry, filename);

            tstart = []
            tstop = []
            dt = []
            for n in range(len(t0)):
                tstart.append(Str2Time(t0[n]))
                tstop.append(Str2Time(t1[n]))
                dt0 = tstop[n] - tstart[n]
                dt.append(dt0.total_seconds())

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
            f.savefig('Patient_' + PID + '.png')
            plt.show()
            # close(f)
        elif int(phy_key) > len(self.phy_dict):
            print 'no such physician, please selec from the list below (or 0 for all):'
            print self.phy_dict
        else:
            phy_name = self.phy_dict[int(phy_key)]
            print 'showing the result for physician: %s' % phy_name
            # filename = 'MotionTimeRecorder.sqlite';
            filename = self.filename;
            
            if (TaskType_key == 'All'):
                print 'all task type'
                qry = "select z_pk from zsession where zphysicianname = '" + phy_name +"'"
                SID = GetValues(qry, filename)
                
                if (year_key != 'All'):
                    qry = "select zsessionid from zsession where zphysicianname = '" + phy_name +"'"
                    SID_datetime = GetValues(qry, filename)
                    
                    SID_datetime_year = [x[0:4] for x in SID_datetime]
                    SID_datetime_month = [x[4:6] for x in SID_datetime]
                    idx_Y = IndexInList(year_key, SID_datetime_year)
                    idx_M = IndexInList(month_key, SID_datetime_month)

                    newSID = [SID[i] for i in idx_Y]
                    SID = newSID
                
                qry = "select z_pk from zpatient where zsession in (" + ','.join(SID) + ")"
                PID1 = GetValues(qry, filename)
                qry = "select zpatient from ztask where zpatient in (" + ','.join(PID1) + ")"
                PID2 = GetValues(qry, filename)
                PID = sorted([int(n) for n in set(PID1) if n in set(PID2)])
                PID = [str(n) for n in PID]
                print 'Corresponding patient IDs:'
                print PID
                print 'total patient number = %s' % len(PID)
                qry = "select zstarttime from ztask where zpatient in (" + ','.join(PID) + ")"
                t0 = GetValues(qry, filename)
                qry = "select zstoptime from ztask where zpatient in (" + ','.join(PID) + ")"
                t1 = GetValues(qry, filename)
                
                tstart = []
                tstop = []
                dt = []
                for n in range(len(t0)):
                    tstart.append(Str2Time(t0[n]))
                    tstop.append(Str2Time(t1[n]))
                    dt0 = tstop[n] - tstart[n]
                    dt.append(dt0.total_seconds())
                
                qry = "select ztaskid from ztask where zpatient in (" + ','.join(PID) + ")"
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
                f = plt.figure()
                
                f.add_subplot(1,3,1)
                width = 0.5;
                x1 = np.array(TotalTime_dict.keys());
                y1 = np.array(TotalTime_dict.values())*1.0/np.array(TaskType_count.values())
                p1 = plt.bar(x1[0:-1], y1[0:-1], width)
                plt.ylabel('Average time for each task [sec]')
                plt.xlabel('Task type')
                plt.title('Physician ' + phy_key) # phy_key or phy_name
                plt.xticks(x1[0:-1] + width/2., x1[0:-1])
                plt.ylim((0, 150))
                
                f.add_subplot(1,3,2)
                width = 0.5;
                x2 = np.array(TotalTime_dict.keys());
                y2 = np.array(TotalTime_dict.values())
                p1 = plt.bar(x2[0:-1], y2[0:-1]/60, width)
                plt.ylabel('Total time for each task [min]')
                plt.xlabel('Task type')
                # plt.title('Physician ' + phy_key + ' Year ' + year_key)
                plt.title('Year ' + year_key)
                plt.xticks(x2[0:-1] + width/2., x2[0:-1])
                # plt.ylim((0, 400))
                
                f.add_subplot(1,3,3)
                width = 0.5;
                x3 = np.array(TotalTime_dict.keys());
                y3 = np.array(TotalTime_dict.values())*1.0/len(PID)
                p1 = plt.bar(x3[0:-1], y3[0:-1], width)
                plt.ylabel('Average time for each patient [sec]')
                plt.xlabel('Task type')
                # plt.title('Physician ' + phy_key + ', total ' + str(len(PID)) + ' patients')
                plt.title('Total ' + str(len(PID)) + ' patients')
                plt.xticks(x3[0:-1] + width/2., x3[0:-1])
                plt.ylim((0, 450))
                
                f.set_size_inches(18, 6, forward=True)
                fname = 'Physician_' + phy_key + '_Year_' + year_key + '_3figs'
                f.savefig(fname+'.png')
                print('Image file (' + fname + '.png) saved')
                if self.var_Save_Data.get() == 1:
                    resultFile = open(fname+'.csv','wb')
                    wr = csv.writer(resultFile, dialect='excel')
                    wr.writerows([x1,y1,x2,y2,x3,y3])
                    print('data for this plot have been saved to ' + fname + '.csv')
                plt.show()
                # close(f)        
                                                
            elif (TaskType_key != 'All'):
                TaskType_key = int(TaskType_key[0])*1000
                print 'All time, task type: %s' % TaskType_key
                qry = "select z_pk from zsession where zphysicianname = '" + phy_name +"'"
                SID = GetValues(qry, filename)                  # session id
                qry = "select z_pk from zpatient where zsession in (" + ','.join(SID) + ")"
                PID1 = GetValues(qry, filename)
                print len(set(PID1))
                qry = "select zpatient from ztask where zpatient in (" + ','.join(PID1) + ")"
                PID2 = GetValues(qry, filename)
                print len(set(PID2))
                PID = sorted([int(n) for n in set(PID1) if n in set(PID2)])
                PID = [str(n) for n in PID]
                print 'Corresponding patient IDs:'
                print PID              # patient id
                print 'total patients: ' + str(len(PID))
                qry = "select zstarttime from ztask where zpatient in (" + ','.join(PID) + ") and ztaskid between " + str(TaskType_key) + " and " + str(TaskType_key + 1000)
                t0 = GetValues(qry, filename)
                qry = "select zstoptime from ztask where zpatient in (" + ','.join(PID) + ") and ztaskid between " + str(TaskType_key) + " and " + str(TaskType_key + 1000)
                t1 = GetValues(qry, filename)
                
                tstart = []
                tstop = []
                dt = []
                for n in range(len(t0)):
                    tstart.append(Str2Time(t0[n]))
                    tstop.append(Str2Time(t1[n]))
                    dt0 = tstop[n] - tstart[n]
                    dt.append(dt0.total_seconds())
                print len(dt)
                
                qry = "select zpatient from ztask where zpatient in (" + ','.join(PID) + ") and ztaskid between " + str(TaskType_key) + " and " + str(TaskType_key + 1000)
                PID2 = GetValues(qry, filename)
                print len(set(PID2))
                qry = "select ztaskid from ztask where zpatient in (" + ','.join(PID) + ") and ztaskid between " + str(TaskType_key) + " and " + str(TaskType_key + 1000)
                taskid = GetValues(qry, filename)
                print 'total tasks: ' + str(len(taskid))
                uni_taskid = [int(n) for n in list(set(taskid))]
                
                Time_node_dict = {}
                All_year_list = [Str2Time(t).year for t in t0]
                Time_node_dict = Time_node_dict.fromkeys(set(All_year_list))
                for key in Time_node_dict.keys():
                    Time_node_dict[key] = All_year_list.index(key)
                # print All_year_list
                # print len(All_year_list)
                # print Time_node_dict
                # print Time_node_dict.values()
                
                f = plt.figure()
                
                newPID = [int(n) for n in set(PID2)]                # make plot for current task type
                newPID = [str(n) for n in sorted(newPID)]
                Pat_dict = {}
                t_node = []
                n = 0
                x_date = []
                for id in PID2:
                    if n in Time_node_dict.values():
                        # print n
                        # print id
                        t_node.append(newPID.index(id))
                    if id not in Pat_dict:
                        Pat_dict[id] = dt[n]
                        x_date.append(str(tstart[n].year) + '-' + str(tstart[n].month) + '-' + str(tstart[n].day))
                    else:
                        Pat_dict[id] = Pat_dict[id] + dt[n]
                    n = n + 1
                # print Pat_dict
                # print t_node
                # print len(Pat_dict)
                
                X = [int(n) for n in Pat_dict.keys()]
                Y = Pat_dict.values()
                y = [y for (x,y) in sorted(zip(X,Y), key=lambda pair: pair[0])]
                x = sorted(X)
                plt.plot(range(len(x)),y,'ro')
                for n in t_node:
                    plt.axvline(n)                  # add a vertical line for the beginning of each year 
                plt.xticks(t_node, sorted(Time_node_dict.keys()))
                plt.title('Physician_' + phy_key + '_TaskType_' + str(TaskType_key))
                plt.xlabel('year')
                plt.ylabel('time spent for each patient [s]')
                fname = 'Physician_' + phy_key + '_TaskType_' + str(TaskType_key) + '_figs'
                f.savefig(fname+'.png')
                print('Image file ('+ fname + '.png) saved')
                
                idx = t_node
                idx.append(len(y))
                T_md = []
                print idx
                n = 0
                for year in Time_node_dict.keys():
                    print('for year ' + str(year) + ', the median time is:')
                    md = np.median(y[idx[n]:idx[n+1]])
                    print md
                    T_md.append(md)
                    n = n + 1
                    
                if self.var_Save_Data.get() == 1:
                    resultFile = open(fname+'.csv','wb')
                    wr = csv.writer(resultFile, dialect='excel')
                    wr.writerows([x_date, x, y, t_node, Time_node_dict.keys(), T_md])
                    print('data for this plot have been saved to ' + fname + '.csv')
                f.clf()
                
                for id in sorted(uni_taskid):               # make plots for each sub-task type
                    print id
                    idx = IndexInList(str(id), taskid)
                    x0 = [tstart[i] for i in idx]
                    y0 = [dt[i] for i in idx]
                    # cnt_dict = {}
                    dt_dict = {}
                    n = 0
                    for x in x0:
                        x_date = str(x.year) + '-' + str(x.month) + '-' + str(x.day)
                        if x_date not in dt_dict:
                            # cnt_dict[x_date] = 1
                            # dt_dict[x_date] = y0[n]
                            dt_dict[x_date] = [y0[n]]
                        else:
                            # cnt_dict[x_date] = cnt_dict[x_date] + 1
                            # dt_dict[x_date] = dt_dict[x_date] + y0[n]
                            dt_dict[x_date].append(y0[n])
                        n = n + 1

                    width = 0.5;
                    # cnt = np.array(cnt_dict.values())
                    # print cnt_dict
                    # print dt_dict
                    # print cnt
                    # x = ([datetime.strptime(n, "%Y-%m-%d") for n in dt_dict.keys()])
                    x1 = dt_dict.keys()
                    # y1 = np.array(dt_dict.values())*1.0/cnt;
                    # y1 = [np.mean(n) for n in dt_dict.values()]
                    y1 = [np.median(n) for n in dt_dict.values()]
                    # print y1

                    y = [y for (x,y) in sorted(zip(x1,y1), key=lambda pair: pair[0])]
                    x = np.array(range(1,len(dt_dict.keys())+1))

                    p1 = plt.bar(x, y, width)
                    plt.title('task type ' + str(id))
                    plt.xlabel('date')
                    plt.ylabel('time spent [s]')
                    if len(x) > 8:
                        ticks = np.arange(min(x), max(x) + 1, 3)
                        xtick_lab = sorted(x1)
                        xtick_lab = [xtick_lab[i-1] for i in ticks]
                    else:
                        ticks = x
                        xtick_lab = sorted(x1)
                    plt.xticks(ticks + width/2., xtick_lab)
                    f.set_size_inches(10, 6, forward=True)
                    fname = 'Physician_' + phy_key + '_TaskType_' + str(id) + '_figs'
                    f.savefig(fname+'.png')
                    print('Image file ('+ fname + '.png) saved')
                    if self.var_Save_Data.get() == 1:
                        resultFile = open(fname+'.csv','wb')
                        wr = csv.writer(resultFile, dialect='excel')
                        wr.writerows([sorted(x1),y])
                        print('data for this plot have been saved to ' + fname + '.csv')
                    f.clf()
                plt.title('plots have been saved')
                plt.show()

            
            
    def TimeByVisitType(self):
        filename = self.filename;
        phy_key = self.select_phy.get()
        year_key = self.year.get()
        month_key = self.month.get()
        TaskType_key = self.TaskType.get()
        # TaskType_key = int(TaskType_key[0])*1000
        # PID = self.Patient_ID.get()
        VisitType_key = self.VisitType.get()
        
        # find the PID for selected physician
        # if phy_key ! = 'All':
            
            # PID_phy = 
        
        
        
        print '=== Displaying the time sorted by visit type ==='
        print 'the current visit type is "%s"' % VisitType_key
        if VisitType_key == 'All':
            print '==Please choose a certain visit type=='
            # print 'Actually I am not going to show anything here'
        elif TaskType_key == 'All':
            print '==Please choose a certain task type=='
        elif phy_key != 'All' and int(phy_key) > len(self.phy_dict):
            print 'no such physician, please selec from the list below (or 0 for all):'
            print self.phy_dict
        else:
            TaskType_key = int(TaskType_key[0])*1000
            VisitType_key = VisitType_key[3:-1]
            print '== Displaying the time for visit type "%s", task type "%s" ==' % (VisitType_key, TaskType_key)
            
            qry = "select z_pk from zpatient where zvisittype = '" + VisitType_key + "'"
            PID1 = GetValues(qry, filename)
            
            # if '/' in VisitType_key:
            # VisitType_key = VisitType_key.replace('/', '-');
            
            if phy_key != 'All':
                phy_name = self.phy_dict[int(phy_key)]
                print 'showing the result for physician: %s' % phy_name
                qry = "select z_pk from zsession where zphysicianname = '" + phy_name +"'"
                SID = GetValues(qry, filename)
                qry = "select z_pk from zpatient where zsession in (" + ','.join(SID) + ")"
                PID1_phy = GetValues(qry, filename)
                print '%s had %d patients.' % (phy_name, len(set(PID1_phy)))
                qry = "select zpatient from ztask where zpatient in (" + ','.join(PID1_phy) + ")"
                PID2_phy = GetValues(qry, filename)
                PID_phy = sorted([int(n) for n in set(PID1_phy) if n in set(PID2_phy)])
                PID_phy = [str(n) for n in PID_phy]
                PID1_tmp = PID1
                del PID1
                PID1 = [n for n in PID1_phy if n in PID1_tmp]
            
            print 'total patients with this visit type: %d' % len(PID1)
            qry = "select zpatient from ztask where zpatient in (" + ','.join(PID1) + ")"
            PID2 = GetValues(qry, filename)
            print 'Found %d of %d patients\' data' % (len(set(PID2)), len(PID1))
            PID = sorted([int(n) for n in set(PID1) if n in set(PID2)])
            PID = [str(n) for n in PID]
            print 'Corresponding patient IDs:'
            print PID
            print 'total patient number = %s' % len(PID)
            qry = "select zstarttime from ztask where zpatient in (" + ','.join(PID) + ") and ztaskid between " + str(TaskType_key) + " and " + str(TaskType_key + 1000)
            t0 = GetValues(qry, filename)
            qry = "select zstoptime from ztask where zpatient in (" + ','.join(PID) + ") and ztaskid between " + str(TaskType_key) + " and " + str(TaskType_key + 1000)
            t1 = GetValues(qry, filename)
            
            tstart = []
            tstop = []
            dt = []
            for n in range(len(t0)):
                tstart.append(Str2Time(t0[n]))
                tstop.append(Str2Time(t1[n]))
                dt0 = tstop[n] - tstart[n]
                dt.append(dt0.total_seconds())
            
            qry = "select zpatient from ztask where zpatient in (" + ','.join(PID) + ") and ztaskid between " + str(TaskType_key) + " and " + str(TaskType_key + 1000)
            PID2 = GetValues(qry, filename)
            qry = "select ztaskid from ztask where zpatient in (" + ','.join(PID) + ") and ztaskid between " + str(TaskType_key) + " and " + str(TaskType_key + 1000)
            taskid = GetValues(qry, filename)
            print 'total tasks: ' + str(len(taskid))
            uni_taskid = [int(n) for n in list(set(taskid))]
            
            Time_node_dict = {}
            All_year_list = [Str2Time(t).year for t in t0]
            Time_node_dict = Time_node_dict.fromkeys(set(All_year_list))
            for key in Time_node_dict.keys():
                Time_node_dict[key] = All_year_list.index(key)
            # print All_year_list
            # print len(All_year_list)
            # print Time_node_dict
            # print Time_node_dict.values()
            
            f = plt.figure()
            
            newPID = [int(n) for n in set(PID2)]                # make plot for current task type
            newPID = [str(n) for n in sorted(newPID)]
            # print newPID
            # print len(newPID)
            Pat_dict = {}
            t_node = []
            n = 0
            x_date = []
            for id in PID2:
                if n in Time_node_dict.values():
                    # print n
                    # print id
                    t_node.append(newPID.index(id))
                if id not in Pat_dict:
                    Pat_dict[id] = dt[n]
                    x_date.append(str(tstart[n].year) + '-' + str(tstart[n].month) + '-' + str(tstart[n].day))
                else:
                    Pat_dict[id] = Pat_dict[id] + dt[n]
                n = n + 1
            # print Pat_dict
            # print t_node
            # print len(Pat_dict)
            
            X = [int(n) for n in Pat_dict.keys()]
            Y = Pat_dict.values()
            y = [y for (x,y) in sorted(zip(X,Y), key=lambda pair: pair[0])]
            x = sorted(X)
            plt.plot(range(len(x)),y,'ro')
            for n in t_node:
                plt.axvline(n)                  # add a vertical line for the beginning of each year 
            plt.xticks(t_node, sorted(Time_node_dict.keys()))
            plt.title('Physician_' + phy_key + '_VisitType_' + str(VisitType_key) + '_TaskType_' + str(TaskType_key))
            plt.xlabel('year')
            plt.ylabel('time spent for each patient [s]')
            fname = 'Physician_' + phy_key + '_VisitType_' + str(VisitType_key) + '_TaskType_' + str(TaskType_key) + '_figs'
            fname = fname.replace('/', '-');
            f.savefig(fname+'.png')
            print('Image file ('+ fname + '.png) saved')
            
            idx = t_node
            idx.append(len(y))
            T_md = []
            print idx
            n = 0
            for year in Time_node_dict.keys():
                print('for year ' + str(year) + ', the median time is:')
                md = np.median(y[idx[n]:idx[n+1]])
                print md
                T_md.append(md)
                n = n + 1
                
            if self.var_Save_Data.get() == 1:
                resultFile = open(fname+'.csv','wb')
                wr = csv.writer(resultFile, dialect='excel')
                wr.writerows([x_date, x, y, t_node, Time_node_dict.keys(), T_md])
                print('data for this plot have been saved to ' + fname + '.csv')
            f.clf()
            
            for id in sorted(uni_taskid):               # make plots for each sub-task type
                print id
                idx = IndexInList(str(id), taskid)
                x0 = [tstart[i] for i in idx]
                y0 = [dt[i] for i in idx]
                # cnt_dict = {}
                dt_dict = {}
                n = 0
                for x in x0:
                    x_date = str(x.year) + '-' + str(x.month) + '-' + str(x.day)
                    if x_date not in dt_dict:
                        # cnt_dict[x_date] = 1
                        # dt_dict[x_date] = y0[n]
                        dt_dict[x_date] = [y0[n]]
                    else:
                        # cnt_dict[x_date] = cnt_dict[x_date] + 1
                        # dt_dict[x_date] = dt_dict[x_date] + y0[n]
                        dt_dict[x_date].append(y0[n])
                    n = n + 1

                width = 0.5;
                # cnt = np.array(cnt_dict.values())
                # print cnt_dict
                # print dt_dict
                # print cnt
                # x = ([datetime.strptime(n, "%Y-%m-%d") for n in dt_dict.keys()])
                x1 = dt_dict.keys()
                # y1 = np.array(dt_dict.values())*1.0/cnt;
                # y1 = [np.mean(n) for n in dt_dict.values()]
                y1 = [np.median(n) for n in dt_dict.values()]
                # print y1

                y = [y for (x,y) in sorted(zip(x1,y1), key=lambda pair: pair[0])]
                x = np.array(range(1,len(dt_dict.keys())+1))

                p1 = plt.bar(x, y, width)
                plt.title('task type ' + str(id))
                plt.xlabel('date')
                plt.ylabel('time spent [s]')
                if len(x) > 8:
                    ticks = np.arange(min(x), max(x) + 1, 3)
                    xtick_lab = sorted(x1)
                    xtick_lab = [xtick_lab[i-1] for i in ticks]
                else:
                    ticks = x
                    xtick_lab = sorted(x1)
                plt.xticks(ticks + width/2., xtick_lab)
                f.set_size_inches(10, 6, forward=True)
                fname = 'Physician_' + phy_key + '_VisitType_' + str(VisitType_key) + '_TaskType_' + str(id) + '_figs'
                fname = fname.replace('/', '-');
                f.savefig(fname+'.png')
                print('Image file ('+ fname + '.png) saved')
                if self.var_Save_Data.get() == 1:
                    resultFile = open(fname+'.csv','wb')
                    wr = csv.writer(resultFile, dialect='excel')
                    wr.writerows([sorted(x1),y])
                    print('data for this plot have been saved to ' + fname + '.csv')
                f.clf()
            plt.title('plots have been saved')
            plt.show()
            
            
        
    def ExecuteSQL(self):
        print 'Executing the following SQL query:'
        print self.SQL_query.get()
        # filename = 'MotionTimeRecorder.sqlite';
        filename = self.filename
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
    root.title("Time-motion Workflow Data Analysis Tool v0.7")
    root.minsize(800, 400)
    app = App(root)
    root.mainloop()
