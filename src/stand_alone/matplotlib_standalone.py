from pylsl import StreamInlet, resolve_byprop, local_clock, TimeoutError
from pyqtgraph.Qt import QtGui,QtCore
import collections
import numpy as np
import pyqtgraph as pg
import time 
import signal, sys, os, time, csv
import serial
import threading

import matplotlib.pyplot as plt
import random_lsl

numSamples = 0

#count = -1

graph = None

class Graph(object):
  def __init__(self, size=(600,350)):
    self.running = True
    self.ProcessedSig = []
    self.SecondTimes = []
    self.count = -1

    plt.ion()
    plt.hold(False)     
    self.lineHandle = plt.plot(self.SecondTimes, self.ProcessedSig)
    plt.title("Streaming Live EMG Data")
    plt.xlabel('Time (s)')
    plt.ylabel('Volts')
    plt.show()

  def _graph_lsl(self):
    print('checking if stream has be initialized')
    self.streams = resolve_byprop('name', 'bci', timeout=2.5)
    try:
      self.inlet = StreamInlet(self.streams[0])
    except IndexError:
      raise ValueError('Make sure stream name=bci is opened first.')
    while self.running:
      # initial run
      self.sample, self.timestamp = self.inlet.pull_sample(timeout=5)
    # time correction to sync to local_clock()
      try:
        if self.timestamp is not None and self.sample is not None:
          self.timestamp = self.timestamp + self.inlet.time_correction(timeout=5) 

      except TimeoutError:
        pass
      self.SecondTimes.append(self.sample[1])                         #add time stamps to array 'timeValSeconds'
      self.ProcessedSig.append(self.sample[0])                           #add processed signal values to 'processedSig'
    
      self.count = self.count + 1

      if((self.count % 20 == 0) and (self.count != 0)):   #every 20 samples (ie ~ 0.10 s) is when plot updates
	self.lineHandle[0].set_ydata(self.ProcessedSig)
	self.lineHandle[0].set_xdata(self.SecondTimes)
	#plt.xlim(0, 5)
	plt.xlim(self.SecondTimes[0], self.SecondTimes[-1])
	plt.ylim(0, 10)
	plt.pause(0.01)
      
      if(self.count >= 399): 
        self.ProcessedSig.pop(0)    
        self.SecondTimes.pop(0)

    plt.pause(0.01)
    print('closing graphing utility')
    self.inlet.close_stream()

  def start(self):
    self.lsl_data = threading.Thread(target=random_lsl.start)
    #self.lsl_thread = threading.Thread(target=self._graph_lsl)
    self.lsl_data.start()
    print('lsl data stream has started')
    time.sleep(6)
    #self.lsl_thread.start()
    print('graphing will begin')
    self._graph_lsl()
     
  def stop(self):
    self.running = False
    self.lsl_thread.join(5)

def load(queue):
  global graph
  #lsl_data.start()
  #print('done starting thread')
  #time.sleep(5)
  graph = Graph()
  
  print('init graph')

def start():
  #graph._graph_lsl()
  graph.start()
  #graph._graph_lsl()
 

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
   # while not event.is_set():
    while not event:
      time.sleep(1)

    print('event was set, stopping')
    stop()

if __name__ == '__main__':
  main()
