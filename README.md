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
* PupilLabs - See (pupil-depends)[https://github.com/pupil-labs/pupil/wiki/Dependencies-Installation-Linux]
* PsychoPy - Unfortunately, python3 is not supported here yet.
* theeyetribe c++ lib, I assume it's been installed into the path, 
  ```/usr/local/lib``` and include files into 
  ```/usr/local/include/tet```
  
## Device Management
 * look at the device manager to find the appropriate COM port. Change the port number for your device in 'capture_bci.py', line 21. 
 
 ## Changing parameters of live-streaming signal display 
  1. Editing the frequency at which display updates streaming data: see line 72 to change the number of samples (given a particular sammpling frequency) to be displayed before graph updates.
  2. Editing the window of display for live-streaming data: see line 89 to change the number of samples (given a particular sampling frequency) to be shown on the graph during a particular viewing window. 
  3. Changing the y-axis limits on the display: see line 81. The first parameter (ie 0) sets the lowest y-limit and the second parameter sets the highest y-limit (ie 10). 
  4. Changing the title, x and y-axes labels on the display: see lines 38-40. 
  5. Changing the set of data to be graphed on the display: see line 67. The channel holding the data that is desired to be graphed should be passed into the 'abs()' function. (ex: currently, the desired EEG data to be graphed is stored in 'self.sample[3]', which has been divided by 1000 to scale values to mV.) 
  
   * reference code: all graphing instructions can be found in graph_matplotlib.py, lines 52-117. 
  
 
## Trial Settings
* All changes to trial parameters can be done in the ```test.yaml``` file in ```esys-pbi\stimulus-config``` directory.
* Stimuli for a specific trial type must be stored in a folder in the ```esys-pbi\src\stimuli``` directory
* All stimuli in a folder will be displayed except for the last file. The last file is a place holder for a chosen fixation stimuli (reference code: display_stimuli.py lines 33 to 42) 

## Data Storage
* A ```data``` folder will be created in ```esys-pbi\src``` directory. 
* ```BCI``` subfolder will be created in ```esys-pbi\src\data``` to store any data from OpenBCI.
* Sample file names: 'data-0.csv', 'data-1.csv'
* Reference code: capture_bci.py lines 92 to 113

  

  
  

