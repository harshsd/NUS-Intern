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
        os.chdir("G:/Harsh_Data_Backup/Readable_Data/Entropies_2_S")
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
        os.chdir("G:/Harsh_Data_Backup/Readable_Data/PICTURES/"+entropy)
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
print ("Average of good slopes is : "+str(sum_of_good_slopes/negative))
print ("positive is : "+str(positive) + " and negative is : "+str(negative))   
print (ch_score)
print (sorted_array_with_indices(ch_score))   
print (np.sum(ch_score))  
# plt.figure("Channel Info")        
# plt.plot(np.arange(len(channel_counter)),channel_counter)