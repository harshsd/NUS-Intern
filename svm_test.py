#Apply and test the svm

from sklearn import svm
import os
import numpy as np
import matplotlib.pyplot as plt

#Get features in this part  should be an array of arrays or list of list with each small list containing features of one segment and many such lists
# Assumed final list os lists is in entropies_train[[]]
#For each list give in array fatigue =1 and not-fatigue=0
#Do_same for test data

mean_old = 0
for entropy in ["permut"]:#,"tsallis","renyi","permut"]:	
	for ccc in range (1,100):
		for ggg in range (1,100):
			cc = ccc/10
			gg = ggg/10
			print (cc,gg)
			mean_accuracies = []
			std_accuracies = []
			#print (entropy)
			accuracy = []
			for sub in range (1,26):
				for turn in range (1,3):
					entropies_train = []
					entropies_test = []
					fatigue_train = []
					fatigue_test = []
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
							#print (temp)		
							temp2 = temp[0:300] 
							temp2 += temp[len(temp)-300:len(temp)]
							temp3 = temp[300:400]
							temp3 += temp[len(temp)-400:len(temp)-300]
							#temp3 = temp2
							# print(len (temp3))
							entropies_train.append(temp2)	
							entropies_test.append(temp3)	
							#print (len(temp2))
							# print (len(entropies_train))

					#print (entropies_train[0])
					entropies_train = np.array(entropies_train)
					entropies_test = np.array(entropies_test)
					# print(entropies_train.shape)
					entropies_train = entropies_train.transpose()
					entropies_test = entropies_test.transpose()
					#print (entropies_train.shape)
					# print(len(entropies_test[0]))
					for i in range (0,300):
						fatigue_train.append(0)
					for j in range (0,300):
						fatigue_train.append(1)	
					for k in range (0,100):               #CHANGE_HERE!!!!!!!!!
						fatigue_test.append(0)
					for l in range (0,100):
						fatigue_test.append(1)		

					#print (entropies_train[0])


					#accuracy = 0.0
					#Apply SVM  
					#Best yet c=0.01 gamma=0.646 75.5  0.1 0.52 76
					# for c in range (1,10):
					# 	for gamma in range (1,1000):
					# 		gg = gamma/100
					# 		cc = c/10

					# cc = 0.1
					# gg = 0.52
					clf = svm.SVC(kernel='rbf', C=cc, gamma = gg )
					clf.fit(entropies_train,fatigue_train)  


					#test the result
					fatigue_result = clf.predict(entropies_test)
					y=0
					n=0
					for i in range (0,len(fatigue_result)):
						if (fatigue_result[i] == fatigue_test[i]):
							y=y+1
						else:
							n=n+1
							#print (fatigue_test[i])
					#accuracy_new = 0.00		
					accuracy_new = float((y/(y+n)))*100		
			# if (accuracy_new > accuracy):
			# 	accuracy = accuracy_new
			# 	print (cc,gg)
			# 	print (y)
			# 	print (n)
			# 	print (accuracy)
					accuracy.append(accuracy_new)
					# os.chdir('/media/harsh/DATA/Readable_Data/Results_unfiltered/SVM')
					# writing = open ("svm_results.txt","a+")
					# writing.write("renyi \n")
					# writing.write(str(accuracy_new))
					# writing.write("\n")
					# writing.close()
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