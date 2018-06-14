#generate_data_for_svm
from sklearn import svm,datasets
import numpy as np 
import scipy
import matplotlib.pyplot as plt
import os
import itertools
import math


w_in_s = 2
del_in_s = 2
L=10
w=int(w_in_s*250)   #128			#256000
delta=int(del_in_s*250) #8			#8000				this is for Unfilterd Data
q=2
alpha = 0.3
d = 3
delay = 2

# w_in_s = 10
# del_in_s = 10
# L=20	#10             #10
# w=int(w_in_s*250)   #128			#256000						this is for Unfiltered)Data_1
# delta=int(del_in_s*250) #8			#8000
# q=0.8
# alpha = 0.75
# d = 2
# delay = 1

def read_file(file_name):
	f = open(file_name , 'r')
	vec = []
	for line in f:
		for word in line.split():
			vec.append(float(word))
	f.close()
	return vec

def sig_entropy ( L , w, delta, sig, entropy_name,q,alpha,d,delay):
	#entropy_name = shannon/tsallis/renyi/permutation

	entropy = []
	K = len(sig)
	M = (K-w)//delta  # Should be an int
	M = int(M)
	print (M)
	#print (maxp,minp)
	for m in range (0,M):
		partition = sig[m*delta:(w+(m*delta))+1]
		entropy.append(partition_entropy(partition,L,q,entropy_name,alpha,d,delay))
		#print(m/M)
		# print(entropy_name)
	return entropy

def partition_entropy( partition,L,q,entropy_name,alpha,d,delay):
	
		maxp = np.amax(partition)
		minp = np.amin(partition)
		slot_height = (maxp-minp)/L
		#print slot_height
		if (entropy_name == "shannon"):
			sh_ent = Shannon_entropy(L,partition,slot_height,maxp,minp)
			return sh_ent
		elif (entropy_name == "tsallis"):
			ts_ent = Tsallis_entropy(L,partition,slot_height,maxp,minp,q)
			return ts_ent
		elif (entropy_name == "renyi"):
			ren_ent= Renyi_entropy(L,partition,slot_height,maxp,minp,alpha)
			return ren_ent				
		elif (entropy_name == "permutation"):
			per_ent = permutation_entropy(L,partition,d,delay)	
			return per_ent
		else:
			return -1
		#print (sh_ent,ts_ent)
		#return (sh_ent,ts_ent,ren_ent)
		#amplitude intervals defined as [minp+ (k) (slot_height) , minp + (k+1) (slot_height)] k belongs to 0 to L-1
		#Number of s(k) in partition is w

def P_m_l(partition,k,slot_height,maxp,minp): #k from 0 to L-1

		count = 0
		w = len(partition)
		#print(w)
		for i in range (0,w-1):
			if ((partition[i] >= minp + k*(slot_height)) & (partition[i] <= minp + (k+1)*(slot_height))):
					count = count + 1
		#print count
		#print (count/w)			
		return (count/w)

def Shannon_entropy(L,partition,slot_height,maxp,minp):
	sh_ent = 0.00
	for it in range (0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		if(prob_m_l > 0):
			sh_ent = sh_ent - (prob_m_l*math.log(prob_m_l));
	#print sh_ent		
	return sh_ent
	
def Tsallis_entropy(L,partition,slot_height,maxp,minp,q):
	ts_ent = 0.00
	for it in range (0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		if(prob_m_l > 0):
			ts_ent = ts_ent - (pow(prob_m_l,q)-prob_m_l);
	ts_ent = ts_ent/(q-1)		
	return ts_ent

def Renyi_entropy(L,partition,slot_height,maxp,minp,alpha):
	p_ent = 0.00
	for it in range(0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		p_ent = p_ent + pow(prob_m_l,alpha)
	ren_ent = p_ent/(1-alpha)
	return ren_ent

def permutation_entropy(L,time_series, m, delay):
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
    pe = -sum(p*np.log(p))
    return pe


if __name__ == '__main__':
	#band_name = input("Enter band name: (alpha,beta,delta,theta,gamma)")
	entropy_name = input("Enter Entropy Name: (s,t,r,p)")
	#for band_name in ["theta"]:#"alpha","beta","delta","theta",
	for sub in range (1,31):
			for ch in range (1,25):
				for turn in range (1,3):   
					os.chdir('G:/Harsh_Data_Backup/Readable_Data/Unfiltered_Data')
					file_name = 's'+str(sub)+'t'+str(turn)+'c'+str(ch)+'.txt'  #change_here
					print (file_name)
					sig = read_file(file_name)
					os.chdir('G:/Harsh_Data_Backup/Readable_Data/Entropies_2_S')
					if (entropy_name == "s"):
						sh_ent = sig_entropy(L,w,delta,sig,"shannon",q,alpha,d,delay)
						print (w)
						print (delta)
						print (len(sig))
						print (float((len(sig)-w)/delta))
						print("shannon")
						file_name = 'shannons'+str(sub)+'t'+str(turn)+'c'+str(ch)+'.txt'
						file = open (file_name,'a+')
						M = len(sh_ent)
						print (M)
						for i in range (0,M):
							file.write(str(sh_ent[i]))
							file.write('\n')
						file.close()		

					elif (entropy_name == "t"):		
						te_ent = sig_entropy(L,w,delta,sig,"tsallis",q,alpha,d,delay)
						print("tsallis")
						file_name = 'tsalliss'+str(sub)+'t'+str(turn)+'c'+str(ch)+'.txt'
						file = open (file_name,'a+')
						M = len(te_ent)
						for i in range (0,M):
								file.write(str(te_ent[i]))
								file.write('\n')
						file.close()

					elif (entropy_name == "r"):
						
						ren_ent= sig_entropy(L,w,delta,sig,"renyi",q,alpha,d,delay)
						print("renyi")
						file_name = 'renyis'+str(sub)+'t'+str(turn)+'c'+str(ch)+'.txt'
						file = open (file_name,'a+')
						M = len (ren_ent)
						for i in range (0,M):
								file.write(str(ren_ent[i]))
								file.write('\n')
						file.close()

					elif (entropy_name == "p"):	
						per_ent= sig_entropy(L,w,delta,sig,"permutation",q,alpha,d,delay)
						print("permutation")		
						M = len (per_ent)
						file_name = 'permuts'+str(sub)+'t'+str(turn)+'c'+str(ch)+'.txt'
						file = open (file_name,'a+')
						for i in range (0,M):
							file.write(str(per_ent[i]))
							file.write('\n')														
						file.close()		
#testt