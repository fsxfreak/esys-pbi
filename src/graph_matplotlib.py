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

numSamples = 0

#count = -1

graph = None

class Graph(object):
  def __init__(self, size=(600,350)):
    streams = resolve_byprop('name', 'bci', timeout=2.5)
    try:
      self.inlet = StreamInlet(streams[0])
    except IndexError:
      raise ValueError('Make sure stream name=bci is opened first.')
   
    self.running = True
    
    self.ProcessedSig = []
    self.SecondTimes = []
    self.count = -1
    self.sampleCount = self.count 

    plt.ion()
    plt.hold(False)     
    self.lineHandle = plt.plot(self.SecondTimes, self.ProcessedSig)
    plt.title("Live Stream EEG Data")
    plt.xlabel('Time (s)')
    plt.ylabel('mV')
    plt.show()
    #while(1):
    #secondTimes.append(serialData[0])                         #add time stamps to array 'timeValSeconds'
    #floatSecondTimes.append(float(serialData[0])/1000000)     # makes all second times into float from string
    
    #processedSig.append(serialData[6])                           #add processed signal values to 'processedSig'
    #floatProcessedSig.append(float(serialData[6]))
    


  def _graph_lsl(self):
    while self.running:
      # initial run
      self.sample, self.timestamp = self.inlet.pull_sample(timeout=5)
      #if self.timeBuffer[0] == 0.0:
       # self.timeBuffer = collections.deque([self.timestamp] * self._bufsize, self._bufsize)
    # time correction to sync to local_clock()
      try:
        if self.timestamp is not None and self.sample is not None:
          self.timestamp = self.timestamp + self.inlet.time_correction(timeout=5) 

      except TimeoutError:
        pass
      self.SecondTimes.append(self.timestamp)                         #add time stamps to array 'timeValSeconds'
      print(abs(self.sample[3])/1000)
      self.ProcessedSig.append(abs(self.sample[3])/1000)                           #add processed signal values to 'processedSig'
    
      self.sampleCount = self.sampleCount + 1  
      self.count = self.count + 1
      #plt.show()
      if((self.count % 20 == 0) and (self.count != 0)):   #every 20 samples (ie ~ 0.2 ms) is when plot updates
      #if(self.count == 20):
        self.count = -1
	self.lineHandle[0].set_ydata(self.ProcessedSig)
	self.lineHandle[0].set_xdata(self.SecondTimes)
	#plt.xlim(0, 5)
	plt.xlim(self.SecondTimes[0], self.SecondTimes[-1])
	plt.ylim(0, 5)
        #plt.autoscale(True)
	plt.pause(0.01)
      
      
      
      if(self.sampleCount >= 511):        #shows up to 2 seconds of data (512 samples = 2s of data given a 256 Hz (BCI) sampling freq)
        self.ProcessedSig.pop(0)    
        self.SecondTimes.pop(0)

    plt.pause(0.01)
    print('closing graphing utility')
    self.inlet.close_stream()

  def start(self):
    #self.lsl_thread = threading.Thread(target=self._graph_lsl)
    #self.lsl_thread.start()
    self._graph_lsl()
  
  def stop(self):
    self.running = False
    self.lsl_thread.join(5)

def load(queue):
  global graph
  graph = Graph()
  print('init graph')

def start():
  graph.start()
  #graph.app.exec_()

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
