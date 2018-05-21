from __future__ import division
import numpy as np
import math
from random import *
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import svm,datasets
style.use("ggplot")

##Entropy calculations
def sig_entropy ( L , w, delta, sig):

	entropy = []
	K = len(sig)
	M = (K-w)//delta  # Should be an int
	maxp = np.amax(sig)
	minp = np.amin(sig)
	#print (maxp,minp)
	for m in range (0,M):
		partition = sig[m*delta:(w+(m*delta))+1]
		#print partition
		#print m
		#sh_entropy[m] = partition_entropy(partition,L,q)[0]
		#ts_entropy[m] = partition_entropy(partition,L,q)[0]
		entropy.append(partition_entropy(partition,L,q,maxp,minp))
		print(m/M)
	#print entropy
	return entropy

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


# Assume eeg is present in a vector sig
#L=10	#10             #10
w=256000   #128			#256000
delta=4000 #8			#8000
#For Tsallis entropy
# q= int(input("Enter q for Tsallis Entropy"))	#5 #1164500
q=3
# sig_len = 3072
# # sig = np.zeros(1024)
# # for j in range (0,1023):
# # 	sig[j] = random()
# sig = np.zeros(sig_len)
# for j in range (0,1023):
# 	sig[j] = random()
# for j in range (1024,2047):
# 	sig[j] = 0.5333
# for j in range (2048,3071):
# 	sig[j] = np.random.uniform(0,2)		

## Reading the signal from a txt file
file_name = input("Data File: \n")
# file_name = 's5t1.txt'
f = open (file_name , 'r')
print(f)
sig = []
xs =  []
j=1
for line in f:

	for word in line.split():	
				#print(word)
				sig.append(float(word))

for i in range(1,len(sig)+1):
	xs.append(i)

lenghts = [5,10,20,30]

for L in lenghts:
	#print sig
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





## Support vector machine implementation	
# train_len = int(M/10) + M - int(9*M/10)
# train_data = np.zeros((train_len,2))
# ind=0
# acc = 0
# se_train = []
# se_test = np.zeros((M-train_len,2))
# for k in range (0,int(M/10)):
# 	train_data[ind][0]=x[k]
# 	train_data[ind][1]=se[k]
# 	# train_data[ind][0]=se[k]
# 	# train_data[ind][1]=x[k]
# 	se_train.append(0)
# 	ind = ind+1
# for k in range (int(M/10),int(9*M/10)):
# 	se_test[acc][0] = x[k]
# 	se_test[acc][1] = se[k]
# 	acc = acc + 1
# for k in range (int(9*M/10),M):
# 	train_data[ind][0]=x[k]
# 	train_data[ind][1]=se[k]
# 	# train_data[ind][0]=se[k]
# 	# train_data[ind][1]=x[k]
# 	se_train.append(2)
# 	ind = ind+1
# clf = svm.SVC(kernel='linear',C = 1.0)
# # train_data = [[0,0],[1,1]]
# # yy = [0,1]
# # print train_data
# # print se_train
# # print se_test
# train_data_arr = np.array(train_data)
# clf.fit(train_data_arr,se_train)
# # se_test.reshape(1,-1)
# # a=[[2,50]]
# # a = []
# # print clf.predict(se_test)
# coef = clf.coef_[0]
# plotse = np.zeros((2,M-train_len))
# for l in range (0,acc-1):
# 	# print (se_test[l][0],se_test[l][1])
# 	plotse[0][l]=se_test[l][0]
# 	plotse[1][l]=se_test[l][1]
# lin_slope = -coef[0]/coef[1]
# xline = np.linspace(1075.8,1076.1)
# yline = lin_slope*xline - clf.intercept_[0]/coef[1]	
# print plotse	
# plt.plot(plotse[0],plotse[1],'ro')
# plt.plot(xline,yline,'g')
# plt.scatter(se_test[:,0],se_test[:,1],c='y')



#PLotting/Visualzing the data	
	#plt.plot(x,se)
	plt.plot(x,te)
	plt.legend(lenghts)
#plt.plot(sig)
plt.show()