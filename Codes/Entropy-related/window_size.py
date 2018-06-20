from __future__ import division
import numpy as np
import math
from random import *
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import svm,datasets
import os
import itertools

os.chdir('/home/harsh/Desktop/Harsh_Deshpande/Readable_Data')
L=10
delta=25
q=3
alpha = 0.5


def partition_entropy( partition,L,q):
	
		maxp = np.amax(partition)
		minp = np.amin(partition)
		slot_height = (maxp-minp)/L
		#print slot_height
		ts_ent = Tsallis_entropy(partition,slot_height,maxp,minp,q)
		sh_ent = Shannon_entropy(partition,slot_height,maxp,minp)
		re_ent = Renyi_entropy(partition,slot_height,maxp,minp,alpha)
		pe_ent = permutation_entropy(partition,2,1)
		#print (sh_ent,ts_ent)
		return [sh_ent,ts_ent,re_ent,pe_ent]
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
	p = 0.00
	for it in range(0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		p = p + pow(prob_m_l,alpha)
	ren_ent = p/(1-alpha)
	return ren_ent

def permutation_entropy(time_series, m, delay):
    """Calculate the Permutation Entropy
    Args:
        time_series: Time series for analysis
        m: Order of permutation entropy
        delay: Time delay
    Returns:
        Vector containing Permutation Entropy
    Reference:
        [1] Massimiliano Zanin et al. Permutation Entropy and Its Main Biomedical and Econophysics Applications:
            A Review. http://www.mdpi.com/1099-4300/14/8/1553/pdf
        [2] Christoph Bandt and Bernd Pompe. Permutation entropy — a natural complexity
            measure for time series. http://stubber.math-inf.uni-greifswald.de/pub/full/prep/2001/11.pdf
        [3] http://www.mathworks.com/matlabcentral/fileexchange/37289-permutation-entropy/content/pec.m
    """
    n = len(time_series)
    permutations = np.array(list(itertools.permutations(range(m))))
    c = [0] * len(permutations)

    for i in range(n - delay * (m - 1)):
        # sorted_time_series =    np.sort(time_series[i:i+delay*m:delay], kind='quicksort')
        sorted_index_array = np.array(np.argsort(time_series[i:i + delay * m:delay], kind='quicksort'))
        for j in range(len(permutations)):
            if abs(permutations[j] - sorted_index_array).any() == 0:
                c[j] += 1

    c = [element for element in c if element != 0]
    p = np.divide(np.array(c), float(sum(c)))
    pe = -sum(p * np.log(p))
    return pe	

labels = []
sub = input("subject: \n")
for ch in range (1,25):
	labels.append('se'+str(ch))
	labels.append('te'+str(ch))
	labels.append('re'+str(ch))
	labels.append('pe'+str(ch))
	print(ch)
	file_name = 's'+sub+'t1c'+str(ch)+'.txt'
	#file_name = 's5t1.txt'
	f = open (file_name , 'r')
	sig = []
	se =  []
	te = []
	ren = []
	pe =[]
	j=1
	for line in f:	
		for word in line.split():	
					#print(word)
					sig.append(float(word))
	for w in range (1,510):
		
		m = 1
		partition = sig[m*delta:(w+(m*delta))+1]	
		parti_ent = partition_entropy(partition , L ,q)
		se.append(parti_ent[0])
		te.append(parti_ent[1])
		ren.append(parti_ent[2])
		pe.append(parti_ent[3])
	plt.plot (se)
	plt.plot(te)
	plt.plot(ren)
	plt.plot(pe)
plt.legend(labels)
	#plt.holdon()	
plt.show()	