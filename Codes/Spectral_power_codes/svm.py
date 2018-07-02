from sklearn import svm
import os
import numpy as np
import matplotlib.pyplot as plt


def accuracy_svm (data_set1 , data_set2 , cc , gg):
	'''Returns average accuracy of a svm after doing 5 fold validation on the given datasets.Uses rbf kernel. To edit change on line 53
	Args:
		data_set1 : The first data_set. All the inputs should have same number of features. Also each of them should belong to the same class.
		data_set2 : The second data_set. All inputs should have same number of features. Each should belong to same class other than that of data_set1. Also, lenght of the dataset must be same as the previous data_set.
		cc: C for kernal
		gg: gamma for kernel
		More datasets can be easily added for multiclass svm. See next function (commented) for an example.
	Returns:
		Tuple containing mean accuracy of selected svm and standard deviation of the included accuracies.'''	
	accuracy = []
	l = len(data_set1)
	if l != len (data_set2):
		print ("error")
		print (l)
		print (len(data_set2))
	for i in range (0,5):
		fatigue_train1 = []
		fatigue_train2 = []
		fatigue_test1 = []
		fatigue_test2 = []		
		test1 = data_set1[int(i*l/5):int((i+1)*l/5)]
		test2 = data_set2[int(i*l/5):int((i+1)*l/5)]
		#print(type(test1))
		if i == 0:
			train1 = data_set1[int(l/5):l]
			train2 = data_set2[l//5:l]
		elif i == 4 :
			train1 = data_set1[0:4*l//5]
			train2 = data_set2[0:4*l//5]	
		else:
			train1 = data_set1[0:i*l//5]
			train1 = np.concatenate((train1,data_set1[(i+1)*l//5:l]),axis = 0)
			train2 = data_set2[0:i*l//5]
			train2 = np.concatenate((train2 ,data_set2[(i+1)*l//5:l]) , axis =0)
		test1 = np.concatenate((test1,test2),axis=0)
		train1 = np.concatenate((train1,train2), axis=0)
		#print (test1.shape)
		#print (len(test1[0]))	
		for k in range (0,int(4*l//5)):
			fatigue_train1.append(0)
			fatigue_train2.append(1)
			if(k<int(l//5)):
				fatigue_test1.append(0)
				fatigue_test2.append(1)	
		#print (len(fatigue_train1))		
		fatigue_train1 += fatigue_train2
		fatigue_train = np.array(fatigue_train1)
		#print (len(fatigue_train))
		fatigue_test1 += fatigue_test2 		
		fatigue_test = np.array(fatigue_test1)
		#print (len(fatigue_test))
		clf = svm.SVC(kernel='rbf', C=cc, gamma = gg )				
		clf.fit (train1 , fatigue_train1)
		fatigue_result = clf.predict(test1)
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


'''
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
'''		