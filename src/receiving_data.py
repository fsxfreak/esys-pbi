# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 13:24:38 2017

@author: Kokila
"""
#Do I need to use StreamInfo function for anything?
#psychopy.data.ExperimentHandler useful here?

from datetime import datetime
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_stream
#stimuli_running = True

# data from Krista
# [ 'stimuli_type', 'filename', 'duration' ]
# stimuli_type = 'audio' | 'visual'
# filename = stimulus filename
# duration = time that stimulus is displayed
# timestamp

# krista_data1
# krista_data2
# bci_data1
# ..
# bci_datan

# bci_data.raw
# include only bcidata

# stimulus.raw
# include only the krista_data


#initializing number of channels of OpenBCI to be used
#create empty array to receive data
NUM_CHANNELS = 8
data = []
bci_dataFile = ""
bci_stimulusFile = "" 

#to store list of data arrays from each channel set
#def recordData(data):
#  all_data = all_data.append(data)
#  all_data = all_data.append(str(datetime.now()))
   
#to store data belonging to each experiment and type of stimuli    
def recordStimulus(details):
    details.append(str(datetime.now()))

#each data set is added on to the variable "channels"
def handleSample(sample):
    channels = sample.channel_data[0:NUM_CHANNELS]
    channels.append(str(datetime.now()))
    data.append(channels)
   # recordData(data)#to store data belonging to each experiment and type of stimuli
    recordStimulus(details)

def saveFile():
for i in len(data):
    bci_dataFile = ' '.join(map(str,data(i)))
    f.write(bci_dataFile)
    f.write("\n")

bci_stimulusFile = ' '.join(map(str(details)))
f.write(bci_stimulusFile)
f.write("\n")

def stop():
  running = False
  saveFile()
  board.disconnect()
    
#initialize board, set it up to start streaming
def main():
    board = bci.OpenBCIBoard(port='/dev/ttyUSB0', filter_data=True, daisy=False)
    print (board.getNbEEGChannels(), "EEG channels and", 
    board.getNbAUXChannels(), "AUX channels at", 
    board.getSampleRate(), "Hz.")
    running = true
    while running == true:
         board.start_streaming(handleSample)

if __name__ == '__main__':
    main()



#receive signal that a stimuli is being presented, stimuli_running = true

#while stimuli_running == true

#   start pushing OpenBCI data (specific to the stimuli) on to the "lab network" using StreamOutlet 

#   open new data file

#   begin reading and recording data from the openBCI with time stamp
#   use StreamInlet function - to get time series data
#   ....needs to have connected outlet in main.py and Krista's generate stimuli function?
#   run disp_data() to get updated with each incoming reading
#   continue recording data for a set amount of time, T

#   or stop recording data when flag == False, (i.e. when stimulus is no longer being shown)
#end

#close data file


## write separate function to display data simultaneously as recordings are being taken: disp_data()
