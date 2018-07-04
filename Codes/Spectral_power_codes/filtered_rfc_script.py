import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.fftpack import fft,fftfreq
import read_write as rw
import svm
import random_forest_classifier as rfc
import time

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

#                                                                                                 ax = plt.subplot(111)
# ax.plot(freq,(np.absolute(Y)**2)/3000)
# ax.set_xlim(0,30)
# plt.show()

band_name = input("Enter name of band (d,t,a,b,g): ")
os.chdir('G:/Harsh_Data_Backup/Data/New_Data_filtered/'+band_name)
# os.chdir('G:/Harsh_Data_Backup/Data/New_Data')
ch_accuracy=[]
mean_accuracy = 0
for sub in range (1,8):
	lpsdt = []
	mpsdt = []
	hpsdt = []
	for ch in range (1,63):
		#print (sub,ch)
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
			# delta_f = (0.1,4)
			# theta_f = (4,7)
			# alpha_f = (8 ,12)
			# beta_f = (12,30)
			# gamma_f = (30,100
			if band_name == 'a':
				Sps = Sps[16:24]
			elif band_name == 'd':
				Sps = Sps[0:10]
			elif band_name	== 't':
				Sps = Sps[7:16]
			elif band_name == 'b':
				Sps = Sps[24:60]
			elif band_name == 'g':
				Sps = Sps[60:]
			else:
				print ("error")					
			# print (sfreq.size)
			# print (Sps.size)
			#plt.plot(sfreq,Sps)
			#plt.show()
			if ((i<60) or (i>=180 and i<240) or (i>=360 and i<420)):
				lpsd.append(np.sum(np.square(Sps)))
				#plt.plot(sfreq,Sps,color='r')
				#plt.show()
				#print ("lpsd")
			elif((i>=60 and i<120) or (i>=240 and i<300) or (i>=420 and i<480)):
				mpsd.append(np.sum(np.square(Sps)))
				#plt.plot(sfreq,Sps,color = 'b')
				#plt.show()
				#print ("mpsd")
			else:
				hpsd.append(np.sum(np.square(Sps)))
				#plt.plot(sfreq,Sps, color = 'y')
				#plt.show()
				#print ("hpsd")		
		lpsd = np.array(lpsd)
		mpsd = np.array(mpsd)
		hpsd = np.array(hpsd)	
		lpsdt.append(lpsd)
		mpsdt.append(mpsd)
		hpsdt.append(hpsd)
	lpsdt=np.array(lpsdt)
	mpsdt=np.array(mpsdt)
	hpsdt=np.array(hpsdt)
	# plt.plot(lpsdt[0],color='r')
	# plt.plot(mpsdt[0],color='y')
	# plt.plot(hpsdt[0],color='g')
	# plt.show()
	x,y = lpsdt.shape
	lpsdt = lpsdt.reshape((y,x))
	x,y = mpsdt.shape
	mpsdt = mpsdt.reshape((y,x))
	x,y = hpsdt.shape
	hpsdt = hpsdt.reshape((y,x))
	#print (lpsdt.shape)	
	time.sleep(10)	
	mean = 0
	std = 0
	# for cbt in range (1,10):
	# 	for gbt in range (1,10):
	# 		c = cbt*10
	# 		g = gbt*10
	# 		meanlocal,stdlocal = svm.accuracy_svm_3(lpsdt,mpsdt,hpsdt,c,g)
	# 		if(meanlocal>mean):
	# 			mean = meanlocal
	# 			std = stdlocal
	for trees in range (5,10):
		for depth in range (5,10):
			trees_act = trees*100
			meanlocal,stdlocal = rfc.rfc(lpsdt,mpsdt,hpsdt,num_of_trees=trees_act,max_depth=depth)
			if(meanlocal>mean):
				mean = meanlocal
				std = stdlocal
	print ("real rfc accuracy")
	print (sub,mean)
	mean_accuracy = mean_accuracy + mean/7
print (mean_accuracy)