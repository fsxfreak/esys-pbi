from pylsl import StreamInlet, resolve_byprop, local_clock, TimeoutError
from pylsl import StreamInfo, StreamOutlet
from bci import open_bci_v3 as bci

import signal, sys, os, time, csv
import serial
import threading
import win32api as win
board = None
samples_lock = threading.Lock()

class Board(object):
  LSL_STREAM_NAME = 'psychopy'

  LSL_BCI_STREAM_NAME = 'bci'
  LSL_BCI_NUM_CHANNELS = 8
  LSL_BCI_SAMPLE_RATE = 0 #

  def __init__(self):
    # check device manager for correct COM port.
    self.board = bci.OpenBCIBoard(port='COM3', filter_data=True,
                                  daisy=False)

    # setup LSL
    streams = resolve_byprop('name', self.LSL_STREAM_NAME, timeout=2.5)
    try:
      self.inlet = StreamInlet(streams[0])
    except IndexError:
      raise ValueError('Make sure stream name="%s", is opened first.'
          % LSL_STREAM_NAME)

    self.running = True
    self.samples = []

    info = StreamInfo(self.LSL_BCI_STREAM_NAME, 'eeg', 
        self.LSL_BCI_NUM_CHANNELS, self.LSL_BCI_SAMPLE_RATE, 'float32', 'uid2')
    self.outlet = StreamOutlet(info)

  # LSL and BCI samples are synchronized to local_clock(), which is the
  # runtime on this slave, not the host
  def _record_lsl(self):
    while self.running:
      sample, timestamp = self.inlet.pull_sample(timeout=5)

      # time correction to sync to local_clock()
      try:
        if timestamp is not None and sample is not None:
          timestamp = timestamp + self.inlet.time_correction(timeout=5) 

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

    self.outlet.push_sample(data)

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
    self.bci_thread.join(5)
    self.lsl_thread.join(5)
    print('Joined threads, now outputting BCI data.')

    i = 0
    folder = '\\recorded_data\\BCI'
    folder_path = os.getcwd() + folder
    #new folders recorded_data/BCI will be created in current directory (where experiment.py is saved) if they don't exist
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)

    #file_path = os.path.normpath(folder_path + 'data-%s.csv')
    file_path = folder_path + '\\data-%s.csv'

    while os.path.exists(file_path % i):
      i += 1

    # csv writer with stim_type, msg, and timestamp, then data
    with open(file_path % i, 'w+') as f:
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
  try:
    global board
    board = Board()
    print('init board')
  except:
    if queue is not None:
      queue.put('FAIL')

def start():
  board.capture()

def stop(queue):
  board.export_data()
  print('Finished exporting data.')
  queue.put('SAVED_BCI')
  #os._exit(0) # dirty, but it's ok because everything is already cleaned up

def sigint_handler(signal, frame):
  stop()

def sigterm_handler(signal, frame):
  stop()

def main():
  signal.signal(signal.SIGINT, sigint_handler)
  signal.signal(signal.SIGTERM, sigterm_handler)
  load(queue=None)
  start()

  signal.pause()

def win_handler(dwCtrlhandler):
  if dwCtrlhandler in (0,2,6):
    return 1
  #return 0

def begin(queue, event=None):
  signal.signal(signal.SIGINT, sigint_handler)
  signal.signal(signal.SIGTERM, sigterm_handler)
 
  if sys.platform == 'win32':
    win.SetConsoleCtrlHandler(win_handler,1)
  
  load(queue)
  queue.put('CONNECTED')
  start()

  try:
    # linux signal handling
    while True:
      signal.pause()
  except AttributeError:
    # signal.pause() not implemented on windows
    while not event.is_set():
      time.sleep(1)
    print('event was set in bci, stopping')
    stop(queue)

if __name__ == '__main__':
  main()
