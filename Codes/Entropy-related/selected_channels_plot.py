from __future__ import division
import numpy as np
import math
from random import *
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import svm,datasets
import os
import itertools
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import time

def rolling_mean (a,n):
	a = np.array(a)
	l = len(a)
	rolling_mean = []
	for start in range (0,l-n+1):
		part_sum = 0
		for k in range (0,n):
			part_sum += a[start+k]
		rolling_mean.append(part_sum/n)
	return np.array(rolling_mean)


def sorted_array_with_indices(b):
	a = b
	l = len(a)
	x = np.arange(l)
	x = x
	for i1 in range (0,l-1):
		#print (i1)
		for i2 in range (0,l-1-i1):
			#print(i2)
			if (a[i2])<(a[i2+1]):
				#print ("exchanged")
				temp = a[i2]
				a[i2]=a[i2+1]
				a[i2+1]=temp
				temp = x[i2]
				x[i2]=x[i2+1]
				x[i2+1]=temp
	return (a,x)  

def read_file(file_name):
	f = open(file_name , 'r')
	vec = []
	for line in f:
		for word in line.split():
			vec.append(float(word))
	f.close()
	return vec 

#Last one has lowest score and hence can be the best channel
#tsallis =      8,  4, 20,  9, 19, 22, 18, 16,  7,  5, 23,  3, 10,  6,  1, 14,  2, 21, 13, 12, 11,  0, 17, 15
#shannon = 	 8, 20,  4,  9,  1, 19, 22, 16, 23, 18,  0, 13, 21,  6, 14,  7, 10, 12,  2,  5, 17, 11,  3, 15
#renyi =   8, 20,  4,  9, 23,  1, 21, 22, 16, 19, 18,  6,  0, 14, 10, 17,  7, 13, 11, 12,  2,  5,  3, 15
#permut = 0, 15, 12, 19,  5,  2,  8,  9, 23, 18,  3,  6, 20,  1, 22,  4, 17, 11, 13, 21, 14, 16,  7, 10

sorted_channels = {'shannon' : [8, 20,  4,  9,  1, 19, 22, 16, 23, 18,  0, 13, 21,  6, 14,  7, 10, 12,  2,  5, 17, 11,  3, 15] ,
					'tsallis' : [ 8,  4, 20,  9, 19, 22, 18, 16,  7,  5, 23,  3, 10,  6,  1, 14,  2, 21, 13, 12, 11,  0, 17, 15],
					'renyi' : [8, 20,  4,  9, 23,  1, 21, 22, 16, 19, 18,  6,  0, 14, 10, 17,  7, 13, 11, 12,  2,  5,  3, 15],
					'permut' : [0, 15, 12, 19,  5,  2,  8,  9, 23, 18,  3,  6, 20,  1, 22,  4, 17, 11, 13, 21, 14, 16,  7, 10]}
entropy = input("Enter Entropy Name: ")
ch_selected = sorted_channels[entropy]
ch_selected = np.array(ch_selected)
# print(ch_selected)
ch_selected = np.flip(ch_selected,0)
# print (ch_selected)
no_of_significant_channels = int(input("Enter number of significant channels(less than 24): "))
ch_selected = ch_selected[0:no_of_significant_channels]
# print(ch_selected)
slopes = []
for sub in range(1,31):
	for turn in range (1,3):
		print (sub,turn)
		os.chdir('G:/Harsh_Data_Backup/Readable_Data/Entropies_2_S/')
		slope_weights = []
		all_ent = []
		leng = 0
		for ch in ch_selected:
			ent = read_file(entropy+"s"+str(sub)+"t"+str(turn)+"c"+str(ch+1)+".txt")
			x = np.arange(len(ent))
			line = np.polyfit(x,ent,1,full=True)
			slope = line[0][0]
			slope_weights.append(slope)
			all_ent.append(ent)
			if(leng == 0):
				leng = len(ent)
			elif(leng != len(ent)):
				print ("error")	
		final_sig = np.zeros(leng)
		slope_weights = np.array(slope_weights)
		slope_weights = slope_weights/np.sum(abs(slope_weights))
		for index in range (0,leng):
			for j in range (0,no_of_significant_channels):
				final_sig[index] = final_sig[index] + slope_weights[j]*all_ent[j][index]
		mov_avg_n = 1000
		rolling_sig = rolling_mean(final_sig,mov_avg_n)		
		xfinal = np.arange(len(rolling_sig))       
		final_line = np.polyfit(xfinal,rolling_sig,1,full=True)        
		yfinal = (xfinal*final_line[0][0]) + final_line[0][1]	
		slopes.append(final_line[0][0])	
		os.chdir("G:/Harsh_Data_Backup/Readable_Data/selected_channels_pictures/"+entropy)	
		plt.figure(entropy+"s"+str(sub)+"t"+str(turn)+"c"+str(ch+1)+".png")	
		plt.plot(xfinal,rolling_sig)
		plt.plot(xfinal,yfinal)
		plt.savefig(entropy+"s"+str(sub)+"t"+str(turn)+"c"+str(ch+1)+".png")	
		plt.close(entropy+"s"+str(sub)+"t"+str(turn)+"c"+str(ch+1)+".png")
slopes = np.array(slopes)
print (np.sum(slopes)/no_of_significant_channels)