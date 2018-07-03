import read_write as rw
import filter_bands as filt
import os
import sys
import numpy as np

# delta_f = (0.1,4)
# theta_f = (4,7)
# alpha_f = (8 ,12)
# beta_f = (12,30)
# gamma_f = (30,100)

sample_freq = 256
low_f = 0
high_f = 100
band_name = input("Enter band name (d,t,a,b,g): ")

if(band_name=="d"):
	low_f = 0.1
	high_f = 4
elif(band_name=="t"):
	low_f = 4
	high_f = 7
elif(band_name=="a"):
	low_f=8
	high_f=12
elif(band_name=="b"):
	low_f=12
	high_f=30
elif(band_name=="g"):
	low_f=30
	high_f=100	
else:
	print ("error")
	sys.exit()	

for sub in range (1,8):
	for ch in range (1,63):
		os.chdir("G:/Harsh_Data_Backup/Data/New_Data")
		file_name = "s"+str(sub)+"c"+str(ch)+".txt"
		sig = np.array(rw.read_file(file_name))
		filtered_sig = []
		filtered_sig = np.array(filtered_sig)
		for i in range (0,540):
			segment = sig[i*512:(i+1)*512]
			filt_segment=filt.butter_filter(segment,sample_freq,low_f,high_f)
			#print ((type(filtered_sig),type(filt_segment)))
			filtered_sig = np.concatenate((filtered_sig,filt_segment),axis=0)
		os.chdir("G:/Harsh_Data_Backup/Data/New_Data_filtered/"+band_name)
		rw.write_to_file(file_name,filtered_sig)
		print (sub,ch,band_name)	

