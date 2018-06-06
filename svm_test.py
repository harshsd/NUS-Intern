#Apply and test the svm

from sklearn import svm
import os
import numpy as np
import matplotlib.pyplot as plt


def accuracy_svm (data_set1 , data_set2 , cc , gg):
	accuracy = []
	l = len(data_set1)
	fatigue_train1 = []
	fatigue_train2 = []
	fatigue_test1 = []
	fatigue_test2 = []
	if l != len (data_set2):
		print ("error")
		print (l)
		print (len(data_set2))
	for i in range (0,5):
		fatigue_trial1 = []
		fatigue_trial2 = []
		fatigue_test1 = []
		fatigue_test2 = []		
		test1 = data_set1[int(i*l/5):int((i+1)*l/5)]
		test2 = data_set2[int(i*l/5):int((i+1)*l/5)]
		if i == 0:
			train1 = data_set1[l/5:l]
			train2 = data_set2[l/5:l]
		elif i == 4 :
			train1 = data_set1[0:4*l/5]
			train2 = data_set2[0:4*l/5]	
		else:
			train1 = data_set1[0:i*l/5]
			train1 += data_set1[i*l/5:l]
			train2 = data_set2[0:i*l/5]
			train2 += data_set2[i*l/5:l]
		test1 += test2
		train1 += train2	
		for k in range (0,int(4*l/5)):
			fatigue_train1.append(0)
			fatigue_train2.append(1)
			if(k<int(l/5)):
				fatigue_test1.append(0)
				fatigue_test2.append(1)	
		fatigue_train1 += fatigue_train2
		fatigue_test1 += fatigue_test2 		
		clf = svm.SVC(kernel='rbf', C=cc, gamma = gg )				
		clf.fit (train1 , fatigue_train1)
		fatigue_result = clf.predict(test1)
		for i in range (0,len(fatigue_result)):
			if (fatigue_result[i] == fatigue_test[i]):
				y=y+1
			else:
				n=n+1
		accuracy.append (float(y/y+n))
	accuracy = np.array(accuracy)
	mean = accuracy.mean()
	std = accuracy.std()
	return (mean , std)			


#Get features in this part  should be an array of arrays or list of list with each small list containing features of one segment and many such lists
# Assumed final list os lists is in entropies_train[[]]
#For each list give in array fatigue =1 and not-fatigue=0
#Do_same for test data

mean_old = 0
for entropy in ["permut"]:#,"tsallis","renyi","permut"]:	
	for ccc in range (1,10):
		for ggg in range (1,10):
			cc = ccc/10
			gg = ggg/10
			print (cc,gg)
			mean_accuracies = []
			std_accuracies = []
			#print (entropy)
			accuracy = []
			accuracy_std = []
			for sub in range (1,26):
				for turn in range (1,3):
					data_set1 = []
					data_set2 = []
					for ch in range (1,25):
							os.chdir ('/media/harsh/DATA/Readable_Data/Entropies')
							file_name = entropy+"s"+str(sub)+"t"+str(turn)+"c"+str(ch)+".txt"
							# print (file_name)
							f = open (file_name , 'r')
							n = 0
							temp = []
							a=0
							for line in f:
								for word in line.split() :
									#a = a+1
									#print (a)
									#print (word)
									temp.append(str(float(word)))
							f.close()				
							data1 = temp[0:300]
							data2 = temp[len(temp)-300:len(temp)]
							data_set1.append(data1)
							data_set2.append(data2)
					data_set1 = np.array(data_set1)
					x , y = data_set1.shape
					if (y!=24):
						print ("error")
						print (y)
						print (x)
					data_set1 = data_set1.reshape((24,x))
					data_set2 = np.array(data_set2)
					x , y = data_set2.shape
					data_set2 = data_set2.reshape(y,x)
					mean , std = accuracy_svm(data_set1 , data_set2 , cc , gg)
					accuracy.append(mean)
					accuracy_std.append(std)
			accuracy = np.array(accuracy)				
			mean = accuracy.mean()
			if (mean > mean_old):
					mean_old = mean
					std = accuracy.std()
					print (mean,std,entropy)
			
			
			# mean_accuracies.append(mean)
			# std_accuracies.append(std)


# n = 4
# b = 0.35
# fig , ax = plt.subplots()
# index = np.arange(n)
# opacity = 0.5
# error_config = {'ecolor':'0.0'}
# rects1 = ax.bar (index, mean_accuracies, b, alpha=opacity, color='r', yerr=(0,0,0,0), error_kw=error_config,label='Mean accuracy')
# rects2 = ax.bar (index+b, std_accuracies, b, alpha=opacity, color='b', yerr=(0,0,0,0), error_kw=error_config,label='Standard Deviation of accuracies')
# ax.set_xlabel('Entropy')
# ax.set_ylabel('Value')
# ax.set_title('SVM Results')
# ax.set_xticks(index )
# ax.set_xticklabels(('Shannon','Tsallis','Renyi','Permutation'))
# ax.legend()
# fig.tight_layout()
# plt.show()	