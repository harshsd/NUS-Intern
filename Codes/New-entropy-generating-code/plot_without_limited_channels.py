import matplotlib.pyplot as plt
import os
import numpy as np
import time


def sorted_array_with_indices(b):
	a = b
	l = len(a)
	x = np.arange(l)
	x = x+1
	for i1 in range (0,l-1):
		#print (i1)
		for i2 in range (0,l-1-i1):
			#print(i2)
			if a[i2]>a[i2+1]:
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




# c = [5,35,44,-20,66,121,22,11,8]
# b = []
# for x in range (0,len(c)):
# 	b.append(c[x])
# res,ind = sorted_array_with_indices(b)
# print (c)
# print (res)
# print (ind)



entropy = input("Enter entropy to plot: ")
total_slopes = []
means = []
stds = []
ch_specific=[]

for sub in range (1,8):
	os.chdir("G:/Harsh_Data_Backup/Data/New_Entropies_Data")
	subject_slope = []
	total_sig1 = []
	total_sig2 = []
	total_sig3 = []
	slope_weights = np.zeros((3,62))
	for ch in range (1,63):
		sig = read_file(entropy+"s"+str(sub)+"c"+str(ch)+".txt")
		if len(sig) != 540:
			print ("error")
		else:

			sig1 = sig[0:180]
			sig2 = sig[180:360]
			sig3 = sig[360:540]
			total_sig1.append(sig1)
			total_sig2.append(sig2)
			total_sig3.append(sig3)
			x = np.arange(180)
			line1 = np.polyfit(x,sig1,1,full=True)
			slope1 = line1[0][0]
			line2 = np.polyfit(x,sig2,1,full=True)
			slope2 = line2[0][0]
			line3 = np.polyfit(x,sig3,1,full=True)
			slope3 = line3[0][0]
			slope_weights[0][ch-1]=abs(slope1)
			slope_weights[1][ch-1]=abs(slope2)
			slope_weights[2][ch-1]=abs(slope3)
			
			slope = np.array([slope1,slope2,slope3])

			subject_slope.append(slope)
	subject_slope = np.array(subject_slope)
	#print(subject_slope.shape)
	total_slopes.append(subject_slope)
	slope_weights = np.array(slope_weights)
	trial = np.copy(slope_weights)
	trial1 , trialx1 = sorted_array_with_indices(trial[0])
	trial2 , trialx2 = sorted_array_with_indices(trial[1])
	trial3 , trialx3 = sorted_array_with_indices(trial[2])
	print ("Subject "+str(sub)+":")
	print (trialx1)
	print (trialx2)
	print (trialx3)
	#print (slope_weights[0])
	# for kkk in range (0,2):
	# 	slope_weights[kkk] = slope_weights[kkk]/np.sum(slope_weights[kkk])
	 
	# total_sig1 = np.array(total_sig1)
	# total_sig2 = np.array(total_sig2)
	# total_sig3 = np.array(total_sig3)
	# print (total_sig1.shape)
	# final_sig1 = np.zeros(180)
	# final_sig2 = np.zeros(180)
	# final_sig3 = np.zeros(180)
	# for chan in range (0,62):
	# 	final_sig1 = final_sig1 + slope_weights[0][chan]*total_sig1[chan]
	# 	final_sig2 = final_sig2 + slope_weights[1][chan]*total_sig2[chan]
	# 	final_sig3 = final_sig3 + slope_weights[2][chan]*total_sig3[chan]
	#time.sleep(15)
# 	os.chdir("G:/Harsh_Data_Backup/Data/Results_photos/"+entropy)
# 	plt.figure("sub "+str(sub)+"trial 1")
# 	plt.plot(final_sig1)
# 	plt.savefig("sub "+str(sub)+"trial 1.png")
# 	plt.figure("sub "+str(sub)+"trial 2")
# 	plt.plot(final_sig2)
# 	plt.savefig("sub "+str(sub)+"trial 2.png")	
# 	plt.figure("sub "+str(sub)+"trial 3")
# 	plt.plot(final_sig3)
# 	plt.savefig("sub "+str(sub)+"trial 3.png")	
# plt.show()




# for subject in range (0,7):
# 	for ch in range(0,62):
# 		final_slopes[ch][3*subject]=total_slopes[subject][ch][0]
# 		final_slopes[ch][3*subject+1]=total_slopes[subject][ch][1]
# 		final_slopes[ch][3*subject+2]=total_slopes[subject][ch][2]
# for ch in range (0,62):
# 	slopes = final_slopes[ch]
# 	mean = abs(slopes.mean())
# 	std = slopes.std()
# 	means.append(mean)
# 	stds.append(std)
# plt.plot(means)
# plt.plot(stds)	
# plt.figure()
# plt.plot(ch_specific)					
# plt.show()