from pylsl import StreamInlet, resolve_byprop, local_clock, TimeoutError

import signal, sys, os, time, csv
import serial
import threading

graph = None

class Graph(object):
  def __init__(self):
    streams = resolve_byprop('name', 'bci', timeout=2.5)
    try:
      self.inlet = StreamInlet(streams[0])
    except IndexError:
      raise ValueError('Make sure stream name=bci is opened first.')
    
    self.running = True

  def _graph_lsl(self):
    while self.running:
      sample, timestamp = self.inlet.pull_sample(timeout=5)

      # time correction to sync to local_clock()
      try:
        if timestamp is not None and sample is not None:
          timestamp = timestamp + self.inlet.time_correction(timeout=5) 

        # TODO Place graphing stuff here
        print(sample, timestamp)

      except TimeoutError:
        pass

    print('closing graphing utility')
    self.inlet.close_stream()

  def start(self):
    self.lsl_thread = threading.Thread(target=self._graph_lsl)
    self.lsl_thread.start()
  
  def stop(self):
    self.running = False
    self.lsl_thread.join(5)
    # Place any graphing termination or cleanup here

def load(queue):
  global graph
  graph = Graph()
  print('init graph')

def start():
  graph.start()

def stop():
  graph.stop()
  print('Stopping graphing.')
  os._exit(0) # dirty, but it's ok because everything is already cleaned up

def sigint_handler(signal, frame):
  stop()

def sigterm_handler(signal, frame):
  stop()

def main():
  signal.signal(signal.SIGINT, sigint_handler)
  signal.signal(signal.SIGTERM, sigterm_handler)
  load(queue=None)
  start()

  try:
    signal.pause()
  except AttributeError:
    while True:
      time.sleep(1)

  stop()

def begin(queue, event=None):
  signal.signal(signal.SIGINT, sigint_handler)
  signal.signal(signal.SIGTERM, sigterm_handler)

  load(queue)
  start()

  try:
    while True:
      signal.pause()
  except AttributeError:
    # signal.pause() not implemented on windows
    while not event.is_set():
      time.sleep(1)

    print('event was set, stopping')
    stop()

if __name__ == '__main__':
  main()
