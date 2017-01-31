import gi
gi.require_version('Gtk', '2.0')
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf
import threading
import os, signal
from gi.repository import GObject as gobject
gobject.threads_init()
from time import sleep
import random
import open_bci_v3 as bci

import numpy as np
from scipy import io
# from gi.repository import gtk

#Number of repetitions for each image in the directory
PHOTO_REPS = 2

class MainWin:

	'''
	Data thread subclass for gathering data from the OpenBCI amplifier
	The thread gets executed in parallel with the graphical thread, and handles samples with the callback handleSample()
	Data is stored in a matrix of size CxS, C = number of channels, S = number of samples
	'''
	class DataThread(threading.Thread):

		def __init__(self):
			super(MainWin.DataThread, self).__init__()
			
			#Connect the board object to the port; the port name may vary with device, so we just have to hardcode it
			self.board = bci.OpenBCIBoard(port='/dev/tty.usbserial-DB00MHTW', filter_data=True, daisy=False)
			
			#Check the status of the device
			print (self.board.getNbEEGChannels(), "EEG channels and", self.board.getNbAUXChannels(), "AUX channels at", self.board.getSampleRate(), "Hz.")

			#Don't worry about why this is in a loop; was using it for testing
			for i in range(0, 1):
				self.board.set_channel7()

			sleep(10)

			#sentinel flag for running the thread
			self.running = True
			
			#initialize the data matrix to empty
			self.data = np.empty(shape=(8, 0))


		#Data callback; this function gets called automatically every single time a sample is received by the OpenBCI
		def handleSample(self, curSample):
			
			#increment the counter for use with timestamps in GUI thread
			#I'm actually not 100% sure why this is thread safe to access without mutex....I think it's a Python thing?
			self.samplesRead += 1
			
			#Stack new sample onto the data matrix
			self.data = np.hstack([self.data, np.reshape(curSample.channel_data[0:8],(8, 1))])		

		
		def stop(self):
			#stop is called when window is closed so we unset sentinel here, and disconnect from the board to disable the data reading
			self.running = False
			self.board.disconnect()


		def run(self):
			self.samplesRead = 0		
			#This starts the board to begin streaming; the argument it takes is a function pointer to the data handler function
			self.board.start_streaming(self.handleSample)
			while self.running:
				x = 1

	'''
	This function handles timing of the images on the screen
	It also handles iterating over the image array, as well as gathering the timestamps for each stimulus
	'''
	def timerFunc(self):

		if self.imageIndex < len(self.filenames):

			if self.showFixation == False:
				pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale('./P300Photos/' + self.filenames[self.imageIndex], width=700, height=700, preserve_aspect_ratio=False)
				self.image.set_from_pixbuf(pixbuf)
				self.imageIndex += 1
				gobject.timeout_add(self.testImageDuration, self.timerFunc)
				self.timestamps.append(self.dataThread.samplesRead)
			else:
				self.image.set_from_pixbuf(self.fixation)
				gobject.timeout_add(self.fixationDuration, self.timerFunc)

			self.showFixation = ~self.showFixation
		
		else:
			self.image.set_from_pixbuf(self.fixation)
			#gather an extra ~2 seconds of data at the end for window completion reasons
			sleep(2)
			self.dataThread.stop()

		return False

			

	def __init__(self):
		#get P300 file names, shuffle them, and create markers array
		self.filenames = []
		self.timestamps = []
		self.markers = []
		for file in os.listdir("./P300Photos"):
			for i in range(0, PHOTO_REPS):
				self.filenames.append(file)
		random.shuffle(self.filenames)

		#Create our markers array up front
		for f in self.filenames:
			if 'apple' in f:
				self.markers.append(0)
			else:
				self.markers.append(1)

		self.imageIndex = 0
		self.samplesRead = 0
		
		#if set to True, will show the fixation dot on the next iteration
		self.showFixation = False
		
		#Time durations for fixation image, as well as test images in milliseconds
		self.fixationDuration = 700
		self.testImageDuration = 200

		#Where is our fixation image?
		self.fixation = GdkPixbuf.Pixbuf.new_from_file_at_scale('./fixation_dot2.jpg', width=700, height=700, preserve_aspect_ratio=False)

		#setup GTK window stuff
		self.window = gtk.Window()
		self.window.connect('delete-event', self.signalInterrupt)
		self.image = gtk.Image()
		self.image.set_from_pixbuf(self.fixation)
		self.window.add(self.image)
		self.image.show()
		self.window.show()

		#start threading junk
		'''
		UNCOMMENT THE NEXT TWO LINES TO GET THE DATA THREAD GOING ONCE WE HAVE THE OPEN BCI CONNECTED
		'''
		self.dataThread = self.DataThread()
		self.dataThread.start()
		gobject.timeout_add(5000, self.timerFunc)

	def main(self):
		gtk.main()

	#Gets called when the (x) on the window is clicked to close the window.  Note that stopping the program from Eclipse will NOT trigger this function
	def signalInterrupt(self, selfnum, frame):
		self.dataThread.stop()
		io.savemat('p300Data_jct_2_17_10.mat', {'data' : self.dataThread.data, 'timestamps' : self.timestamps, 'markers' : self.markers})

		gtk.main_quit()

if __name__ == "__main__":
	MainWin().main() 