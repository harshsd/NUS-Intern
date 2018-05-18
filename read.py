import numpy
import matplotlib.pyplot as plt
f = open ('s8t2.txt' , 'r')
print(f)
input_data = []
x =  []
j=1
for line in f:
	# if j>1 :
	# 	if j <250:

	for word in line.split():	
				#print(word)
		input_data.append(float(word))
				#print(float(word))
#	j=j+1		
for i in range(1,len(input_data)+1):
	x.append(i)
print(input_data)	
plt.plot(x,input_data)
plt.show()
