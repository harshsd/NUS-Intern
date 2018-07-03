import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.fftpack import fft,fftfreq
import read_write as rw
import svm
import random_forest_classifier as rfc

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

band_name = input("Enter name of band (d,t,a,b,g): ")
os.chdir('G:/Harsh_Data_Backup/Data/New_Data_filtered/'+band_name)
ch_accuracy=[]
for ch in range (1,63):
	mean_acc = 0
	cc_max = 0
	gg_max = 0
	mean_for_fixed_par = 0
	for sub in range (1,8):
		print (sub,ch)
		file_name = "s"+str(sub)+"c"+str(ch)+".txt"
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
			Sps = np.absolute(fft(seg))/3000
			sfreq = fftfreq(seg.size,d=dt)
			keep = sfreq>0
			Sps = Sps[keep]
			sfreq = sfreq[keep]
			# print (sfreq.size)
			# print (Sps.size)
			#plt.plot(sfreq,Sps)
			#plt.show()
			if ((i<60) or (i>=180 and i<240) or (i>=360 and i<420)):
				lpsd.append(Sps[0:60])
				#plt.plot(sfreq,Sps,color='r')
				#plt.show()
				#print ("lpsd")
			elif((i>=60 and i<120) or (i>=240 and i<300) or (i>=420 and i<480)):
				mpsd.append(Sps[0:60])
				#plt.plot(sfreq,Sps,color = 'b')
				#plt.show()
				#print ("mpsd")
			else:
				hpsd.append(Sps[0:60])
				#plt.plot(sfreq,Sps, color = 'y')
				#plt.show()
				#print ("hpsd")		
		lpsd = np.array(lpsd)
		mpsd = np.array(mpsd)
		hpsd = np.array(hpsd)	
		x,y = lpsd.shape
		#lpsd = lpsd.reshape((y,x))
		x,y = mpsd.shape
		#mpsd = mpsd.reshape((y,x))
		x,y = hpsd.shape
		#hpsd = hpsd.reshape((y,x))								
		mean,std = rfc.rfc(lpsd,mpsd,hpsd)
		#print (mean)
		mean_for_fixed_par = mean_for_fixed_par + mean/7
	mean_acc = mean_for_fixed_par	
	# print ("Channel: "+str(ch))
	# print(" Max Acuuracy: "+str(mean_acc))
	ch_accuracy.append((ch,mean_acc))
print (ch_accuracy)
ch_accuracy = np.array(ch_accuracy)
dtype = [('channel_name',int),('ch_Accuracy',float)]
a = np.array(ch_accuracy,dtype=dtype)
print(np.sort(a,order='ch_Accuracy'))	