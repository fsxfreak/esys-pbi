from pylsl import StreamInlet, resolve_byprop, local_clock, TimeoutError
from pyqtgraph.Qt import QtGui,QtCore
import collections
import numpy as np
import pyqtgraph as pg
import time 
import signal, sys, os, time, csv
import serial
import threading

graph = None

class Graph(object):
  def __init__(self, size=(600,350)):
    streams = resolve_byprop('name', 'bci', timeout=2.5)
    try:
      self.inlet = StreamInlet(streams[0])
    except IndexError:
      raise ValueError('Make sure stream name=bci is opened first.')
    
    self.running = True
    
    self.frequency = 250.0
    self.sampleinterval = (1/self.frequency)
    self.timewindow = 10
    self._bufsize = int(self.timewindow/self.sampleinterval)
    self.dataBuffer = collections.deque([0.0]*self._bufsize,self._bufsize)
    self.timeBuffer = collections.deque([0.0]*self._bufsize,self._bufsize)
    self.x = np.zeros(self._bufsize,dtype='float64')
    self.y = np.zeros(self._bufsize,dtype='float64')
    self.app = QtGui.QApplication([])
    self.plt = pg.plot(title='EEG data from OpenBCI')
    self.plt.resize(*size)
    self.plt.showGrid(x=True,y=True)
    self.plt.setLabel('left','Amplitude','V')
    self.plt.setLabel('bottom','Time','s')
    self.curve = self.plt.plot(self.x,self.y,pen=(255,0,0))
    self.sample=[0.0]
    self.timestamp = 0.0

    #QTimer
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.update)
    self.timer.start(self.sampleinterval)

  def _graph_lsl(self):
    while self.running:
      self.sample, self.timestamp = self.inlet.pull_sample(timeout=5)

      # time correction to sync to local_clock()
      try:
        if self.timestamp is not None and self.sample is not None:
          self.timestamp = self.timestamp + self.inlet.time_correction(timeout=5) 
          
        print(self.sample, self.timestamp)

      except TimeoutError:
        pass

    print('closing graphing utility')
    self.inlet.close_stream()

  def update(self):
    self.dataBuffer.append(self.sample[0])
    self.y[:] = self.dataBuffer
    self.timeBuffer.append(self.timestamp)
    self.x[:] = self.timeBuffer
    self.curve.setData(self.x,self.y)
    self.app.processEvents()

  def start(self):
    self.lsl_thread = threading.Thread(target=self._graph_lsl)
    self.lsl_thread.start()
  
  def stop(self):
    self.running = False
    self.lsl_thread.join(5)

def load(queue):
  global graph
  graph = Graph()
  print('init graph')

def start():
  graph.start()
  graph.app.exec_()

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
