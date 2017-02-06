import yaml

class Config(object):
  def __init__(self):
    # somehow construct the object using the yaml
    # http://stackoverflow.com/questions/19439765/is-there-a-way-to-construct-an-object-using-pyyaml-construct-mapping-after-all-n
    # http://pyyaml.org/wiki/PyYAMLDocumentation#Loader
    pass
  

def main():
  raw_cfg = open('../stimulus-config/test.yml')
  cfg = yaml.safe_load(raw_cfg)
  raw_cfg.close()

  print(cfg)

if __name__ == '__main__':
  main()
