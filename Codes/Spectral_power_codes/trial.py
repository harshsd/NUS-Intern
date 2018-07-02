import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.fftpack import fft,fftfreq
import read_write as rw

# f = 5
# f1 = 20
# dt = 0.001
# T = 10
# x = np.linspace(0,T,T/dt)
# y = np.sin(2*np.pi*x*f) + 10*np.sin(2*np.pi*x*f1)
# Y = fft(y)
# freq = fftfreq(y.size,d=dt)
# print (freq.size)
# print (Y.size)

# keep = freq>=0
# Y = Y[keep]
# freq = freq[keep]

# ax = plt.subplot(111)
# ax.plot(freq,(np.absolute(Y)**2)/3000)
# ax.set_xlim(0,30)
# plt.show()

os.chdir('G:/Harsh_Data_Backup/Data/New_Data')
file_name = "s1c1.txt"
sig = rw.read_file(file_name)
sig = np.array(sig)
dt = 1/256
lpsd = []
mpsd = []
hpsd = []
for i in range (0,540):
	seg = sig[512*i:512*i+512]
	#print (len(seg))
	seg = np.array(seg)
	Sps = np.absolute(fft(seg))**2
	sfreq = fftfreq(seg.size,d=dt)
	keep = sfreq>0
	Sps = Sps[keep]
	sfreq = sfreq[keep]
	# print (sfreq.size)
	# print (Sps.size)
	#plt.plot(sfreq,Sps)
	#plt.show()
	if ((i<60) or (i>=180 and i<240) or (i>=360 and i<420)):
		lpsd.append(Sps)
	elif((i>=60 and i<120) or (i>=240 and i<300) or (i>=420 and i<480)):
		mpsd.append(Sps)
	else:
		hpsd.append(Sps)
lpsd = np.array(lpsd)
mpsd = np.array(mpsd)
hpsd = np.array(hpsd)	
print (lpsd[0].shape)			
print ("done")		

