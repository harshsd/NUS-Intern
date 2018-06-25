#Apply and test the svm

from sklearn import svm
import os
import numpy as np
import matplotlib.pyplot as plt



def accuracy_svm (data_set1 , data_set2 , cc , gg):
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
	print(entropy)							#(6.1,8.4)
	for cc in range(1,100):
		for gg in range (1,100):
	#print (cc,gg)
	#print (cc,gg)
			mean_accuracies = []
			std_accuracies = []
			#print (entropy)
			accuracy = []
			for sub in range (1,31):
				for turn in range (1,3):
					data_set1 = []
					data_set2 = []
					slopes = []
					for ch in range (1,25):
							os.chdir ('/media/harsh/DATA/Readable_Data/Entropies/')
							file_name = entropy+"s"+str(sub)+"t"+str(turn)+"c"+str(ch)+".txt"
							#print (file_name)
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
							line_channel = np.polyfit(np.arange(len(temp)),temp,1,full=True)
							slopes.append(line_channel[0][0])
							data1 = temp[0:300]
							data2 = temp[len(temp)-300:len(temp)]
							data_set1.append(data1)
							data_set2.append(data2)
					#print ("read")		
					data_set1 = np.array(data_set1)
					x , y = data_set1.shape
					#print (x,y)
					# if (y!=24):
					# 	print ("error")
					# 	print (y)
					# 	print (x)
					data_set1 = data_set1.reshape((y,x))
					data_set2 = np.array(data_set2)
					x , y = data_set2.shape
					#print (x,y)
					data_set2 = data_set2.reshape(y,x)
					#print (len(data_set2[0]))
					mean , std = accuracy_svm(data_set1 , data_set2 , cc , gg)
					accuracy.append(mean)
			#accuracy_std.append(std)
			accuracy = np.array(accuracy)		
			accuracy_std = accuracy.std()		
			mean = accuracy.mean()
			minn , maxx = (accuracy.min() , accuracy.max())
			#print (mean)
			if (mean > mean_old):
				cc_max = cc
				gg_max = gg
				mean_old = mean
				#print (cc_max,gg_max,mean,accuracy_std,entropy)
			print (cc,gg)
			print (cc_max,gg_max,mean,accuracy,entropy)	
			means.append(mean)
			sdeviations.append(accuracy_std)
			min_max.append(maxx-minn)	
	# print (result)
	# print (entropy + " done")		
			# mean_accuracies.append(mean)
			# std_accuracies.append(std)



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