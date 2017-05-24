# esys-pbi
Experimental system synchronizing OpenBCI EEG and EKG, pupillabs and theeyetribe eyetrackers, with stimulus from PsychoPy through LSL.

## Dependencies
* See requirements.txt for pip depends. Install using pip2, and run using python2.
* PupilLabs - See (pupil-depends)[https://github.com/pupil-labs/pupil/wiki/Dependencies-Installation-Linux]
* Psychopy - Install from (here)[http://psychopy.org/installation.html] Unfortunately, python3 is not supported here yet.
* theeyetribe c++ lib, I assume it's been installed into the path, 
  ```/usr/local/lib``` and include files into 
  ```/usr/local/include/tet```
  
# Device Management
 *look at the device manager to find the appropriate COM port. Change the port number for your device in 'capture_bci.py', line 21. 
 
# Changing Parameters of fixation
  *All changes to the fixation parameters can be done in the test.yaml file. 
  

  
  

