import os
import numpy
import scipy
import matplotlib.pyplot as plt


def read_file(file_name):
	f = open(file_name , 'r')
	vec = []
	for line in f:
		for word in line.split():
			vec.append(float(word))
	f.close()
	return vec

count = 0
os.chdir ("G:/Harsh_Data_Backup/Readable_Data/chaninfo")
a = read_file("s1t1chaninfo.txt")
print (len(a))
x = []
for i in range(0,len(a)):
	count = count +1
	if a[i]==1:
		x.append(count)
print (len(x))		
#print (x)
#Make the array for x coordinate of entropy

os.chdir("G:/Harsh_Data_Backup/Readable_Data/Unfiltered_Data")
sig = read_file("s4t2c18.txt")
print(len(sig))

#SUCCESS