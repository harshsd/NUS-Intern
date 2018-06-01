from __future__ import division
import numpy as np
import math
from random import *
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import svm,datasets
import os
import itertools


style.use("ggplot")
os.chdir('/home/harsh/Desktop/Harsh_Deshpande/Readable_Data')


#Constants
w_in_s = 0.5
del_in_s = 0.5
L=5	#10             #10
w=int(w_in_s*250)   #128			#256000
delta=int(del_in_s*250) #8			#8000
q=3
alpha = 0.5
d = 2
delay = 1


##Entropy calculations
def sig_entropy ( L , w, delta, sig, entropy_name):
	#entropy_name = shannon/tsallis/renyi/permutation

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
		entropy.append(partition_entropy(partition,L,q,entropy_name))
	#print entropy
	return entropy

def partition_entropy( partition,L,q,entropy_name):
	
		maxp = np.amax(partition)
		minp = np.amin(partition)
		slot_height = (maxp-minp)/L
		#print slot_height
		if (entropy_name == "shannon"):
			sh_ent = Shannon_entropy(partition,slot_height,maxp,minp)
			return sh_ent
		elif (entropy_name == "tsallis"):
			ts_ent = Tsallis_entropy(partition,slot_height,maxp,minp,q)
			return ts_ent
		elif (entropy_name == "renyi"):
			ren_ent= Renyi_entropy(partition,slot_height,maxp,minp,alpha)
			return ren_ent				
		elif (entropy_name == "permutation"):
			per_ent = permutation_entropy(partition,d,delay)	
			return per_ent
		else:
			return -1
		#print (sh_ent,ts_ent)
		#return (sh_ent,ts_ent,ren_ent)
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
		p_ent = p_ent + pow(prob_m_l,alpha)
	ren_ent = p_ent/(1-alpha)
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
	


shannon_slope_array = []
tsalllis_slope_array = []
renyi_slope_array = []
permutation_slope_array = []

for sub in range (1,31):
	for ch in range (1,25):
		for turn in range (1,3):	
			file_name = 's'+str(sub)+'t'+str(turn)+'c'+str(ch)+'.txt'
			print (file_name)
			f = open (file_name , 'r')
			sig = []
			j=1
			for line in f:
				for word in line.split():	
					sig.append(float(word))

			sh_ent = sig_entropy(L,w,delta,sig,"shannon")
			te_ent = sig_entropy(L,w,delta,sig,"tsallis")
			ren_ent= sig_entropy(L,w,delta,sig,"renyi")
			per_ent= sig_entropy(L,w,delta,sig,"permutation")
			
			M = len(sh_ent)
			print (M)
			x = np.arange(M)

			shannon_line = np.polyfit(x, sh_ent, 1, full=True)
			shannon_slope = shannon_line[0][0]

			tsallis_line = np.polyfit(x , te_ent , 1, full = True)
			tsalllis_slope = tsallis_line[0][0]

			renyi_line = np.polyfit(x, ren_ent, 1 , full=True)
			renyi_slope = renyi_line [0][0]

			permutation_line = np.polyfit (x, per_ent, 1, full=True)
			permutation_slope = permutation_line[0][0]

			shannon_slope_array.append(shannon_slope)
			tsalllis_slope_array.append(tsalllis_slope)
			renyi_slope_array.append(renyi_slope)
			permutation_slope_array.append(permutation_slope)


#PLotting/Visualzing the data	
print (np.sum(shannon_slope_array))
print (np.sum(tsalllis_slope_array))
print (np.sum(renyi_slope_array))
print (np.sum(permutation_slope_array))


legend = ["shannon","tsallis","renyi","permutation"]
plt.plot(shannon_slope_array)
plt.plot(tsalllis_slope_array)
plt.plot(renyi_slope_array)
plt.plot(permutation_slope_array)
plt.legend(legend)
plt.show()