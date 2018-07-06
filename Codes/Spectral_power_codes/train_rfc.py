from sklearn.ensemble import RandomForestClassifier as RFC
import numpy as np
import time

def train(train_data_arr,class_arr,min_trees,max_trees,min_depth,max_depth,max_features="auto"):
	trees_step = int((max_trees-min_trees)/10)
	depth_step = int((max_depth-min_depth)/10)

	max_train_acc = 0
	trained_rfc = None

	for i in range (0,11): #change 
		for j in range (0,11): #change
			trees = min_trees + trees_step
			depth = min_depth + depth_step
			clf = RFC(max_depth=depth,n_estimators=trees,max_features=max_features)
			clf.fit(train_data_arr,class_arr)
			class_result = clf.predict(train_data_arr)
			acc = 0
			for k in range(0,len(class_result)):
				if(class_result[k]==class_arr[k]):
					acc = acc + 1/len(class_arr)
			if(acc>max_train_acc):
				max_train_acc = acc*100	
				trained_rfc = clf	
	#print (max_train_acc)			
	return (trained_rfc)


def get_arrays(data_set1,data_set2,data_set3,i):
		l = len(data_set1)
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
		return(train_final,test_final,class_train,class_test)


def final_accuracy(dataset1,dataset2,dataset3):
	start_time = time.time()
	acc_mean = 0
	for i in range (0,5):
		(train_final,test_final,class_train,class_test) = get_arrays(dataset1,dataset2,dataset3,i)
		model = train(train_final,class_train,min_trees=100,max_trees=1000,min_depth=10,max_depth=20)
		class_result = model.predict(test_final)
		acc = 0
		for k in range(0,len(class_result)):
			if(class_result[k]==class_test[k]):
					acc = acc + 1
		acc = acc*100/len(class_test)			
		acc_mean = acc_mean + acc/5	
		print ("percentage done: "+str(20*i)+"%")
		end_time = time.time()
		print (end_time-start_time)		
	return acc_mean			


