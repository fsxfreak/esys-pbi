from pylsl import StreamInlet, resolve_byprop, local_clock, TimeoutError
from bci import open_bci_v3 as bci

import signal, sys, os, time, csv
import serial
import threading

# useful LSL constants
import display_stimuli as ds

board = None
samples_lock = threading.Lock()

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

          samples_lock.acquire()
          self.samples.append(('STIM', timestamp, sample))
          samples_lock.release()

      except TimeoutError:
        pass

    print('closing lsl')
    self.inlet.close_stream()

  def _bci_sample(self, sample):
    NUM_CHANNELS = 8
    data = sample.channel_data[0:NUM_CHANNELS]

    samples_lock.acquire()
    self.samples.append(('BCI', local_clock(), data))
    samples_lock.release()

  def _record_bci(self):
    try:
      self.board.start_streaming(self._bci_sample)
    except:
      print('Got a serial exception. Expected behavior if experiment ending.')
      

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
    self.bci_thread.join(5)
    self.lsl_thread.join(5)
    print('Joined threads, now outputting data.')

    i = 0
    while os.path.exists("data/data-%s.xml" % i):
      i += 1

    # csv writer with stim_type, msg, and timestamp, then data
    with open('data/data-%s.csv' % i, 'w+') as f:
      writer = csv.writer(f)
      writer.writerow(('Signal Type', 'Msg', 'Time', 'Channel 1', 'Channel 2', 'Channel 3', 'Channel 4', 'Channel 5', 'Channel 6', 'Channel 7', 'Channel 8' ))
      for sample in self.samples:
        signal_type, timestamp, datas = sample
        out = (signal_type, 'msg', timestamp)
        for data in datas:
          out = out + (data,)
        writer.writerow(out)

  def __str__(self):
    return '%s EEG channels' % board.getNbEEGChannels()

  def __del__(self):
    self.board.disconnect()
    self.inlet.close_stream()

def load(queue):
  global board
  try:
    board = Board()
  except:
    if queue is not None:
      queue.put('FAIL')

def start():
  board.capture()

def stop():
  board.export_data()
  os._exit(0) # dirty, but it's ok because everything is already cleaned up

def sigint_handler(signal, frame):
  stop()

def sigterm_handler(signal, frame):
  print('BCI got terminate signal, now terminating threads.')
  stop()

def main():
  signal.signal(signal.SIGINT, sigint_handler)
  signal.signal(signal.SIGTERM, sigterm_handler)
  load()
  start()

  signal.pause()

def begin(queue):
  signal.signal(signal.SIGTERM, sigterm_handler)

  load(queue)
  queue.put('CONNECTED')
  start()

  signal.pause()

if __name__ == '__main__':
  main()
