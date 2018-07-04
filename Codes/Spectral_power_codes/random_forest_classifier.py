from sklearn.ensemble import RandomForestClassifier
import numpy as np


def rfc(data_set1 , data_set2 , data_set3 , max_depth = 5 ,num_of_trees = 100, max_features = None):
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
		class_train = np.array(fatigue_train1)
		fatigue_test1 += fatigue_test2
		fatigue_test1 += fatigue_test3 		
		class_test = np.array(fatigue_test1)	
		

		clf = RandomForestClassifier(max_depth=max_depth,n_estimators=num_of_trees,max_features=max_features)	
		clf.fit(train_final,class_train)

		class_result = clf.predict(test_final)

		y = 0
		n = 0
		for i in range (0,len(class_result)):
			#print (fatigue_result[i])
			if (class_result[i] == class_test[i]):
				y=y+1
			else:
				n=n+1
		accuracy_curr = y/(y+n)
		#print (y,n)		
		accuracy.append (float(100*accuracy_curr))
	accuracy = np.array(accuracy)
	#print (accuracy)
	mean = accuracy.mean()
	std = accuracy.std()
	return (mean , std)	