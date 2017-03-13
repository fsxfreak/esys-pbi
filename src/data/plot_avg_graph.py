##plot_avg_graph
##1. set channel to be analyzed
##2. ensure data is saved in BCI_data folder of directory the script is running from  
##3. set gain (1,2,4,6,8,12,24) where 24X is 0.02235 microVolts per count
##4. sampling frequency, fs = 250 Hz

import os
import matplotlib.pyplot as plt
import csv
import numpy as np

y_tot = []
sample_tot = []
markers_all = []
channel = 3
gain = 24
scaleFactor = 4.5/gain/(2**23 - 1)
fs = 250

current_path = os.path.dirname(os.path.abspath(__file__))
path = current_path + '\\BCI_data\\'

'''#convert txt to csv
for trial_no, trials in enumerate(os.listdir(path)):
	output_csv = "data-" + str(trial_no) + ".csv"
	with open('%s%s' %(path,trials),'r') as input_f:
		for row in input_f:
			lines = (row.split(",") for row in input_f if row)
			if not os.path.exists('CSV_data'):
				os.makedirs('CSV_data')
			out_path = os.path.join(current_path + '\\CSV_data\\', output_csv) 	
			with open(out_path,'w') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerows(lines)	
'''


#plot individual graph directly from text file
for run,trials in enumerate(os.listdir(path)):
	y = []
	sample_num = []
	marker = []
	with open('%s%s' %(path,trials),'r') as input_f:
	  	csv_f = csv.reader(input_f)
		#for num, row in enumerate(input_f):
		for num, vals in enumerate(csv_f):
			   if not vals == 0:
			   #vals = row.split(',')
				   if vals[0]=='STIM':
					msg = vals[len(vals)-1]
					if 'pre' in msg:
						marker.append(num)
						y.append(y[len(y)-1]*scaleFactor)

				   if vals[0]=='BCI':
					y1 = vals[channel+2]
					y.append(float(y1)*scaleFactor) 
	
	sample_num = [i for i in range(len(y))]
	sample_tot.append(np.divide(sample_num,250)) 
	y_tot.append(y)
	markers_all.append(marker)

for i in range(run+1):
	plt.figure(1)
	plt.plot(sample_tot[i],y_tot[i],'b-', marker='o', markerfacecolor = 'r', markevery=markers_all[i], markersize = 20)
'''
#to calculate and plot the average graph
#checking if there is more than 1 trial for data to be averaged
if run > 1:

	#making all data sets from chosen channel the same size
	maxSample_y = max(len(i) for i in y_tot)
	maxSample_x = max(len(i) for i in sample_tot)

	for ydata in y_tot:
		if len(ydata)<maxSample_y:
			ydata.extend(0 for point in range(maxSample_y - len(ydata)))
	
	for xdata in sample_tot:
		if len(xdata) < maxSample_x:
			xdata.extend(0 for point in range(maxSample_x - len(xdata)))
		
	y_avg = (np.array(y_tot[0]) + np.array(y_tot[1]))/2
	x_avg = (np.array(sample_tot[0])+np.array(sample_tot[1]))/2

	for data in range(2, run+1):
		y_avg = (np.array(y_avg) + np.array(y_tot[data]))/2
		x_avg = (np.array(x_avg) + np.array(sample_tot[data]))/2
	
	plt.plot(x_avg,y_avg,'r-')

#saves csv file of averaged signal values (debug purposes)
ylist = np.asarray(y_avg)
np.savetxt("y_avg.csv",ylist,delimiter=",")
'''
	
plt.title('Individual and Averaged sample data')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (uV)')
plt.show()
