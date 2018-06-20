#Apply and test the svm

from sklearn import svm
import os
import numpy as np
import matplotlib.pyplot as plt


def read_file(file_name):
	f = open(file_name , 'r')
	vec = []
	for line in f:
		for word in line.split():
			vec.append(float(word))
	f.close()
	return vec


def accuracy_svm (data_set1 , data_set2 , data_set3 , cc , gg):
	accuracy = []
	l = len(data_set1)
	if l != len (data_set2):
		print ("error")
		print (l)
		print (len(data_set2))
	elif l != len(data_set3):
		print ("error")
		print (l)
		print (len(data_set3))	

	for i in range (0,5):
		fatigue_train1 = []
		fatigue_train2 = []
		fatigue_train3 = []
		fatigue_test1 = []
		fatigue_test2 = []	
		fatigue_test3 = []	
		test1 = data_set1[int(i*l/5):int((i+1)*l/5)]
		test2 = data_set2[int(i*l/5):int((i+1)*l/5)]
		test3 = data_set3[int(i*l/5):int((i+1)*l/5)]
		if i == 0:
			train1 = data_set1[int(l/5):l]
			train2 = data_set2[l//5:l]
			train3 = data_set3[l//5:l]
		elif i == 4 :
			train1 = data_set1[0:4*l//5]
			train2 = data_set2[0:4*l//5]	
			train3 = data_set3[0:4*l//5]
		else:
			train1 = data_set1[0:i*l//5]
			train1 = np.concatenate((train1,data_set1[(i+1)*l//5:l]),axis = 0)
			train2 = data_set2[0:i*l//5]
			train2 = np.concatenate((train2 ,data_set2[(i+1)*l//5:l]) , axis =0)
			train3 = data_set3[0:i*l//5]
			train3 = np.concatenate((train3 ,data_set3[(i+1)*l//5:l]) , axis =0)			
		test_final = np.concatenate((test1,test2,test3),axis=0)
		train_final = np.concatenate((train1,train2,train3), axis=0)
		# print (len(train1))
		# print (len(train2))
		# print (len(train3))
		# print (len(train_final))
		for k in range (0,int(4*l//5)):
			fatigue_train1.append(0)
			fatigue_train2.append(1)
			fatigue_train3.append(2)
			if(k<int(l//5)):
				fatigue_test1.append(0)
				fatigue_test2.append(1)	
				fatigue_test3.append(2)		
		fatigue_train1 += fatigue_train2
		fatigue_train1 += fatigue_train3
		fatigue_train = np.array(fatigue_train1)
		fatigue_test1 += fatigue_test2
		fatigue_test1 += fatigue_test3 		
		fatigue_test = np.array(fatigue_test1)
		# print(l)
		# print (np.array(train_final).shape)
		# print(fatigue_train.shape)
		clf = svm.SVC(kernel='rbf', C=cc, gamma = gg ,decision_function_shape='ovo')				
		clf.fit (train_final , fatigue_train)
		fatigue_result = clf.predict(test_final)
		y = 0
		n = 0
		for i in range (0,len(fatigue_result)):
			if (fatigue_result[i] == fatigue_test1[i]):
				y=y+1
			else:
				n=n+1
		accuracy_curr = y/(y+n)		
		accuracy.append (float(100*accuracy_curr))
	accuracy = np.array(accuracy)
	#print (accuracy)
	mean = accuracy.mean()
	std = accuracy.std()
	return (mean , std)			







means = []
sdeviations = []
legends = []
min_max = []
#Get features in this part  should be an array of arrays or list of list with each small list containing features of one segment and many such lists
# Assumed final list os lists is in entropies_train[[]]
#For each list give in array fatigue =1 and not-fatigue=0
#Do_same for test data
# band_name = input ("Enter band name: ")
mean_old = 0
cc_max , gg_max = (0,0)
entropy = input ("Enter entropy name: ")
#for entropy in ["shannon","tsallis","renyi" , "permut"]:
for just_for_fun in ["to avoid editing"]:
	print(entropy)							
	for cc in range(1,100):
		for gg in range (1,100):
			mean_accuracies = []
			std_accuracies = []
			accuracy = []
			for sub in range (1,8):
					data_set1 = []
					data_set2 = []
					data_set3 = []
					for ch in range (1,63):
							os.chdir ('G:/Harsh_Data_Backup/Data/New_Entropies_Data')
							file_name = entropy+"s"+str(sub)+"c"+str(ch)+".txt"
							#print (file_name)
							temp = read_file(file_name)				
							data1 = temp[0:60]
							data1 += temp[180:240]
							data1 += temp[360:420]
							data2 = temp[60:120]
							data2 += temp[240:300]
							data2 += temp[420:480]
							data3 = temp[120:180]
							data3 += temp[300:360]
							data3 += temp[480:540]
							data_set1.append(data1)
							data_set2.append(data2)	
							data_set3.append(data3)
					data_set1 = np.array(data_set1)
					x , y = data_set1.shape
					data_set1 = data_set1.reshape((y,x))
					data_set2 = np.array(data_set2)
					x , y = data_set2.shape
					data_set2 = data_set2.reshape((y,x))
					data_set3 = np.array(data_set3)
					x , y = data_set3.shape
					data_set3 = data_set3.reshape((y,x))
					mean , std = accuracy_svm(data_set1 , data_set2 , data_set3, cc , gg)
					accuracy.append(mean)
			accuracy = np.array(accuracy)		
			accuracy_std = accuracy.std()		
			mean = accuracy.mean()
			minn , maxx = (accuracy.min() , accuracy.max())
			if (mean > mean_old):
				cc_max = cc
				gg_max = gg
				mean_old = mean
				print (cc_max,gg_max,mean,accuracy_std,entropy)
			means.append(mean)
			sdeviations.append(accuracy_std)
			min_max.append(maxx-minn)	


# print (type(means[0]))
# n = 4
# b = 0.35
# fig , ax = plt.subplots()
# index = np.arange(n)
# opacity = 0.5
# error_config = {'ecolor':'0.0'}
# rects1 = ax.bar (index, means, b, alph10a=opacity, color='r', yerr=sdeviations, error_kw=error_config,label='Mean accuracy')
# #rects2 = ax.bar (index+b, means, b, alpha=opacity, color='b', yerr=min_max, error_kw=error_config,label='Standard Deviation of accuracies')
# ax.set_xlabel('Entropy')
# ax.set_ylabel('Accuracy')
# ax.set_title('SVM Results')
# ax.set_xticks(index )
# ax.set_xticklabels(('Shannon','Tsallis','Renyi','Permutation'))
# ax.legend()
# fig.tight_layout()
# plt.show()	