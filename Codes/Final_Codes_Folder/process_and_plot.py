#Codes for processing the calculated entropies

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import os


def rolling_mean (input_sig,n):
	'''Calculates the rolling mean of an array
	Args:
	input_sig:List/array whose mean is to be calculated
	n:The window size to be considered while calculating rolling mean.Should be greater than 0 and less than or equal to the lenght of signal
	Returbs:
	npArray with rolling mean of input signal'''

    input_sig = np.array(input_sig)
    l = len(a)
    rolling_mean = []
    for start in range (0,l-n+1):
        part_sum = 0
        for k in range (0,n):
            part_sum += input_sig[start+k]
        rolling_mean.append(part_sum/n)
    return np.array(rolling_mean) 

def sorted_array_with_indices(b):
	'''Returns sorted array and indices of orignal positions
	Args:
	b = input_array
	Returns:
	Tuple with first element as sorted array and second containing array with indices of orignal positions'''
	
	b = np.array(b)
    a = np.copy(b)
    l = len(a)
    x = np.arange(l)
    #x = x
    for i1 in range (0,l-1):
        #print (i1)
        for i2 in range (0,l-1-i1):
            #print(i2)
            if (a[i2])<(a[i2+1]):
                #print ("exchanged")
                temp = a[i2]
                a[i2]=a[i2+1]
                a[i2+1]=temp
                temp = x[i2]
                x[i2]=x[i2+1]
                x[i2+1]=temp        
    return (a,x)        

def plot(sig_ent):
    '''Plots the signal using matplotlib'''
    plt.figure()
    plt.plot(sig_ent)
    plt.show()
