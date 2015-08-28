This codebook will show the instruction of how to use the GUI.

# System requirement
The OS I used mostly is Windows 8, but the program works on Mac OS too.
You need to install Python if using a Windows PC. Mac PC comes with Python installed. I used Python 2.7.9.

The Python libraries required are:
```
pylab
numpy
matplotlib
Tkinter
sqlite3
```

# Running the GUI
All you need is the TimeMotionGUI_??.py file. (?? may denotes the version information, for example TimeMotionGUI_**v7**.py) Download it (if you don't know how to use github you could just simply copy the texts and save them as a .py file), and put the .py file in a folder (working directory) with the .sqlite file.

Then open the *PowerShell* (for Windows) or *Terminal* (Mac OS), and navigate to the folder containing the .py file.

Type `python TimeMotionGUI_v7.py` (here I am using TimeMotionGUI_v7.py as an example), and you'll see the interface as following.
![GUI layout](Plots/TimeMotionGUI_v7.png)

# Using the GUI
1. To load the data, using the `Load file` button. If the target .sqlite file is in the same folder as the .py, it'll be loaded as default.  
**You may want to read the log appeared in the PowerShell/Terminal window for extra information**  
2. (Optional) Press `Show the Observers' Record` to see the observers' record. (It's just a summary for the observers, no further analysis included at this moment).  
3. Press `Show the Physicians' record` to see the physicians' record. This step is required if you want to look at the record of certain physician. The figure and a .csv file will be generated in the working directory for future use.  
4. You can select one certain `Physician`, a certain `Year` (`Month` doesn't do anything), then press the `Show time` button to see the record for that physician. **IMPORTANT**: the figure will always be saved in the working directory, the actual data used for plotting the figure can be saved in a .csv file if you check `Save data` box. (The physician and observer data will always be saved in a .csv file, though you can only access it after you close the GUI)  
5. (Optional) You can input a `Patient ID` and then press `Show time` to see the record for that patient. **IMPORTANT**: you need to remove the patient id so that the other feather would work.  
6. You can also select a physician, and one task type, then press `Show time` to see the record for that physician and that task type. (Note, the `Year` won't do anything if you select a task type) Because several plots will be made, they are saved in your working directory.  
7. By selecting a `visit type`, the `Select Physician` and `Year` won't work anymore. You can press `Show Time By Visit Type` to see the record for certain visit type together with certain task type. Similarly as step 6, several plots will be made in your working directory. (This is probably the most important function of this GUI)  
8. (Optional) You may also write a simple SQL query and `Execute` it. The result will be shown in the PowerShell/Terminal window.


