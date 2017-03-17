##real-time plot

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import collections

class Graph():
	def setup(self):
		#provide all parameters as floats with at least one decimal point
		self.frequency = 250.0
		self.sample_interval = 1/self.frequency
		#converting to milliseconds for timer.start() function
		self.timer_interval = self.sample_interval*1000 
		self.time_window = 10
		self.buffer_size = int(self.time_window/self.sample_interval)
		self.data_buffer = collections.deque([0.0]*self.buffer_size,self.buffer_size)
		
		self.x = np.linspace(0.0,self.time_window,self.buffer_size)
		self.y = np.zeros(self.buffer_size, dtype=np.float)

		#PyQtGraph settings
		self.app = QtGui.QApplication([])
		self.plt = pg.plot(title='Real Time Open BCI data')
		self.plt.showGrid(x=True, y=True)
		self.plt.setLabel('left','amplitude','uV')
		self.plt.setLabel('bottom','time','s')
		self.curve = self.plt.plot(self.x,self.y,pen=(255,0,0))

		#QTimer
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.update_plot)
		self.timer.start(self.timer_interval)

	def __init__(self):
		with open('data-trial.txt','r') as f:
			self.data = f.readlines()
			self.data = [x.strip() for x in self.data]
		self.i = 0	

	def get_data(self):
		sample = self.data[self.i].split(' ')[5]
		self.i = self.i + 1
		return sample 

	def update_plot(self):
		self.data_buffer.append(self.get_data())
		self.y[:] = self.data_buffer
		self.curve.setData(self.x,self.y)
		self.app.processEvents()

	def run(self):
		self.app.exec_()

if __name__ == '__main__':
	g = Graph()
	g.setup()
	g.run()

