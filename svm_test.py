#Apply and test the svm

from sklearn import svm
import os
import numpy as np

#Get features in this part  should be an array of arrays or list of list with each small list containing features of one segment and many such lists
# Assumed final list os lists is in entropies_train[[]]
#For each list give in array fatigue =1 and not-fatigue=0
#Do_same for test data

os.chdir ('/media/harsh/DATA/Readable_Data/Entropies')
sub = 1
entropies_train = []
entropies_test = []
fatigue_train = []
fatigue_test = []
for ch in range (1,25):
	for turn in range (1,2):
		file_name = "renyis1t"+str(turn)+"c"+str(ch)+".txt"
		print (file_name)
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
		#print (temp)		
		temp2 = temp[0:200] 
		temp2 += temp[len(temp)-200:len(temp)]
		temp3 = temp[200:300]
		temp3 += temp[len(temp)-300:len(temp)-200]
		# print(len (temp3))
		entropies_train.append(temp2)	
		entropies_test.append(temp3)	
		#print (len(temp2))
		# print (len(entropies_train))

print (entropies_train[0])
entropies_train = np.array(entropies_train)
entropies_test = np.array(entropies_test)
# print(entropies_train.shape)
entropies_train = entropies_train.transpose()
entropies_test = entropies_test.transpose()
print (entropies_train.shape)
# print(len(entropies_test[0]))
for i in range (0,200):
	fatigue_train.append(0)
for j in range (0,200):
	fatigue_train.append(1)	
for k in range (0,100):
	fatigue_test.append(0)
for l in range (0,100):
	fatigue_test.append(1)		

print (entropies_train[0])


accuracy = 0.0
#Apply SVM  
#Best yet c=0.01 gamma=0.646 75.5  0.1 0.52 76
for c in range (1,10):
	for gamma in range (1,1000):
		gg = gamma/100
		cc = c/10
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
		accuracy_new = 0.00		
		accuracy_new = float((y/(y+n)))*100		
		if (accuracy_new > accuracy):
			accuracy = accuracy_new
			print (cc,gg)
			print (y)
			print (n)
			print (accuracy)
				