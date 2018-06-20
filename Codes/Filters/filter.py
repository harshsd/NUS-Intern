#code for filtering the data into bands
from __future__ import division
import numpy as np
import math
from random import *
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import svm,datasets
import os
import itertools
from scipy import signal


L=10
delta=25
q=3
alpha = 0.5
fs = 250
r = fs/2

for sub in range (1,31):
	for turn in range (1,3):
		for channel in range (1,25):
			os.chdir('/media/harsh/DATA/Readable_Data/Unfiltered_Data')
			file_name = 's'+str(sub)+'t'+str(turn)+'c'+str(channel)+'.txt'
			file = open(file_name,'r')
			print (file_name)
			sig = []
			a=0
			for line in file:
				for word in line.split():
					sig.append(float(word))
					a = a+1
			file.close()		
			#Alpha Band
			cuta = [1/r,4/r]
			b,a = signal.butter (4,cuta,'band')
			n_epochs = int(len(sig)/500)
			print (len(sig))
			# cutb = [4/r,7/r]
			# b1,a1 = signal.butter (4,cutb,'band')
			le = 0
			os.chdir('/media/harsh/DATA/Readable_Data/Delta')
			for start in range (0,n_epochs):
				input_sig = sig[start*500:((start+1)*500)]
				output_alpha = signal.filtfilt(b,a,input_sig)
				for x in range(0,len(output_alpha)):
					f_w = open('delta'+file_name,'a+')
					f_w.write(str(output_alpha[x]))
					f_w.write('\n')
					f_w.close()
				# output_beta = signal.filtfilt(b1,a1,input_sig)
				# for x in range(0,len(output_beta)):
				# 	f_w = open('theta'+file_name,'a+')
				# 	f_w.write(str(output_beta[x]))
				# 	f_w.write('\n')
				# 	f_w.close()
				# le = le + (len(output_alpha)+len(output_beta))/2		
			print (le)	