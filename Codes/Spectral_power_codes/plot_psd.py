import read_write as rw
import numpy as np
import os
from scipy.fftpack import fft,fftfreq
import matplotlib.pyplot as plt

def butter_filter(input_sig,sample_freq,lowf,highf,order=4):
	'''Computes the filtered value of a given discrete time signal using a butterwort filter.
	Args:
	input_sig: Input Signal
	sample_freq: Sampling frequency of the input signal
	lowf: Lower cut-off of the filter
	highf: Higher cut-off of the filter
	order: order of the filter to be used

	Returns:
	An array with the filtered signal'''
	r = sample_freq/2
	band = [lowf/r,highf/r]
	b,a = signal.butter(order,band,'band')
	output = signal.filtfilt(b,a,input_sig)
	return output

for ch in range(25,29):
	for sub in range (1,8):	
		os.chdir("G:/Harsh_Data_Backup/Data/New_Data_filtered/a")
		dt = 1/256
		file_name = "s"+str(sub)+"c"+str(ch)+".txt"
		seg = rw.read_file(file_name)
		seg = np.array(seg)
		segl = seg[0:512]
		segm = seg[66*512:67*512]
		segh = seg[135*512:136*512]
		Spsl = np.absolute(fft(segl))/3000
		Spsm = np.absolute(fft(segm))/3000
		Spsh = np.absolute(fft(segh))/3000
		sfreql = fftfreq(segl.size,d=dt)
		sfreqm = fftfreq(segm.size,d=dt)
		sfreqh = fftfreq(segh.size,d=dt)
		keep = sfreql>0
		Spsl = Spsl[keep]
		sfreql = sfreql[keep]
		keep = sfreqm>0
		sfreqm = sfreqm[keep]
		Spsm = Spsm[keep]
		keep = sfreqh>0
		sfreqh = sfreqh[keep]
		Spsh = Spsh[keep]
		#plt.xlim(xmin=4,xmax=14)
		# plt.plot(sfreql,Spsl,color='r')
		# plt.plot(sfreqm,Spsm,color='b')
		# plt.plot(sfreqh,Spsh,color='y')
		plt.figure("ch"+str(ch)+"sub"+str(sub))
		plt.plot(Spsl,color='g')
		plt.plot(Spsm,color='m')
		plt.plot(Spsh,color='c')
		plt.show()

# f = 5
# T = 1
# dt = 1/4
# x = np.linspace(0,T,T/dt)
# y = np.sin(2*np.pi*f*x) + np.sin(2*np.pi*10*f*x)
# y_filt = butter_filter(y,sample_freq=4,lowf=3,highf=6)
# Sps = np.absolute(fft(y))/3000
# sfreq = fftfreq(y.size,d=dt)
# keep = sfreq>0
# Sps = Sps[keep]
# sfreq = sfreq[keep]
# plt.plot(Sps,color='r')
# Sps = np.absolute(fft(y_filt))/3000
# sfreq = fftfreq(seg.size,d=dt)
# keep = sfreq>0
# Sps = Sps[keep]
# sfreq = sfreq[keep]
# plt.plot(Sps)