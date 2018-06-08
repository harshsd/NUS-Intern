# Read entropies and plot them along with variance and both best fit lines. Prints slopes of the best fit lines as well

import os
import numpy as np
import matplotlib.pyplot as plt
import scipy


#Change Dirctory Here
os.chdir ("/media/harsh/DATA/Readable_Data/Entropies_new") 

#Define arrays here
permut = np.zeros((30,2,24))
renyi = np.zeros((30,2,24))
tsallis = np.zeros((30,2,24))
shannon = np.zeros((30,2,24))
entropy_names = ["shannon","tsallis", "renyi" , "permut"]


#Entropies read and stored here
for sub in range (1,31):
	print (sub)
	for turn in range (1,3):
		for ch in range (1,25):
			for ent in entropy_names:
				entropy = []
				file_name = ent + "s" + str(sub) + "t" + str(turn) + "c" + str(ch) + ".txt"
				#print (file_name)
				f = open (file_name, "r")
				for line in f:
					for word in line.split():
						entropy.append(float(word))
				M = len (entropy)
				x = np.arange(M)

				line = np.polyfit ( x, entropy , 1 , full=True)

				if ent == "shannon":
					shannon[sub-1][turn-1][ch-1] = line[0][0]
				elif ent == "tsallis":
					tsallis[sub-1][turn-1][ch-1] = line[0][0]
				elif ent == "renyi":
					renyi[sub-1][turn-1][ch-1] = line[0][0]
				elif ent == "permut":
					permut[sub-1][turn-1][ch-1] = line[0][0]		

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
		

permut = np.array(permut)
permut = permut.reshape((24,30,2))
renyi = np.array(renyi)
renyi = renyi.reshape((24,30,2))
tsallis = np.array(tsallis)
tsallis = tsallis.reshape((24,30,2))
shannon = np.array(shannon)
shannon = shannon.reshape((24,30,2))

permut_mean = []
shannon_mean = []
renyi_mean = []
tsallis_mean = []
rstd  = []
tstd = []
sstd = []

for ch in range(1,25):
	permut_mean.append(abs(np.mean(permut[ch-1])))
	renyi_mean.append(abs(np.mean(renyi[ch-1])))
	tsallis_mean.append(abs(np.mean(tsallis[ch-1])))
	shannon_mean.append(abs(np.mean(shannon[ch-1])))
	rstd.append(np.std(renyi[ch-1]))
	tstd.append(np.std(tsallis[ch-1]))
	sstd.append(np.std(shannon[ch-1]))

# print (np.mean(slopes))
# print (np.std(slopes))
# # Plot means with channels
# plt.plot(shannon_mean)
# plt.plot(tsallis_mean)
plt.plot(renyi_mean)
# plt.plot(permut_mean)
# plt.plot(sstd)
# plt.plot(tstd)
plt.plot(rstd)
# plt.plot(slopes)
# legend = ["shannon","tsallis","renyi","sstd","tstd","rstd"]
# plt.legend(legend)
plt.show()