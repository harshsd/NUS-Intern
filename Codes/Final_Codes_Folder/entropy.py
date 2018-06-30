#Codes for all entropies

def sig_entropy ( L , w, delta, sig, entropy_name,q,alpha,d,delay):
	''' Calaculates one type of entropy of a discrete time signal
	Args:
	L : Number of partitions of amplitude
	w : Width of the moving window
	delta : Step size of the window
	sig : Time series whose entropy is to be found
	entropy_name : Name of entropy. Currently shannon/renyi/tsallis/permutation are available
	q : q for tsallis.Only if entropy is tsallis
	alpha : alpha for renyi
	d,delay : d,delay for permutation

	Returns:
	An array with the entropy values '''

	entropy = []
	K = len(sig)
	M = (K-w)//delta  # Should be an int
	M = int(M)     #Lenght of output sorted_index_array
	#print (M)
	for m in range (0,M):
		partition = sig[m*delta:(w+(m*delta))+1]
		entropy.append(partition_entropy(partition,L,q,entropy_name,alpha,d,delay))
	return entropy



def partition_entropy( partition,L,q,entropy_name,alpha,d,delay):
	'''Calculates entropy a time series considering it as one partition.
		Args:
		partition : The signal/partition whose entropy is to be found
		L : Number of partitions of amplitude
		w : Width of the moving window
		delta : Step size of the window
		entropy_name : Name of entropy. Currently shannon/renyi/tsallis/permutation are available
		q : q for tsallis.Only if entropy is tsallis
		alpha : alpha for renyi
		d,delay : d,delay for permutation

		Returns:
		A single float value containing the entropy the signal'''
		
		maxp = np.amax(partition)
		minp = np.amin(partition)
		slot_height = (maxp-minp)/L
		#print slot_height
		if (entropy_name == "shannon"):
			sh_ent = Shannon_entropy(L,partition,slot_height,maxp,minp)
			return sh_ent
		elif (entropy_name == "tsallis"):
			ts_ent = Tsallis_entropy(L,partition,slot_height,maxp,minp,q)
			return ts_ent
		elif (entropy_name == "renyi"):
			ren_ent= Renyi_entropy(L,partition,slot_height,maxp,minp,alpha)
			return ren_ent				
		elif (entropy_name == "permutation"):
			per_ent = permutation_entropy(L,partition,d,delay)	
			return per_ent
		else:
			return -1	

def P_m_l(partition,k,slot_height,maxp,minp): #k from 0 to L-1
		'''Calaculates probability of the signal being in one part of the partition
		Args:
		partition : input signal
		k: Defines the part of the partition. Should be between 0 and L-1
		slot_height: Height of each slot/part of the partition
		maxp,minp : Maximum and Minimum values in the signal
		Return:
		Single float value containing probability of signal being in that slot of the partition'''

		count = 0
		w = len(partition)
		for i in range (0,w-1):
			if ((partition[i] >= minp + k*(slot_height)) & (partition[i] <= minp + (k+1)*(slot_height))):
					count = count + 1			
		return (count/w)	


def Shannon_entropy(L,partition,slot_height,maxp,minp):
	'''Returns Shannon entropy of a signal
	Args: 
	L : Number of partitions of amplitude
	partition: Time series whose entropy is to be found
	slot_height: Height of each slot/part of the partition
	maxp,minp : Maximum and Minimum values in the signal
	Returns:
	Float value containing shannon entropy'''

	sh_ent = 0.00
	for it in range (0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		if(prob_m_l > 0):
			sh_ent = sh_ent - (prob_m_l*math.log(prob_m_l));		
	return sh_ent
	
def Tsallis_entropy(L,partition,slot_height,maxp,minp,q):
	'''Returns Tsallis entropy of a signal
	Args: 
	L :  Number of partitions of amplitude
	partition : Time series whose entropy is to be found
	slot_height: Height of each slot/part of the partition
	maxp,minp : Maximum and Minimum values in the signal
	q : q parameter for tsallis entropy

	Returns:
	Float value containing tsallis entropy'''

	ts_ent = 0.00
	for it in range (0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		if(prob_m_l > 0):
			ts_ent = ts_ent - (pow(prob_m_l,q)-prob_m_l);
	ts_ent = ts_ent/(q-1)		
	return ts_ent

def Renyi_entropy(L,partition,slot_height,maxp,minp,alpha):
	'''Returns Shannon entropy of a signal
	Args: 
	L  : Number of partitions of amplitude
	partition : Time series whose entropy is to be found
	slot_height: Height of each slot/part of the partition
	maxp,minp : Maximum and Minimum values in the signal
	alpha: alpha parameter for renyi entropy

	Returns:
	Float value containing renyi entropy'''

	p_ent = 0.00
	for it in range(0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		p_ent = p_ent + pow(prob_m_l,alpha)
	ren_ent = p_ent/(1-alpha)
	return ren_ent	


def permutation_entropy(L,time_series, m, delay):
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
    pe = -sum(p*np.log(p))
    return pe
				