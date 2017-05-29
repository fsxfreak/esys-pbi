from pylsl import StreamInlet, resolve_byprop, local_clock, TimeoutError
from pylsl import StreamInfo, StreamOutlet
import numpy as np
import time


LSL_STREAM_NAME = 'psychopy'

LSL_BCI_STREAM_NAME = 'bci'
LSL_BCI_NUM_CHANNELS = 2
LSL_BCI_SAMPLE_RATE = 0 #

def setup():
  # setup LSL
  global outlet
  streams = resolve_byprop('name', LSL_STREAM_NAME, timeout=5)
  '''
  try:
  inlet = StreamInlet(streams[0])
  except IndexError:
  raise ValueError('Make sure stream name="%s", is opened first.'
  % LSL_STREAM_NAME)
  '''
  running = True
  
  info = StreamInfo(LSL_BCI_STREAM_NAME, 'eeg',
                          LSL_BCI_NUM_CHANNELS, LSL_BCI_SAMPLE_RATE, 'float32', 'uid2')
  outlet = StreamOutlet(info)
  
  print('lsl stream has been setup')

def generate():
  #x = 0
  while True:
    x = np.random.uniform(0, 1)
    fx = np.sin(x)
    outlet.push_sample([fx,x])
    time.sleep(0.01)
    #x = x + 1
def start():
  setup()
  generate()

def main():
  start()
  

if __name__ == '__main__':
  main()

