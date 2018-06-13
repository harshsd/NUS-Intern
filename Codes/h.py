from __future__ import division
import numpy as np
import math
from random import *
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import svm,datasets
from scipy import stats
import os
import itertools

style.use("ggplot")
# os.chdir('/home/harsh/Desktop/Harsh_Deshpande/Readable_Data')


# Assume eeg is present in a vector sig


#Constants
'''w and alpha are the window lenghts and window shift for time dependent entropy calculations. 
L is the number of intervals in which he amplitude is divided
q is the q-index for tsallis entropy
alpha is alpha for renyi entropy
d and delay are parameters for permutation entropy'''

w_in_s = 2
del_in_s = 2
L=5	#10             #10
w=int(w_in_s*250)   #128			#256000
alpha=int(del_in_s*250) #8			#8000
q=3
alpha = 0.5
d = 3
delay = 2
	



##Entropy calculations
def sig_entropy ( L , w, alpha, sig, entropy_name):
	#entropy_name = shannon/tsallis/renyi/permutation

	entropy = []
	K = len(sig)
	M = (K-w)//delta  # Should be an int
	M = int (M)
	#print (maxp,minp)
	for m in range (0,M):
		partition = sig[m*alpha:(w+(m*alpha))+1]
		entropy.append(partition_entropy(partition,L,q,entropy_name))
		# print(m/M)
		# print(entropy_name)
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
    pe = -sum(pow(p,alpha)/(1-alpha))
    return pe
	

s_v_slope = []
t_v_slope = []
r_v_slope = []
per_v_slope = []

#sub = int(input("Enter Subject number: \n"))

for sub in range (1,31):
	for ch in range (1,25):
		for turn in range (1,3):
			## Reading the signal from a txt file
			os.chdir('/media/harsh/DATA/Readable_Data/Gamma')
			file_name = 'gammas'+str(sub)+'t'+str(turn)+'c'+str(ch)+'.txt'  #change_here
			print (file_name)
			f = open (file_name , 'r')
			sig = []
			j=1
			for line in f:

				for word in line.split():	
							#print(word)
							sig.append(float(word))

			# sh_ent = sig_entropy(L,w,alpha,sig,"shannon")
			# print("shannon")
			# te_ent = sig_entropy(L,w,alpha,sig,"tsallis")
			# print("tsallis")
			ren_ent= sig_entropy(L,w,alpha,sig,"renyi")
			print("renyi")
			# per_ent= sig_entropy(L,w,alpha,sig,"permutation")
			# print("permutation")
			#print signal_entropy
			#print len(signal_entropy[0])
			#plt.plot(sig)
			M = len(ren_ent)  # Lenght of all entropies is the same
			x = np.arange(M)
			# plt.plot(ren_ent)
			# plt.show()




			# Calculating and printing entropies

			# shannon_line = np.polyfit(x, sh_ent, 1, full=True)
			# shannon_slope = shannon_line[0][0]

			# tsallis_line = np.polyfit(x , te_ent , 1, full = True)
			# tsallis_slope = tsallis_line[0][0]

			renyi_line = np.polyfit(x, ren_ent, 1 , full=True)
			renyi_slope = renyi_line [0][0]

			# permutation_line = np.polyfit (x, per_ent, 1, full=True)
			# permutation_slope = permutation_line[0][0]

			os.chdir('/media/harsh/DATA/Readable_Data/Results_Filtered/Gamma')

			# print("shannon")
			# shannon_file = open ("gamma_shannon_slopes.txt",'a+')		#change here
			# shannon_file.write(str(shannon_slope))
			# shannon_file.write("\n")
			# shannon_file.close()
			# print("tsallis")
			# tsallis_file = open ("gamma_tsallis_slopes.txt",'a+')
			# tsallis_file.write(str(tsallis_slope))
			# tsallis_file.write("\n")
			# tsallis_file.close()
			print("renyi")
			renyi_file = open ("gamma_renyi_slopes1.txt",'a+')
			renyi_file.write(str(renyi_slope))
			renyi_file.write("\n")
			renyi_file.close()
			# print("permutation")
			# permutation_file = open ("gamma_permutation_slopes.txt",'a+')
			# permutation_file.write(str(permutation_slope))
			# permutation_file.write("\n")
			# permutation_file.close()

			sh_ent_var = []
			tsa_ent_var = []
			ren_ent_var = []
			per_ent_var = []


			for start in range (0,M-100):
			# 	per_ent_var.append(np.var(per_ent[start:start+100	]))
				ren_ent_var.append(np.var(ren_ent[start:start+100	]))
				# tsa_ent_var.append(np.var(te_ent[start:start+100	]))
				# sh_ent_var.append(np.var(sh_ent[start:start+100	]))
			# plt.plot(ren_ent_var)
			# plt.show()	

			# variance_line_per = np.polyfit (np.arange(len(per_ent_var)),per_ent_var,1,full=True)
			# variance_slope_per = variance_line_per[0][0]
			# per_v_slope.append(variance_slope_per)
			#xx = np.arange(len(per_ent_var))
			#yy_per = variance_line_per[0][0]*xx + variance_line_per[0][1]

			# variance_line_sh = np.polyfit (np.arange(len(sh_ent_var)),sh_ent_var,1,full=True)
			# variance_slope_sh = variance_line_sh[0][0]
			# s_v_slope.append(variance_slope_sh)
			#yy_sh = variance_line_sh[0][0]*xx + variance_line_sh[0][1]

			# variance_line_te = np.polyfit (np.arange(len(tsa_ent_var)),tsa_ent_var,1,full=True)
			# variance_slope_te = variance_line_te[0][0]
			# t_v_slope.append(variance_slope_te)
			#yy_tsa = variance_line_te[0][0]*xx + variance_line_te[0][1]

			variance_line_ren = np.polyfit (np.arange(len(ren_ent_var)),ren_ent_var,1,full=True)
			variance_slope = variance_line_ren[0][0]
			r_v_slope.append(variance_slope)
			#yy_ren = variance_line_ren[0][0]*xx + variance_line_ren[0][1]

			# shannon_file = open ("gamma_shannon_slopes_var.txt",'a+')		#change_here
			# shannon_file.write(str(variance_slope_sh))
			# shannon_file.write("\n")
			# shannon_file.close()
			# tsallis_file = open ("gamma_tsallis_slopes_var.txt",'a+')
			# tsallis_file.write(str(variance_slope_te))
			# tsallis_file.write("\n")
			# tsallis_file.close()
			renyi_file = open ("gamma_renyi_slopes_var1.txt",'a+')
			renyi_file.write(str(variance_slope))
			renyi_file.write("\n")
			renyi_file.close()
			# permutation_file = open ("gamma_permutation_slopes_var.txt",'a+')
			# permutation_file.write(str(variance_slope))
			# permutation_file.write("\n")
			# permutation_file.close()


# 			print(s_v_slope)
# 			print ("\n")
# print(t_v_slope)
# print(r_v_slope)
# print(per_v_slope)			

#PLotting/Visualzing the data	
#plt.plot(x,sef,'k')
#plt.plot(x,tef,'r')
# plt.figure(1)
# plt.subplot(211)
# plt.plot (x,se,'r')
# plt.plot(x,re,'b')
# plt.plot(x,te,'y')
# plt.plot(x,sef)
# plt.subplot(212)
# plt.plot (sig,'b')
# #plt.plot(sig)
# plt.subplot(211)
# plt.plot(xx,yy_sh)
# plt.plot(xx,yy_tsa)
# plt.plot(xx,yy_ren)
# plt.plot(xx,yy_per)
# legend = ["shannon","tsallis","renyi","permutation"]
# plt.legend(legend)

# plt.subplot(212)
# plt.plot(ren_ent_var)
# plt.show()
# plt.plot(s_v_slope)
# plt.plot(t_v_slope)
# plt.plot(r_v_slope)
# plt.plot(per_v_slope)
# legend = ["shannon","tsallis","renyi","permutation"]
# plt.legend(legend)
# plt.show()