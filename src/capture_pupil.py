from pylsl import StreamInlet, resolve_byprop, local_clock, TimeoutError
import zmq
from zmq.utils.monitor import recv_monitor_message
import msgpack as serializer

import pupil.pupil_src.capture as pupil_capture
from multiprocessing import Process, Queue

import signal, sys, os, time, csv
import serial
import threading

samples_lock = threading.Lock()

LSL_STREAM_NAME = 'psychopy'
LSL_STREAM_TYPE = 'marker'

pupil_tracker = None

class PupilTracker(object):
  def __init__(self):
    pupil_queue = Queue()
    self.pupil_proc = Process(target=pupil_capture.alternate_launch,
                              args=((pupil_queue), ))
    self.pupil_proc.start()

    while True:
      pupil_msg = pupil_queue.get()
      print(pupil_msg)
      if 'tcp' in pupil_msg:
        self.ipc_sub_url = pupil_msg
      if 'EYE_READY' in pupil_msg:
        break

    context = zmq.Context()
    self.socket = zmq.Socket(context, zmq.SUB)
    monitor = self.socket.get_monitor_socket()

    self.socket.connect(self.ipc_sub_url)
    while True:
      status = recv_monitor_message(monitor)
      if status['event'] == zmq.EVENT_CONNECTED:
        break
      elif status['event'] == zmq.EVENT_CONNECT_DELAYED:
        pass
    print('Capturing from pupil on url %s.' % self.ipc_sub_url)
    self.socket.subscribe('pupil')

    # setup LSL
    streams = resolve_byprop('name', LSL_STREAM_NAME, timeout=2.5)
    try:
      self.inlet = StreamInlet(streams[0])
    except IndexError:
      raise ValueError('Make sure stream name="%s", is opened first.'
          % LSL_STREAM_NAME)

    self.running = True
    self.samples = []

  # LSL and pupil samples are synchronized to local_clock(), which is the
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

    print('closing lsl on the pupil side')
    self.inlet.close_stream()

  def _record_pupil(self):
    while self.running:
      topic = self.socket.recv_string()
      payload = serializer.loads(self.socket.recv(), encoding='utf-8')

      samples_lock.acquire()
      self.samples.append(('pupil', local_clock(), payload['diameter']))
      samples_lock.release()

    print('Terminating pupil tracker recording.')
      
  def capture(self):
    self.pupil_thread = threading.Thread(target=self._record_pupil)
    self.lsl_thread = threading.Thread(target=self._record_lsl)
    self.pupil_thread.start()
    self.lsl_thread.start()

  def export_data(self):
    self.running = False

    self.pupil_thread.join(5)
    self.lsl_thread.join(5)
    print('Joined threads, now outputting pupil data.')

    i = 0
    while os.path.exists("data/pupil/data-%s.csv" % i):
      i += 1

    # csv writer with stim_type, msg, and timestamp, then data
    with open('data/pupil/data-%s.csv' % i, 'w+') as f:
      writer = csv.writer(f)
      writer.writerow(('Signal Type', 'Msg', 'Time', 'Channel 1', 'Channel 2', 'Channel 3', 'Channel 4', 'Channel 5', 'Channel 6', 'Channel 7', 'Channel 8' ))
      for sample in self.samples:
        signal_type, timestamp, datas = sample
        out = (signal_type, 'msg', timestamp)
        for data in datas:
          out = out + (data,)
        writer.writerow(out)

  def __str__(self):
    return 'Pupil tracker listening to %s' % self.ipc_sub_url

  def __del__(self):
    try:
      self.inlet.close_stream()
    except AttributeError:
      raise AttributeError('self.inlet does not exist. Most likely the LSL stimuli stream was not opened yet.')

    self.pupil_proc.terminate()

def load(queue):
  try:
    global pupil_tracker 
    pupil_tracker = PupilTracker()
  except:
    if queue is not None:
      queue.put('FAIL')
    print('failed to initailize pupil process')

def start():
  pupil_tracker.capture()

def stop():
  pupil_tracker.export_data()
  os._exit(0) # dirty, but it's ok because everything is already cleaned up

def sigint_handler(signal, frame):
  stop()

def sigterm_handler(signal, frame):
  print('Pupil got terminate signal, now terminating threads.')
  stop()

def main():
  signal.signal(signal.SIGINT, sigint_handler)
  signal.signal(signal.SIGTERM, sigterm_handler)
  load(queue=None)

  # Required message for subprocess comms
  print('CONNECTED')

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
