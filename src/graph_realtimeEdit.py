from pylsl import StreamInlet, resolve_byprop, local_clock, TimeoutError
from pylsl import StreamInfo,StreamOutlet
from random import random as rand
import collections
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui,QtCore 
import time
import signal, sys, os, time, csv
import serial
import threading

win = pg.GraphicsWindow() 
graph = None

class Graph(object):
  def __init__(self,size=(600,350)):
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
    self.x = np.zeros(self._bufsize)
    self.y = np.zeros(self._bufsize)
    self.app = QtGui.QApplication([])
    self.plt = pg.plot(title='Dynamic Plotting with PyQtGraph')
    self.plt.resize(*size)
    self.plt.showGrid(x=True,y=True)
    self.plt.setLabel('left','amplitude','V')
    self.plt.setLabel('bottom','time','s')
    self.curve = self.plt.plot(self.x,self.y,pen=(255,0,0))
  
  def _graph_lsl(self):
    while self.running:
      sample, timestamp = self.inlet.pull_sample(timeout=5)

      # time correction to sync to local_clock()
      try:
        if timestamp is not None and sample is not None:
          timestamp = timestamp + self.inlet.time_correction(timeout=5) 

        # TODO Place graphing stuff here
       
        self.dataBuffer.append(sample[0])
        self.y[:] = self.dataBuffer
        self.timeBuffer.append(timestamp)
        self.x[:] = self.timeBuffer
        
        # added 
        self.sampleNum = self.x
        self.timestampIndex = self.y
        
        self.sampleNum = np.roll(self.sampleNum, 1) # scroll data
        self.timestampIndex = np.roll(self.timestampIndex, 1)

        self.curve.setData(self.sampleNum, self.timestampIndex) # re-plot 
        self.app.processEvents()
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

def randomData():
  info = StreamInfo('bci','randomData',1,150)
  outlet = StreamOutlet(info)
  print ('now sending data')
  
  while True:
    sample = [rand()]
    outlet.push_sample(sample)
    time.sleep(1)

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
  data_stream = threading.Thread(target=randomData)
  data_stream.start()
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
