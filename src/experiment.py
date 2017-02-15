import sys

import capture_stream as cap
import display_stimuli as disp 

def main():
  cap.load()
  ds.load(sys.argv[1]) 

  cap.start()
  sys.wait(1.0)
  ds.start()

  input('press enter to terminate')
  cap.stop()
  ds.stop()

if __name__ == '__main__':
  main()
