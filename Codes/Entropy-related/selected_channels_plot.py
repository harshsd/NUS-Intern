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
            if (a[i2])<(a[i2+1]):
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