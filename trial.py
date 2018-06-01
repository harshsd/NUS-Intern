from __future__ import division
import numpy as np
import math
from random import *
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import svm,datasets
import os


style.use("ggplot")
os.chdir('/home/harsh/Desktop/Harsh_Deshpande/Readable_Data')

window_in_s = 0.5
time_step_in_s = 0.5
# Assume eeg is present in a vector sig
L=20	#10             #10
w= int(window_in_s*250) #128			#256000
delta= int(time_step_in_s*250) #8			#8000
#For Tsallis entropy
# q= int(input("Enter q for Tsallis Entropy"))	#5 #1164500
q=5
##Entropy calculations
def sig_entropy ( L , w, delta, sig):

	entropy = []
	K = len(sig)
	M = (K-w)//delta  # Should be an int
	
	#print (maxp,minp)
	for m in range (0,M):
		partition = sig[m*delta:(w+(m*delta))+1]
		#print partition
		#print m
		#sh_entropy[m] = partition_entropy(partition,L,q)[0]
		#ts_entropy[m] = partition_entropy(partition,L,q)[0]
		entropy.append(partition_entropy(partition,L,q))
		#print(m/M)
	#print entropy
	return entropy

def partition_entropy( partition,L,q):
	
		maxp = np.amax(partition)
		minp = np.amin(partition)
		slot_height = (maxp-minp)/L
		#print slot_height
		ts_ent = Tsallis_entropy(partition,slot_height,maxp,minp,q)
		#sh_ent = Shannon_entropy(partition,slot_height,maxp,minp)
		sh_ent = 0
		#print (sh_ent,ts_ent)
		return (sh_ent,ts_ent)
		#amplitude intervals defined as [minp+ (k) (slot_height) , minp + (k+1) (slot_height)] k belongs to 0 to L-1
		#Number of s(k) in partition is w

def P_m_l(partition,k,slot_height,maxp,minp): #k from 0 to L-1

		count = 0
		for i in range (0,w-1):
			if ((partition[i] >= minp + k*(slot_height)) & (partition[i] <= minp + (k+1)*(slot_height))):
					count = count + 1
		#print count
		#print (count/w)			
		return (count/w)

def Shannon_entropy(partition,slot_height,maxp,minp):
	sh_ent = 0.00
	for it in range (0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		if(prob_m_l > 0):
			sh_ent = sh_ent - (prob_m_l*math.log(prob_m_l));
	#print sh_ent		
	return sh_ent
	
def Tsallis_entropy(partition,slot_height,maxp,minp,q):
	ts_ent = 0.00
	for it in range (0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		if(prob_m_l > 0):
			ts_ent = ts_ent - (pow(prob_m_l,q)-prob_m_l);
	ts_ent = ts_ent/(q-1)		
	return ts_ent

def Renyi_entropy(partition,slot_height,maxp,minp,alpha):
	p_ent = 0.00
	for it in range(0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		p = p + pow(prob_m_l,alpha)
	ren_ent = p/(1-alpha)
	return Renyi_entropy

q_range = [1.5,3,5]
for q in q_range:
	
	oo = 5
	#for oo in range (4.5,5):  #Change  #harsh
	## Reading the signal from a txt file
			#file_name = input("Data File: \n")
	file_name = 's'+str(oo%10)+'t'+str((oo//10) + 1)+'.txt'
	#legends.append(file_name)
	print(file_name)
	f = open (file_name , 'r')
		#print(f)
	sig = []
	xs =  []
	j=1
	for line in f:

		for word in line.split():	
						#print(word)
					sig.append(float(word))
	for i in range(1,len(sig)+1):
		xs.append(i)
	print (len(sig))	
	signal_entropy = sig_entropy(L,w,delta,sig)
	se = []
	te = []
	for seg in range (0,len(signal_entropy)-1):
		se.append(signal_entropy[seg][0])
		te.append(signal_entropy[seg][1])
			#print signal_entropy
			#print len(signal_entropy[0])
			#plt.plot(sig)
	M = len(signal_entropy)-1
	x = []

	for f in range (0,M) : 
		x.append(w + f*delta)
	plt.plot(x,ts_ent)
plt.legend(q_range)	
#plt.plot(sig)
plt.show()