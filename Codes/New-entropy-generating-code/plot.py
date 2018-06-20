import matplotlib.pyplot as plt
import os
import numpy as np

def read_file(file_name):
	f = open(file_name , 'r')
	vec = []
	for line in f:
		for word in line.split():
			vec.append(float(word))
	f.close()
	return vec

os.chdir("G:/Harsh_Data_Backup/Data/New_Entropies_Data")
entropy = input("Enter entropy to plot: ")
total_slopes = []
means = []
stds = []
ch_specific=[]
for sub in range (1,8):
	subject_slope = []
	for ch in range (1,63):
		sig = read_file(entropy+"s"+str(sub)+"c"+str(ch)+".txt")
		if len(sig) != 540:
			print ("error")
		else:
			sig1 = sig[0:180]
			sig2 = sig[180:360]
			sig3 = sig[360:540]
			x = np.arange(180)
			line1 = np.polyfit(x,sig1,1,full=True)
			slope1 = line1[0][0]
			line2 = np.polyfit(x,sig2,1,full=True)
			slope2 = line2[0][0]
			line3 = np.polyfit(x,sig3,1,full=True)
			slope3 = line3[0][0]
			if(ch==15):
				ch_specific.append(slope1)
				ch_specific.append(slope2)
				ch_specific.append(slope3)
			slope = np.array([slope1,slope2,slope3])
			#print (slope)
			#print (slope.mean())
			#print (slope.std())
			subject_slope.append(slope)
	subject_slope = np.array(subject_slope)
	#print(subject_slope.shape)
	total_slopes.append(subject_slope)
total_slopes = np.array(total_slopes)
print (total_slopes.shape)			
final_slopes = np.zeros((62,21))
for subject in range (0,7):
	for ch in range(0,62):
		final_slopes[ch][3*subject]=total_slopes[subject][ch][0]
		final_slopes[ch][3*subject+1]=total_slopes[subject][ch][1]
		final_slopes[ch][3*subject+2]=total_slopes[subject][ch][2]
for ch in range (0,62):
	slopes = final_slopes[ch]
	mean = abs(slopes.mean())
	std = slopes.std()
	means.append(mean)
	stds.append(std)
plt.plot(means)
plt.plot(stds)	
plt.figure()
plt.plot(ch_specific)					
plt.show()