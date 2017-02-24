from pylsl import StreamInlet, resolve_byprop, local_clock, TimeoutError
from bci import open_bci_v3 as bci

import signal, sys, os
import serial
import threading

# useful LSL constants
import display_stimuli as ds

board = None

class Board(object):
  def __init__(self):
    self.board = bci.OpenBCIBoard(port='/dev/ttyUSB0', filter_data=True,
                                  daisy=False)

    # setup LSL
    streams = resolve_byprop('name', ds.Stimuli.LSL_STREAM_NAME, timeout=2.5)
    try:
      self.inlet = StreamInlet(streams[0])
    except IndexError:
      raise ValueError('Make sure stream name="%s", is opened first.'
          % ds.Stimuli.LSL_STREAM_NAME)

    self.running = True
    self.samples = []

  # LSL and BCI samples are synchronized to local_clock(), which is the
  # runtime on this slave, not the host
  def _record_lsl(self):
    while self.running:
      sample, timestamp = self.inlet.pull_sample(timeout=0)

      # time correction to sync to local_clock()
      try:
        if timestamp is not None and sample is not None:
          timestamp = timestamp + self.inlet.time_correction(timeout=0) 
          self.samples.append(('STIM', timestamp, sample))
      except TimeoutError:
        pass

    print('closing lsl')
    self.inlet.close_stream()

  def _bci_sample(self, sample):
    NUM_CHANNELS = 8
    data = sample.channel_data[0:NUM_CHANNELS]
    self.samples.append(('BCI', local_clock(), data))

  def _record_bci(self):
    try:
      self.board.start_streaming(self._bci_sample)
    except:
      print('Serial exception. Hopefully you\'re terminating.')
      

  def capture(self):
    self.bci_thread = threading.Thread(target=self._record_bci)
    self.lsl_thread = threading.Thread(target=self._record_lsl)
    self.bci_thread.start()
    self.lsl_thread.start()

  def export_data(self):
    self.board.stop()
    self.board.disconnect()
    self.running = False
    print('time to stop running')

    self.bci_thread.join()
    self.lsl_thread.join()

    f = open('data.txt', 'w+')

    for sample in self.samples:
      f.write(str(sample))
      f.write('\n')

    f.close()

  def __str__(self):
    return '%s EEG channels' % board.getNbEEGChannels()

  def __del__(self):
    self.board.disconnect()
    self.inlet.close_stream()

def load():
  global board
  board = Board()

def start():
  board.capture()

def stop():
  board.export_data()
  os._exit(0) # dirty, but it's ok because everything is already cleaned up

def sigint_handler(signal, frame):
  stop()

def sigterm_handler(signal, frame):
  stop()

def main():
  signal.signal(signal.SIGINT, sigint_handler)
  signal.signal(signal.SIGTERM, sigterm_handler)
  load()
  start()

  signal.pause()

if __name__ == '__main__':
  main()
