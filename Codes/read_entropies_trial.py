# Read entropies and plot them along with variance and both best fit lines. Prints slopes of the best fit lines as well

import os
import numpy as np
import matplotlib.pyplot as plt
import scipy
from operator import sub


def array_reshape (array):
		ret_arr = np.zeros((24,30,2))
		for i in range (0,24):
			for j in range (0,30):
				for k in range (0,2):
					ret_arr[i][j][k] = array[j][k][i]	
		return ret_arr				

band_names = ["alpha","beta","delta"]#["alpha","beta","gamma","delta","theta"]
#Entropies read and stored here
for band_name in band_names:
	#Define arrays here
	permut = np.zeros((30,2,24))
	renyi = np.zeros((30,2,24))
	tsallis = np.zeros((30,2,24))
	shannon = np.zeros((30,2,24))
	entropy_names = ["shannon","tsallis", "renyi" , "permut"]

	#Change Dirctory Here
	os.chdir ("/media/harsh/DATA/Readable_Data/Entropies_new_filtered/"+band_name) 
	for ent in entropy_names:
		for sub in range (1,31):
		#print (sub)
			for turn in range (1,3):
				entropy_total = []
				for ch in range (1,25):
					entropy = []
					file_name = ent + "s" + str(sub) + "t" + str(turn) + "c" + str(ch) + ".txt"
					#print (file_name)
					f = open (file_name, "r")
					for line in f:
						for word in line.split():
							entropy.append(float(word))
					M = len (entropy)
					x = np.arange(M)
					entropy_total.append(entropy)
					if(ch == 1):
						print (len(entropy))
				entropy_total = np.array(entropy_total)		
				print (entropy_total.shape)

	


	# slopes = []
	# for sub in range (1,31):
	# 	for turn in range (1,3):
	# 		sig1 = []
	# 		sig2 = []
	# 		for ch in [5,19]:
	# 			file_name = "renyis" + str(sub) + "t" + str(turn) + "c" + str(ch) + ".txt"
	# 			f = open(file_name , "r")
	# 			for line in f:
	# 				for word in line.split():
	# 					if (ch == 5):
	# 						sig1.append(float(word))
	# 					elif (ch == 19):
	# 						sig2.append(float(word))
	# 		new_sig = []				
	# 		for i in range (0,len(sig1)):				
	# 		  new_sig.append(sig1[i])
	# 		plt.plot(sig1)
	# 		plt.show() 				
	# 		M = len (new_sig)	
	# 		x = np.arange(M)
	# 		line = np.polyfit(x , new_sig, 1, full=True)
	# 		slopes.append(line[0][0])	
			

# 	permut = np.array(permut)
# 	permut = array_reshape(permut)
# 	renyi = np.array(renyi)
# 	renyi = array_reshape(renyi)
# 	tsallis = np.array(tsallis)
# 	tsallis = array_reshape(tsallis)
# 	shannon = np.array(shannon)
# 	shannon = array_reshape(shannon)

# 	permut_mean = []	
# 	shannon_mean = []
# 	renyi_mean = []
# 	tsallis_mean = []
# 	rstd  = []
# 	tstd = []
# 	sstd = []
# 	pstd = []

# 	#print (len (permut[0]))

# 	for ch in range(1,25):
# 		permut_mean.append(abs(np.mean(permut[ch-1])))
# 		renyi_mean.append(abs(np.mean(renyi[ch-1])))
# 		tsallis_mean.append(abs(np.mean(tsallis[ch-1])))
# 		shannon_mean.append(abs(np.mean(shannon[ch-1])))
# 		rstd.append(np.std(renyi[ch-1]))
# 		tstd.append(np.std(tsallis[ch-1]))
# 		sstd.append(np.std(shannon[ch-1]))
# 		pstd.append(np.std(permut[ch-1]))

# 	# print (np.mean(slopes))
# 	# print (np.std(slopes))
# 	# Plot means with channels
# 	# plt.figure(num = band_name)
# 	# # plt.plot(shannon_mean)
# 	# plt.plot(tsallis_mean)
# 	# plt.plot(renyi_mean)
# 	# # plt.plot(permut_mean)
# 	# # plt.plot(permut_mean)
# 	# # plt.plot(sstd)
# 	# plt.plot(tstd)
# 	# plt.plot(rstd)
# 	# # plt.plot(pstd)
# 	# legend1 = ["t","r","td","rd"]
# 	# plt.legend(legend1)
# 	# plt.plot(slopes)
# 	#legend = ["shannon "+band_name,"tsallis","renyi","sstd","tstd","rstd"]
# 	#plt.figure()
# 	# print (type(means[0]))
# 	print (len(renyi_mean))
# 	n = 24
# 	b = 0.15
# 	fig , ax = plt.subplots()
# 	index = np.arange(n)
# 	opacity = 0.5
# 	error_config = {'ecolor':'0.0'}
# 	rects1 = ax.bar (index, renyi_mean, b, alpha=opacity, color='r' , error_kw=error_config,label='Mean')
# 	rects2 = ax.bar (index+b, rstd, b, alpha=opacity, color='b' , error_kw=error_config,label='Standard Deviation')
# 	ax.set_xlabel('Channel')
# 	ax.set_ylabel('Slope')
# 	ax.set_title('Tracking task results for ' + band_name + " renyi")
# 	ax.set_xticks(index )
# 	ax.set_xticklabels(np.arange(1,25,1))
# 	ax.legend()
# 	fig.tight_layout()

# 	n = 24
# 	b = 0.15
# 	fig , ax = plt.subplots()
# 	index = np.arange(n)
# 	opacity = 0.5
# 	error_config = {'ecolor':'0.0'}
# 	rects1 = ax.bar (index, tsallis_mean, b, alpha=opacity, color='r' , error_kw=error_config,label='Mean')
# 	rects2 = ax.bar (index+b, tstd, b, alpha=opacity, color='b' , error_kw=error_config,label='Standard Deviation')
# 	ax.set_xlabel('Channel')
# 	ax.set_ylabel('Slope')
# 	ax.set_title('Tracking task results for ' + band_name + " tsallis")
# 	ax.set_xticks(index )
# 	ax.set_xticklabels(np.arange(1,25,1))
# 	ax.legend()
# 	fig.tight_layout()

# plt.show()