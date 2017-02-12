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

#to store data belonging to each experiment and type of stimuli
def recordData(data, f):
#open file to write into
#    f_data = str(data)[1:-1]
    f_data = ' '.join(map(str,data)) + ' '+ str(datetime.now())
    f.write(f_data)
    f.write("\n")

def recordStimulus(details):
    s_data = ""
    s = open('Stimulus %s', %str(datetime.now()),'w')
    s_data = ' '.join(map(str,details))

#each data set is added on to the variable "channels"
def handleSample(sample):
    channels = sample.channel_data[0:NUM_CHANNELS]   
    data.append(channels)
 #   data = [0, 1, 2, 3, 4, 5, 6, 7, 8] 
#   print(channels)
    f_data = ""
    f = open('Run4','w')
    recordData(data, f, f_data)
    recordStimulus(details)
    
#initialize board, set it up to start streaming
def main():
    #while stimuli_running == True:
        board = bci.OpenBCIBoard(port='/dev/ttyUSB0', filter_data=True, daisy=False)
        print (board.getNbEEGChannels(), "EEG channels and", 
                board.getNbAUXChannels(), "AUX channels at", 
                board.getSampleRate(), "Hz.")
        board.start_streaming(handleSample)
        #sample = True
        #handleSample(sample)

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
