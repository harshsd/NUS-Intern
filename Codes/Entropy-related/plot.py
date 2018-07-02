from __future__ import division
import numpy as np
import math
from random import *
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import svm,datasets
import os
import itertools
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import time

def rolling_mean (a,n):
    a = np.array(a)
    l = len(a)
    rolling_mean = []
    for start in range (0,l-n+1):
        part_sum = 0
        for k in range (0,n):
            part_sum += a[start+k]
        rolling_mean.append(part_sum/n)
    return np.array(rolling_mean)       


def sorted_array_with_indices(b):
    a = b
    l = len(a)
    x = np.arange(l)
    x = x
    for i1 in range (0,l-1):
        #print (i1)
        for i2 in range (0,l-1-i1):
            #print(i2)
            if abs(a[i2])<abs(a[i2+1]):
                #print ("exchanged")
                temp = a[i2]
                a[i2]=a[i2+1]
                a[i2+1]=temp
                temp = x[i2]
                x[i2]=x[i2+1]
                x[i2+1]=temp        
    return (a,x)            


def read_file(file_name):
    f = open(file_name , 'r')
    vec = []
    for line in f:
        for word in line.split():
            vec.append(float(word))
    f.close()
    return vec

ch_score = np.zeros((24))
sum_of_slopes = 0
sum_of_good_slopes = 0
positive = 0
negative = 0
entropy = input("Enter entropy name: ")
band = input ("Enter band name: ")
total_slopes = []
means = []
stds = []
ch_specific=[]
channel_counter = np.zeros((24))   
var_final = [] 
for sub in range (1,31):
    for turn in range (1,3):
        print ("sub , turn :"+str((sub,turn)))
        total_sig = []
        os.chdir("G:/Harsh_Data_Backup/Readable_Data/Entropies_2_S_filtered/"+band)
        turn_slope=[]
        slope_weights = np.zeros((24))
        for ch in range (1,25):
            sig = read_file(entropy+"s"+str(sub)+"t"+str(turn)+"c"+str(ch)+".txt")
            x = np.arange(len(sig))
            line = np.polyfit(x,sig,1,full=True)
            slope = line[0][0]
            slope_weights[ch-1] = (slope)
            total_sig.append(sig)
        copy_weights = np.copy(slope_weights)
        sweights , xsweights = sorted_array_with_indices(copy_weights)
        for j in range (0,24):
            ch_score[xsweights[j]] += j
        #time.sleep(500)
        final_sig = np.zeros(len(sig))
        no_of_significant_channels = 5
        significant_weights = []
        for chc in range (0,no_of_significant_channels):
            significant_weights.append(sweights[chc])
            channel_counter[xsweights[chc]] += 1
        significant_weights = np.array(significant_weights)
        significant_weights = significant_weights/np.sum(abs(significant_weights))
        # print (slope_weights)
        # print (sweights)
        # print (significant_weights)
        time.sleep(1)
        for chc in range (0,no_of_significant_channels):
            for j in range (0,len(sig)):
                final_sig[j] = final_sig[j] + significant_weights[chc]*total_sig[xsweights[chc]][j]
        mov_avg_n = 1000
        rolling_sig = rolling_mean(final_sig,mov_avg_n)
        xfinal = np.arange(len(rolling_sig))       
        final_line = np.polyfit(xfinal,rolling_sig,1,full=True)        
        yfinal = (xfinal*final_line[0][0]) + final_line[0][1]
        var = 0
        for k in range (0,len(rolling_sig)):
            var = var + abs(rolling_sig[k]-yfinal[k])
        os.chdir("G:/Harsh_Data_Backup/Readable_Data/PICTURES/filtered/"+band+"/"+entropy)
        plt.figure("sub "+str(sub)+"turn"+str(turn)+" rolling mean")
        plt.plot(xfinal,rolling_sig)
        plt.plot(xfinal,yfinal)
        print(final_line[0][0])
        sum_of_slopes += (final_line[0][0])
        if(final_line[0][0]>0):
            positive += 1
            sum_of_good_slopes += final_line[0][0]
        else :
            negative += 1    
        plt.savefig("sub "+str(sub)+"turn"+str(turn)+" rolling mean.png")
        plt.close("sub "+str(sub)+"turn"+str(turn)+" rolling mean")
        var_final.append(var)
plt.figure()
plt.plot(np.arange(len(var_final)),var_final,marker = 'o')
plt.savefig("variance.jpg")
print (channel_counter)
print (np.sum(channel_counter))
print ("Average slope is: "+str(sum_of_slopes/60))
print ("Average of good slopes is : "+str(sum_of_good_slopes/positive))
print ("positive is : "+str(positive) + " and negative is : "+str(negative))   
print (ch_score)
print (sorted_array_with_indices(ch_score))   
print (np.sum(ch_score))  
print (entropy , band)
# plt.figure("Channel Info")        
# plt.plot(np.arange(len(channel_counter)),channel_counter)
'''
shannon:
	alpha :[20, 23, 11,  9, 13, 22,  2, 10,  8,  7, 12,  0, 16,  6,  3, 19,  5, 4, 15, 21, 14,  1, 18, 17]
	beta :[11,  9,  1, 14,  8, 16,  3, 22,  2, 18,  4, 23,  5, 19,  0, 21, 13, 17,  7, 20, 10, 12,  6, 15]
	gamma :[17, 22, 13, 11, 16,  8, 20,  1, 19, 18, 21,  3,  9, 23,  2, 14,  4, 0, 12,  5,  6,  7, 10, 15]
	theta :[16, 19, 20,  8, 22,  9, 14, 23, 12,  3, 18,  4, 15,  6, 10, 17,  5, 13,  7,  0, 21, 11,  2,  1]
	delta : [23, 20, 19, 11, 10, 14, 21, 16,  4,  7,  9,  2, 22,  8,  5, 13,  3, 12, 17, 18,  0,  1,  6, 15]
tsallis:
	alpha : [13, 23,  9, 11, 20, 22, 10,  2,  8,  0,  7,  5, 16,  6, 12, 19,  4, 21,  3, 14, 15,  1, 18, 17]
	beta : [11,  1,  9, 14,  8, 22,  2, 16,  3, 18, 23, 19,  5,  4, 10,  0, 21, 20, 13, 12,  7, 17,  6, 15]
	gamma : [17, 16, 13, 22, 11,  8, 19, 18, 20,  1, 21,  3,  9,  4,  2, 14, 23, 0, 12,  5,  6,  7, 10, 15]
	theta :[19, 16,  8,  3,  9, 20, 22, 14, 18, 13,  4, 12, 15,  6,  7, 17, 23, 0, 10,  5,  1,  2, 21, 11]
	delta :[14,  7,  9, 23, 11, 10,  8,  2, 20, 19,  0, 16, 21, 12,  3, 22, 18, 4,  6,  1, 13, 15, 17,  5]
renyi:
	alpha: [11, 23, 20,  9, 22, 13,  2,  7, 10, 16, 12,  8,  0,  6, 19,  3, 21, 15,  5, 14,  4, 18,  1, 17]
	beta : [ 9, 11, 14,  8,  1,  3,  2, 16, 22, 19, 23, 17,  4, 18,  5, 21, 13, 0, 20,  7, 10, 12, 15,  6]
	theta : [16, 19,  8, 23,  9, 14, 22, 20, 12, 18,  3,  4, 10,  6, 15, 13, 17, 5,  0, 21,  7, 11,  2,  1]
	delta : [23, 20, 19,  4, 14, 11,  9,  7, 10, 16,  8, 22,  2, 17,  5, 12, 21, 13,  1, 18,  0,  3,  6, 15]
	gamma : [17, 22, 13, 11, 16,  8, 20, 14, 21, 19,  1, 23,  9, 18,  3,  4,  2, 0, 12,  6,  7,  5, 10, 15]
'''