"""
Created on Tue May 09 18:20:29 2017

@author: Krista
"""

import serial # imports the PySerial package
import numpy as np 
import scipy.signal 
import matplotlib.pyplot as plt

numSamples = 0
secondTimes = [] 
processedSig = []
floatProcessedSig = []
floatSecondTimes = []
serialData = []

count = -1

ser = serial.Serial("COM3", 115200) # establish connection between python script and arduino
print ser

userSensor = raw_input("Type 'A' to begin sampling...")
ser.write(userSensor)
ser.readline()  #reads the next line to omit the serial prompt line
ser.readline()  #reads the next line to omit the trash time

#serialData = ser.readline().split("\t")        # reads one line from Serial Monitor into array 'serialData'            

plt.ion()
plt.hold(False)     
lineHandle = plt.plot(floatSecondTimes, floatProcessedSig)
plt.title("Streaming Live EMG Data")
plt.xlabel('Time (s)')
plt.ylabel('Volts')
plt.show()

while(1):
    serialData = ser.readline().split("\t")        # reads one line from Serial Monitor into array 'serialData'   
    secondTimes.append(serialData[0])                         #add time stamps to array 'timeValSeconds'
    floatSecondTimes.append(float(serialData[0])/1000000)     # makes all second times into float from string

    processedSig.append(serialData[6])                           #add processed signal values to 'processedSig'
    floatProcessedSig.append(float(serialData[6]))
    
    count = count + 1
    print(count)
      
    if((count % 20 == 0) and (count != 0)):   #every 20 samples (ie ~ 0.10 s) is when plot updates
      lineHandle[0].set_ydata(floatProcessedSig)
      lineHandle[0].set_xdata(floatSecondTimes)
      #plt.xlim(0, 5)
      plt.xlim(floatSecondTimes[0], floatSecondTimes[-1])
      plt.ylim(0, 0.25)
      plt.pause(0.01)
      
    
    
    if(count >= 399): 
      floatProcessedSig.pop(0)    
      floatSecondTimes.pop(0)

      

        
f.close()
       
      