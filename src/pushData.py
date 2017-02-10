import time
import pylsl
import open_bci_v3 as bci

#from random import random as rand
from pylsl import StreamInfo, StreamOutlet
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual, core, sound 


NUM_CHANNELS = 8
SAMP_RATE = 100

info = StreamInfo('OpenBCI', 'EEG', NUM_CHANNELS, SAMP_RATE, 'float32', 'myuid34234')
outlet = StreamOutlet(info)

#funtion call to start displaying images
#def displayStimuli
# for file in os.listdir('directory'):
# for i in range(0,len(images)):


# def display(files, .....):
#   ex: file_name = ['/dir/dir2/img.png']

window = visual.Window([512, 512])

imageIndex = 0
for imageIndex in range(len(file_name)):
    stimulis = file_name[imageIndex]
    showStim = visual.ImageStim(window, stimulis)
    #visual.ImageStim(window, image = stimulus)
    showStim.draw([window])
    window.flip()
    core.wait(2.0) 
    #stimuli_running = True
    
    #if statement to differentiate between images and audio files
    if stimulis.lower().endswith(('.png', '.jpg', 'tif', .'gif'))
        stimuli_type = 'images'
    elif stimulis.lower().endswith(('.mp3', '.wma', '.wav'))
        stimuli_type = 'audio'

    #1st element: type of stimuli, 2nd element: filename, 3rd element: wait time
    mysample = [stimuli_type, stimulis, time_placeholder]
    print("now sending data...")
    outlet.push_sample(mysample)                
    
    time.sleep(0.01)
 


#while True:
#mysample = []

#-------------------#

''' import open_bci_v3 as bci

NUM_CHANNELS = 8
data = []

def handleSample(sample):
    channels = sample.channel_data[0:NUM_CHANNELS]
    data.append(channels)

    print(channels)

def main():
    board = bci.OpenBCIBoard(port='/dev/ttyUSB0', filter_data=True, daisy=False)
    print (board.getNbEEGChannels(), "EEG channels and", 
            board.getNbAUXChannels(), "AUX channels at", 
            board.getSampleRate(), "Hz.")

    #data.append([])

    board.start_streaming(handleSample)

    #while True:
    pass

if __name__ == '__main__':
    main(

#----------------------#

import pylsl
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual, core, sound 

def main():
    win = visual.Window([512, 512])                 #defines the frame to show

    # writes text to win on the back buffer
    message = visual.TextStim(win, text='ehllo') 
    message.setAutoDraw(True)
    win.flip() # displays back buffer to front

    core.wait(1.0)

    for i in xrange(0, 10):
      if i % 2:
        message.setText('odd')
      else:
        message.setText('even')

      win.flip()
      core.wait(1.0)

  sound.Sound('stimulus-400.wav').play()
  core.wait(2.0)

if __name__ == '__main__':
    main( '''
