#from PyQt5 import QtGui 

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg 
import multiprocessing
import collections
import random
import time
import math
import numpy as np

class DynamicPlotter():
    def startStreaming(self):
        streams = stream('name,' 'bci')
        self.inlet = StreamInlet(streams[0])
        #self.running = True
        while True:
            self.sample, self.timestamp = self.inlet.pull_sample(timeout-5)
            self.updateplot

    def __init__(self, size=(600,350)):
#   def __init__(self, sampleinterval=0.1, timewindow=10., size=(600,350)):
        
        self.frequency = 250.0 #the OpenBCI frequency
        self.sampleinterval = (1/self.frequency)*1000     #number of samples per millisecond
        self.timewindow=10.
        # Data stuff
        #self._interval = int(self.sampleinterval*1000)
        self._bufsize = int(self.timewindow/self.sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.timeBuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
       # self.x = np.zeros(self_bufsize, 0.0, self._bufsize)
       # self.y = np.zeros(self._bufsize, dtype=np.float)
        self.x = np.zeros(self._bufsize)
        self.y = np.zeros(self._bufsize)
        # PyQtGraph stuff
        self.app = QtGui.QApplication([])
        self.plt = pg.plot(title='Dynamic Plotting with PyQtGraph')             #pg.plot(...._)
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'amplitude', 'V')
        self.plt.setLabel('bottom', 'time', 's')
        self.curve = self.plt.plot(self.x, self.y, pen=(255,0,0))
        
        # QTimer
        #self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.updateplot)
        #self.timer.start(self.sampleinterval)
        
      
    #def getdata(self):
       # frequency = 0.5

        #noise = random.normalvariate(0., 1.)
        #new = 10.*math.sin(time.time()*frequency*2*math.pi) + noise
        #return new

         
    def updateplot(self):
        #self.databuffer.append( self.getdata() )
        self.databuffer.append(sample)
        self.y[:] = self.databuffer
        self.timeBuffer.append(timestamp)
        self.x[:] = self.timeBuffer
        self.curve.setData(self.x, self.y)
        self.app.processEvents()                    #keeps application active

    def run(self):
        self.app.exec_()

if __name__ == '__main__':
    m = DynamicPlotter()
    m.run()
