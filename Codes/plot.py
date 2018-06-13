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

Entropy = "Beta"
entropy = "beta"

os.chdir('/media/harsh/DATA/Readable_Data/Results_Filtered/'+Entropy)
#print ('/media/harsh/DATA/Readable_Data/Results_Filtered/'+Entropy)

s_slopes = []
t_slopes = []
r_slopes = []
p_slopes = []

f = open (entropy+'_shannon_slopes_var.txt','r')
for line in f:
    for word in line.split():
        s_slopes.append(float(word))
f.close()

f = open (entropy+'_tsallis_slopes_var.txt','r')
for line in f:
    for word in line.split():
        t_slopes.append(float(word))
f.close()

f = open (entropy+'_renyi_slopes_var.txt','r')
for line in f:
    for word in line.split():
    	try:
    		#r_slopes.append(float(line.split()[0].split('[')[1].split(',')[0]))
    		r_slopes.append(float(word))
    	except:
    		pass
f.close()

f = open (entropy+'_permutation_slopes_var.txt','r')
for line in f:
    for word in line.split():
        p_slopes.append(float(word))
f.close()

means = []
means.append(abs(np.average(s_slopes)))
means.append(abs(np.average(t_slopes)))
means.append(abs(np.average(r_slopes)))
means.append(abs(np.average(p_slopes)))

std = []
std.append(np.std(s_slopes))
std.append(np.std(t_slopes))
std.append(np.std(r_slopes))
std.append(np.std(p_slopes))

print (means)
print (std)



n = 4
b = 0.35
fig , ax = plt.subplots()
index = np.arange(n)
opacity = 0.5
error_config = {'ecolor':'0.0'}
rects1 = ax.bar (index, means, b, alpha=opacity, color='r', yerr=(0,0,0,0), error_kw=error_config,label='Mean slope')
rects1 = ax.bar (index+b, std, b, alpha=opacity, color='b', yerr=(0,0,0,0), error_kw=error_config,label='Standard Deviation')
ax.set_xlabel('Entropy')
ax.set_ylabel('Value')
ax.set_title('Mean slopes')
ax.set_xticks(index )
ax.set_xticklabels(('Shannon','Tsallis','Renyi','Permutation'))
ax.legend()
fig.tight_layout()
plt.show()
