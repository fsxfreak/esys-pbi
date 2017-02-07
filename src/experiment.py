import yaml

class TrialConfig(object):
  def __init__(self, *args, **kwargs):
    # auto build config from dictionary. See stimulus_config/test.yml for
    # expected attributes of each trial object in the trials array
    for dictionary in args:
      for key in dictionary:
        setattr(self, key, dictionary[key])
    for key in kwargs:
      setattr(self, key, kwargs[key])

  def __str__(self):
    return (self.__dict__)

class ExperimentConfig(object):
  def __init__(self, name, trials, trial_order):
    self.name = name

    self.trials = {}
    for trial_name in trials:
      self.trials[trial_name] = TrialConfig(trials[trial_name])

    self.trial_order = trial_order

  def __str__(self):
    return ('%s\n\tTrials: %s\n\tOrder: %s' %
        (self.name, self.trials, self.trial_order))

def config_construct(loader, node):
  instance = ExperimentConfig.__new__(ExperimentConfig)
  yield instance
  state = loader.construct_mapping(node, deep=True)
  instance.__init__(**state)

def main():
  yaml.add_constructor(u'!ExperimentConfig', config_construct)

  raw_cfg = open('../stimulus-config/test.yml')
  cfg = yaml.load(raw_cfg)
  raw_cfg.close()

  print(cfg)

  # TODO sort file order by numeric, before an underscore

if __name__ == '__main__':
  main()
