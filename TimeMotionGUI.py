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

# from Tkinter import Tk, Button, Checkbutton, Label, Entry, Frame

import sqlite3

#from PIL import Image
#from numpy import *
#from pylab import *
#import imtools

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

from Tkinter import *

def ShowObs():
   #global current_colour_choices
   #res = new_evaluation(current_colour_choices)
   #current_colour_choices = res[0]
    print 'test...'

    con = sqlite3.connect('MotionTimeRecorder.sqlite')
    con.text_factory = str
    cur = con.cursor()
    # cur.execute("select ZOBSERVERNAME,ZPHYSICIANNAME from ZSESSION")
    cur.execute("select ZOBSERVERNAME from ZSESSION")
    obs = cur.fetchall()
    obs = ['%s' % x for x in obs]
    print(obs[0:5])
    #cur.execute("select ZPHYSICIANNAME from ZSESSION")
    #phy = cur.fetchall()
    #print(phy[0:5])
    #print '1111'
    #rows = cur.fetchall()
    #print(rows)

    labels, values = zip(*Counter(obs).items())

    indexes = np.arange(len(labels))
    width = 1

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()

    #x = [1,2,3,4,5]
    #y = x
    #figure()
    #plot(x,y)
    #show()


def ShowPhy():
    print '===This is show Physician button==='

    con = sqlite3.connect('MotionTimeRecorder.sqlite')
    con.text_factory = str
    cur = con.cursor()
    # cur.execute("select ZOBSERVERNAME,ZPHYSICIANNAME from ZSESSION")
    #cur.execute("select ZOBSERVERNAME from ZSESSION")
    #obs = cur.fetchall()
    #print(obs[0:5])
    cur.execute("select ZPHYSICIANNAME from ZSESSION")
    phy = cur.fetchall()
    phy = ['%s' % x for x in phy]
    print(phy[0:5])

    labels, values = zip(*Counter(phy).items())

    indexes = np.arange(len(labels))
    width = 1

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()



def ClearFig():
    print 'This is the ClearFig button'


class App:
    def __init__(self, master):
        column0_padx = 24
        row_pady = 36

        # title and version
        Title = Label(master, text="Time-motion Workflow Study Data Analysis Tool",font = "Verdana 20 bold")
        Title2 = Label(master, text="Human Movement Biomechanics Lab (HMBL), University of Arizona")
        version = Label(master, text="v0.1")
        Title.grid(row=1, column=0, sticky='w', padx=column0_padx)
        Title2.grid(row=2, column=0, sticky='w', padx=2*column0_padx)
        version.grid(row=1, column=1, sticky='w')

        # buttons
        bottom_frame = Frame(master)
        bottom_frame.grid(row=3, column=0, columnspan=3, sticky='w', padx=column0_padx)

        btn_start = Button(bottom_frame, text = "Show the Observers", width=20, command=ShowObs)
        btn_start.pack(side='left')
        btn_commit = Button(bottom_frame, text="Show the Physicians", width=20, command=ShowPhy)
        btn_commit.pack(side='left', padx=80)
        btn_exit = Button(bottom_frame, text="Clear Figure", width=15, command=ClearFig)
        btn_exit.pack(side='left')

root = Tk()
root.title("Time-motion Workflow Study Data Analysis Tool")
root.minsize(800, 400)
app = App(root)
root.mainloop()
