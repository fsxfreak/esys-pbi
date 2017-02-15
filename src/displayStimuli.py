import pylsl

from pylsl import StreamInfo, StreamOutlet
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual, core, sound 

import esys_cfg

stim = None

class Stimuli(object):
  LSL_STREAM_NAME = 'psychopy'
  LSL_STREAM_TYPE = 'marker'
  LSL_NUM_CHANNELS = 2
  LSL_SAMPLE_RATE = 0 # irregular sample rate. push whenever there is data.

  def __init__(self, cfg_filename):
    # load in the cfg
    self.cfg = esys_cfg.create_config(cfg_filename)

    # psychopy setup
    self.window = visual.Window([1024, 512])

    # preload all of stimuli
    self.loaded_stims = {}
    for trial_name, trial in self.cfg.trials.iteritems():
      stimuli_type = trial.stimuli_type
      path_prefix = '%s/' % trial.stimuli_folder

      if stimuli_type == 'images':
        self.loaded_stims[trial_name] = [ visual.ImageStim(self.window, 
                                            '%s%s' % (path_prefix, stim_file)) 
                                          for stim_file in trial.files ]
      elif stimuli_type == 'sounds':
        self.loaded_stims[trial_name] = [ sound.Sound(
                                            '%s%s' % (path_prefix, stim_file))
                                          for stim_file in trial.files]
      else:
        print('Unsupported stimuli_type: %s' % stimuli_type)
        raise ValueError 

    # setup LSL 
    info = StreamInfo(self.LSL_STREAM_NAME, self.LSL_STREAM_TYPE,
        self.LSL_NUM_CHANNELS, self.LSL_SAMPLE_RATE, 'string', 'uid1')
    self.outlet = StreamOutlet(info)

  def signal(self, stim, msg):
    self.outlet.push_sample([str(stim), msg])

  def do_image_stimuli(self, stim, duration_ms):
    stim.draw(self.window)
    self.window.flip()

    # convert to seconds by division
    core.wait(duration_ms / 1000.0)

  def do_sound_stimuli(self, stim, duration_ms):
    stim.play()

    core.wait(duration_ms / 1000.0)

  def display(self):
    for trial_name in self.cfg.trial_order:
      trial = self.cfg.trials[trial_name]

      for loaded_stim in self.loaded_stims[trial_name]:
        self.signal(loaded_stim, 'pre')

        if trial.stimuli_type == 'images':
          self.do_image_stimuli(loaded_stim, trial.duration_time_ms)
        elif trial.stimuli_type == 'sounds':
          self.do_sound_stimuli(loaded_stim, trial.duration_time_ms)

        # post signal
        self.signal(loaded_stim, 'post')

  def __str__(self):
    return ('Pushing on channel %s for experiment %s.' 
            % (self.LSL_STREAM_NAME, self.cfg.name))

def load(cfg_filename):
  stim = Stimuli(cfg_filename)

def start():
  '''
  Precondition: load(cfg_file) must have been called prior to calling
                this function, to preload all stimuli.
  '''
  if stim is None:
    print('Call the load(cfg_filename) function first to initialize stim.')
    raise TypeError

  stim.display()

def stop():
  if stim is None:
    print("No window to close! The experiment hasn't even start()ed.")
    raise TypeError

  stim.window.close() # TODO cleaner close

def main():
  stim = Stimuli('../stimulus-config/test.yml')
  stim.display()

if __name__ == '__main__':
  main()
