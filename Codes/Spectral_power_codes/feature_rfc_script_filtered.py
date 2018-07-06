import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.fftpack import fft,fftfreq
import read_write as rw
import svm
import random_forest_classifier as rfc
import time
import psd_feat as pf
import train_rfc as trfc

def reshape(data):
	ch = len(data)
	epochs = len(data[0])
	feat = len(data[0][0])
	final_list = []
	for epoch in range (0,epochs):
		epoch_list = []
		for c in range (0,ch):
			for f in range(0,feat):
				epoch_list.append(data[c][epoch][f])
		final_list.append(epoch_list)		
	return np.array(final_list)			

start_time = time.time()
band_name = input("Enter name of band (d,t,a,b,g): ")
os.chdir('G:/Harsh_Data_Backup/Data/New_Data_filtered/'+band_name)
ch_accuracy=[]
mean_accuracy = 0
for sub in range (1,8):
	print (sub)
	lpsdt = []
	mpsdt = []
	hpsdt = []
	for ch in range (1,63):
		file_name = "s"+str(sub)+"c"+str(ch)+".txt"
		sig = rw.read_file(file_name)
		sig = np.array(sig)
		dt = 1/256
		f_step = 0.5
		lpsd = []
		mpsd = []
		hpsd = []
		for i in range (0,540):
			seg = sig[512*i:512*i+512]
			seg = np.array(seg)
			Sps = np.absolute((fft(seg))**2)/3000
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
				f_start = 8
			elif band_name == 'd':
				Sps = Sps[0:10]
				f_start = 0.1
			elif band_name	== 't':
				Sps = Sps[7:16]
				f_start = 3.5
			elif band_name == 'b':
				f_start = 12
				Sps = Sps[24:60]
			elif band_name == 'g':
				Sps = Sps[60:]
				f_start = 30
			else:
				print ("error")	

			df = pf.dominant_frequency(Sps,f_start,f_step)
			#print ("df")
			apdp = pf.apdp(Sps,width=5)
			#print ("apdp")
			cgf = pf.cgf(Sps,f_start,f_step)
			#print ("cgf")
			fv = pf.fv(Sps,f_start,f_step)
			#print ("fv")
			feature_vector = (df,apdp,cgf,fv)					

			if ((i<60) or (i>=180 and i<240) or (i>=360 and i<420)):
				lpsd.append(feature_vector)
			elif((i>=60 and i<120) or (i>=240 and i<300) or (i>=420 and i<480)):
				mpsd.append(feature_vector)
			else:
				hpsd.append(feature_vector)
			#print (ch,i)		
		lpsdt.append(lpsd)
		mpsdt.append(mpsd) 
		hpsdt.append(hpsd)
	#print ("line 84")
	#print (lpsdt[0][0])	
	lpsdt=np.array(lpsdt)
	#print ("line 85")
	mpsdt=np.array(mpsdt)
	hpsdt=np.array(hpsdt)
	x,y,z = lpsdt.shape
	#print (x,y,z)
	#print ("line 88")
	lpsdt = reshape(lpsdt)
	mpsdt = reshape(mpsdt)
	hpsdt = reshape(hpsdt)
	x,y = lpsdt.shape
	#print (x,y)
	#time.sleep(100)d
	print ("data processed")		
	mean = trfc.final_accuracy(lpsdt,mpsdt,hpsdt)
	print (sub,mean)	
	mean_accuracy = mean_accuracy + mean/7
print (mean_accuracy)
print ("total running time")
print (time.time()-start_time)



	# for cbt in range (1,10):
	# 	for gbt in range (1,10):
	# 		c = cbt*10
	# 		g = gbt*10
	# 		meanlocal,stdlocal = svm.accuracy_svm_3(lpsdt,mpsdt,hpsdt,c,g)
	# 		if(meanlocal>mean):
	# 			mean = meanlocal
	# 			std = stdlocal
	# for trees in range (5,10):
	# 	for depth in range (5,10):
	# 		trees_act = trees*100
	# 		meanlocal,stdlocal = rfc.rfc(lpsdt,mpsdt,hpsdt,num_of_trees=trees_act,max_depth=depth)
	# 		if(meanlocal>mean):
	# 			mean = meanlocal
	# 			std = stdlocal