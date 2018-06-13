import numpy as np
import itertools

def permutation_entropy(time_series, m, delay):
    """Calculate the Permutation Entropy
    Args:
        time_series: Time series for analysis
        m: Order of permutation entropy
        delay: Time delay
    Returns:
        Vector containing Permutation Entropy
    Reference:
        [1] Massimiliano Zanin et al. Permutation Entropy and Its Main Biomedical and Econophysics Applications:
            A Review. http://www.mdpi.com/1099-4300/14/8/1553/pdf
        [2] Christoph Bandt and Bernd Pompe. Permutation entropy — a natural complexity
            measure for time series. http://stubber.math-inf.uni-greifswald.de/pub/full/prep/2001/11.pdf
        [3] http://www.mathworks.com/matlabcentral/fileexchange/37289-permutation-entropy/content/pec.m
    """
    n = len(time_series)
    permutations = np.array(list(itertools.permutations(range(m))))
    c = [0] * len(permutations)

    for i in range(n - delay * (m - 1)):
        # sorted_time_series =    np.sort(time_series[i:i+delay*m:delay], kind='quicksort')
        sorted_index_array = np.array(np.argsort(time_series[i:i + delay * m:delay], kind='quicksort'))
        for j in range(len(permutations)):
            if abs(permutations[j] - sorted_index_array).any() == 0:
                c[j] += 1

    c = [element for element in c if element != 0]
    p = np.divide(np.array(c), float(sum(c)))
    pe = -sum(p * np.log(p))
    return pe

a = [4,7,9,10,6,11,3]
print (permutation_entropy(a,3,1))   
print (shannon_entropy(a)) 


## Support vector machine implementation    
# train_len = int(M/10) + M - int(9*M/10)
# train_data = np.zeros((train_len,2))
# ind=0
# acc = 0
# se_train = []
# se_test = np.zeros((M-train_len,2))
# for k in range (0,int(M/10)):
#   train_data[ind][0]=x[k]
#   train_data[ind][1]=se[k]
#   # train_data[ind][0]=se[k]
#   # train_data[ind][1]=x[k]
#   se_train.append(0)
#   ind = ind+1
# for k in range (int(M/10),int(9*M/10)):
#   se_test[acc][0] = x[k]
#   se_test[acc][1] = se[k]
#   acc = acc + 1
# for k in range (int(9*M/10),M):
#   train_data[ind][0]=x[k]
#   train_data[ind][1]=se[k]
#   # train_data[ind][0]=se[k]
#   # train_data[ind][1]=x[k]
#   se_train.append(2)
#   ind = ind+1
# clf = svm.SVC(kernel='linear',C = 1.0)
# # train_data = [[0,0],[1,1]]
# # yy = [0,1]
# # print train_data
# # print se_train
# # print se_test
# train_data_arr = np.array(train_data)
# clf.fit(train_data_arr,se_train)
# # se_test.reshape(1,-1)
# # a=[[2,50]]
# # a = []
# # print clf.predict(se_test)
# coef = clf.coef_[0]
# plotse = np.zeros((2,M-train_len))
# for l in range (0,acc-1):
#   # print (se_test[l][0],se_test[l][1])
#   plotse[0][l]=se_test[l][0]
#   plotse[1][l]=se_test[l][1]
# lin_slope = -coef[0]/coef[1]
# xline = np.linspace(1075.8,1076.1)
# yline = lin_slope*xline - clf.intercept_[0]/coef[1]   
# print plotse  
# plt.plot(plotse[0],plotse[1],'ro')
# plt.plot(xline,yline,'g')
# plt.scatter(se_test[:,0],se_test[:,1],c='y')
