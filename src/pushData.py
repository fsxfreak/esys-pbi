import time
import pylsl
import bci.open_bci_v3 as bci


#from random import random as rand
from pylsl import StreamInfo, StreamOutlet
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual, core, sound 

import esys_cfg

NUM_CHANNELS = 8
SAMP_RATE = 100

info = StreamInfo('OpenBCI', 'EEG', NUM_CHANNELS, SAMP_RATE, 'float32', 'myuid34234')
outlet = StreamOutlet(info)

window = visual.Window([512, 512])

cfg = esys_cfg.create_config('../stimulus-config/test.yml')
print(cfg.trial_order)

for element in cfg.trial_order:               #loop through all elements in array trial_order
  trials['one']                               #trial is a dictionary, 'one' is a keyword  
  
imageIndex = 0
for imageIndex in range(len(cfg.trials[element].files)):
  for element in cfg.trial_order: #loop through all elements in array trial_order
    imageIndex = 0
    for imageIndex in range(len(cfg.trials[element].files)):

      stimulis = cfg.trials[element].stimuli_folder + '/' + cfg.trials[element].files[imageIndex]
      showStim = visual.ImageStim(window, stimulis)
      
      showStim.draw(window)
      window.flip()
      core.wait(2.0) 
       
      #1st element: stimuli type; 2nd element: filename, 3rd element: wait time
      mysample = [stimuli_type, stimulis, time_placeholder]         

      outlet.push_sample(mysample)                
      print("now sending data...")
      if stimulis.lower().endswith(('.png', '.jpg', 'tif', .'gif'))
          stimuli_type = 'images'
      elif stimulis.lower().endswith(('.mp3', '.wma', '.wav'))
          stimuli_type = 'audio'

      #1st element: type of stimuli, 2nd element: filename, 3rd element: wait time
      mysample = [stimuli_type, stimulis, time_placeholder]
      print("now sending data...")
      outlet.push_sample(mysample)                
      '''

      time.sleep(0.01)

