import yaml
import re
import random

from os import listdir
from os.path import isfile, join

class TrialConfig(object):
  def __init__(self, *args, **kwargs):
    # auto build config from dictionary. See stimulus_config/test.yml for
    # expected attributes of each trial object in the trials array
    for dictionary in args:
      for key in dictionary:
        setattr(self, key, dictionary[key])
    for key in kwargs:
      setattr(self, key, kwargs[key])

    self.files = listdir(self.stimuli_folder)
    # need exception handling
    self.files.sort(key=lambda filename: int(re.sub(r'_.*', '', filename)))

  def __str__(self):
    return self.stimuli_folder

class ExperimentConfig(object):
  def __init__(self, name, resolution, trials, trial_order, ordering):
    self.name = name

    self.resolution = resolution

    self.trials = {}
    for trial_name in trials:
      self.trials[trial_name] = TrialConfig(trials[trial_name])

    self.trial_order = []
    for trial in trial_order:
      tokens = trial.split()
      for j in range(0,len(tokens),2):
        trial_name = tokens[j]
        if len(tokens) > 1:
          freq = tokens[j+1]
          for i in range(int(freq)):
            self.trial_order.append(trial_name)
        #self.trial_order.append(trial_name)
    self.ordering = ordering 

    if self.ordering == 'random':
      print('random order')
      random.shuffle(self.trial_order)

  def __str__(self):
    return ('%s\n\tTrials: %s\n\tOrder: %s, Ordering type: %s' %
        (self.name, self.trials, self.trial_order, self.ordering))

def experiment_config_construct(loader, node):
  instance = ExperimentConfig.__new__(ExperimentConfig)
  yield instance
  state = loader.construct_mapping(node, deep=True)
  instance.__init__(**state)

yaml.add_constructor(u'!ExperimentConfig', experiment_config_construct)

def create_config(filename):
  raw_cfg = open(filename)
  cfg = yaml.load(raw_cfg)
  raw_cfg.close()

  # sort within class later

  return cfg

def main():
  cfg = create_config('../stimulus-config/test.yml')
  '''
  refer to /stimulus_config/test.yml on how to use this object
  cfg.trials['trial_name'] object contains an additional parsed field,
  cfg.trials['trial_name'].files which is all the files displayed by this
  trial
  '''
  print(cfg)

if __name__ == '__main__':
  main()
