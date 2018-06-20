import os
os.chdir('/home/harsh/Desktop/Harsh_Deshpande/Readable_Data')

for sub in range (4,31):
	for ch in range (1,25):
		for turn in range (1,3):
			if(sub==2 & turn==2):
				a=0
			else:	
				file_name = 's'+str(sub)+'t'+str(turn)+'c'+str(ch)+'.txt'
				print (file_name)
				f = open (file_name , 'r')
				sig = []
				j=1
				for line in f:
					for word in line.split():	
						sig.append(float(word))
				print(len(sig))		



				#s2t2 s3t2 