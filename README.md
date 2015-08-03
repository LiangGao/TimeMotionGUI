# TimeMotionGUI

GUI for Time Motion Workflow Data Analysis, to visualize changes in orthopaedic clinic workflow with the implementation of electronic medical record, for University of Arizona Medical Center - Tucson.

# History:
v0.5 (and 0.4) added the function to plot time for each physician, for all time or certain year; improved the way to make plots (now three plots in one figure); also added the button to choose the sqlite file.

v0.3 added the function to plot the time for individual patient; added the function to plot the time spent by individual physicians; removed the canvas (for now); user can execute SQL query now. Goal for v0.4: to sort time spent by visit type, and year; improve the way to make plots.

v0.2 rewrote all the button commands. changed the whole layout. (label text works under windows but shows irregular under mac)

v0.1 added first the function of show the records for observers and physicians. added basic layout.

# Introduction

We want to document the time spent for patients' visit after the implementation of electronic medical record (EMR). Student volunteers were recruited to follow physicians during patients’ visit, and record the time spend for each task.

The data are in SQL format, and contain several tables: The session table includes session IDs, physician names, and visit types. The patient table includes patient information. The task table includes the start time and end time for each task for each patient’s visit.

For example, during a patient’s visit, the time spent is as following:

![Example patient’s visit](Plots/Patient/Patient_1504.png)

There are 6 different task types, such as physical exam, discussion, and recording. 

The next figure shows how many sessions were record:
![Physician session recorded during the past 3 years](Plots/Physician/Physician_appearances.png)
The physicians were numbered as 1-8, instead of their real names here.

The following figure shows the time spent by physician #8 during the past 3 years:
![Time* spent by physician 8 during the past 3 years](Plots/Physician/Physician_8_Year_All_3figs.png)
The three subplots are the average time the physician spent for each task, the total time* he spent for each task, and the average time he spent for one patient.

(* the total time corresponds to only the time when the physician was followed by student volunteers, not the actually time spent by the physician.)

The time spent for each year (2013, 2014 and 2015) are as following:
![Time* spent by physician 8 during 2013](Plots/Physician/Physician_8_Year_2013_3figs.png)
![Time* spent by physician 8 during 2014](Plots/Physician/Physician_8_Year_2014_3figs.png)
![Time* spent by physician 8 during 2015](Plots/Physician/Physician_8_Year_2015_3figs.png)

It is clear that the time spent for each patient has been decreasing during the past 3 years.

# What’s next

There are still quite a lot analysis to do, lots of features to be added to the GUI.
