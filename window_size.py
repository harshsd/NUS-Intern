from __future__ import division
import numpy as np
import math
from random import *
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import svm,datasets

L=10
delta=4000
q=3

file_name = input("Data File: \n")
f = open (file_name , 'r')
sig = []
xs =  []
j=1
for line in f:

	for word in line.split():	
				#print(word)
				sig.append(float(word))

for i in range(1,len(sig)+1):
	xs.append(i)

entropy = []

def partition_entropy( partition,L,q,maxp,minp):
	
		
		slot_height = (maxp-minp)/L
		#print slot_height
		ts_ent = Tsallis_entropy(partition,slot_height,maxp,minp,q)
		sh_ent = Shannon_entropy(partition,slot_height,maxp,minp)
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

for ww in range (1,len(sig)//1000):

	w = ww*1000
	print (w/len(sig))
	m = 0
	partition = sig[m*delta:(w+(m*delta))+1]
	maxp = np.amax(sig)
	minp = np.amin(sig)
	entropy.append(partition_entropy(partition,L,q,maxp,minp))
	se = []
	te = []
	for seg in range (0,len(entropy)-1):
		se.append(entropy[seg][0])
		te.append(entropy[seg][1])	
	M = len(entropy)-1
	x = []

	for f in range (0,M) : 
		x.append(w + f*delta)	
plt.plot(x , se)
#plt.holdon()	
plt.show()	