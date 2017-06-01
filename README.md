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
 *look at the device manager to find the appropriate COM port. Change the port number for your device in 'capture_bci.py', line 21. 
 
## Changing Parameters of fixation
All changes to the fixation parameters can be done in the ```test.yaml``` file. 

## Data Storage
* A ```data``` folder will be created in ```esys-pbi\src``` directory. 
* ```BCI``` subfolder will be created in ```esys-pbi\src\data``` to store any data from OpenBCI.
* Sample file names: 'data-0.csv', 'data-1.csv'
* Reference code: capture_bci.py lines 92 to 113

  

  
  

