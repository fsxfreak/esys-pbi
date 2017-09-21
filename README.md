# esys-pbi
Experimental system synchronizing OpenBCI EEG and EKG, pupillabs and theeyetribe eyetrackers, with stimulus from PsychoPy through LSL.

# SETUP
1. Download and install [Python](https://www.python.org/downloads/) (version 2)
2. Download and install [PsychoPy](http://psychopy.org/installation.html) Unfortunately, python3 is not supported here yet.
3. Install Python modules (automatic installation): 
   * Go to 'esys-pbi' folder on any command line terminal (eg. CommandPrompt on Windows)
   * Type ```pip install -r requirements.txt```
4. Download or clone [esys-pbi repo](https://github.com/fsxfreak/esys-pbi.git)


## Dependencies
* See requirements.txt for pip depends. Install using pip2, and run using python2.
* PupilLabs - See [pupil-depends](https://github.com/pupil-labs/pupil/wiki/Dependencies-Installation-Linux)
* PsychoPy - Unfortunately, python3 is not supported here yet.
* theeyetribe c++ lib, I assume it's been installed into the path, 
  ```/usr/local/lib``` and include files into 
  ```/usr/local/include/tet```
  
## OpenBCI Setup and Device Management
  1. Download the appropriate [Virtual COM Port Driver](http://www.ftdichip.com/Drivers/VCP.htm) for OpenBCI USB dongle 
  2. Plug in the dongle and run the installer according to the instructions [here](https://learn.sparkfun.com/tutorials/how-to-install-ftdi-drivers/windows---in-depth) (for Windows) 

  3. With USB dongle still plugged in, open ```Device Manager```. Under ```Ports (COM & LPT)``` find a ```USB Serial Port``` listing with ```(COM_)```
  4. Change the port number in 'capture_bci.py', line 21. 
 
 ## Changing parameters to live-streaming signal graph 
  1. To change how often the graph updates streaming data: see line 78 to change the number of samples (calcuated using the desired sammpling frequency) to be displayed before graph updates.
  2. To change the window of display for live-streaming data: see line 95 to change the number of samples (caculated using the desired sampling frequency) to be shown on the graph during a particular viewing window. (currently set to show up to 2 s = 512 samples of data at a time)
  3. To change the y-axis limits on the display: see line 87. The first parameter (ie 0) sets the lowest y-limit and the second parameter sets the highest y-limit (ie 10). If you would like to set your own y-limits instead of autoscaling the graph, uncomment line 87 and comment line 86. 
  4. To change the title, x and y-axes labels on the display: see lines 40-42. 
  5. To change the set of data to be graphed on the display: see line 69-73. The channel holding the array of data you want to graph should be passed into the 'abs()' function in line 69. You can also change line 68 to print out the data values from the desired channel you want to graph, if you want to see what these values are. (currently, the desired EEG data to be graphed is stored in 'self.sample[3]', which has been divided by 1000 to scale values to mV as seen in line 69.) Be sure to change the parameters (ie, change "self.sample[3]/1000" to the name of the array of data you want, and scale the data if you choose to do so) in lines 71-73 to modify the autoscaling of the graph. 
  
   * reference code: all graphing instructions can be found in graph_matplotlib.py, lines 20-124. 
  
 
## Trial Settings
* All changes to trial parameters can be done in the ```test.yaml``` file in ```esys-pbi\stimulus-config``` directory.
* Stimuli for a specific trial type must be stored in a folder in the ```esys-pbi\src\stimuli``` directory
* All stimuli in a folder will be displayed except for the last file. The last file is a place holder for a chosen fixation stimuli (reference code: display_stimuli.py lines 33 to 42) 

## Data Storage
### Location
* A ```recorded_data``` folder will be created in ```esys-pbi\src``` directory. 
* ```BCI``` subfolder will be created in ```esys-pbi\src\recorded_data``` to store any data from OpenBCI.
* Sample file names: 'data-0.csv', 'data-1.csv'
* Reference code: capture_bci.py lines 92 to 113
### Additional Information
* Data will be saved in a file at the end of the experiment terminating normally.
* End the experiment early by pressing ```Ctrl-C``` or closing the command window and data will be saved automatically. 
* Data currently **DOES NOT** get automatically saved during a shutdown or other power outage event. 

## Experiment Hardware Setup
### Switching on OpenBCI
1. Set knob on USB dongle to ```GPIO-6``` and not ```RESET```
  <img src="/images/Dongle_connection.JPG" width="300" height="300">
  
2. Set knob on OpenBCI board to ```PC```
  <img src="/images/BCI_board.JPG" width="400" height="300">

### Attaching Electrodes
* the black cable is ground-- place on the forehead or boney area. 
* the white cable is the reference electrode, place on the collarbone. 
* the green cable will be streaming data into the array self.sample[3]-- place this electrode over the heart. 

# Running the Experiment
1. Open a command-line interpreter like "Command Prompt" on Windows
2. Navigate to the location "experiment.py" is stored (path: ```esys-pbi/src```). For instance, type ```cd Desktop/esys-pbi/src``` and hit Enter. 
3. Ensure changes to experiment settings have been made. (Refer to Trial Settings above)
4. To run the experiment type: ```python experiment.py``` and hit Enter.  

  

  
  

