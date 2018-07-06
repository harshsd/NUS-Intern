#feature extraction codes
import numpy as np

def freq(i,f_start,f_step):
	return f_start + i*f_step

def dominant_frequency(psd,f_start,f_step):
	psd = np.array(psd)
	f_max = 0
	p_f_max = 0
	for i in range (0,len(psd)):
		if (psd[i]>p_f_max):
			p_f_max=psd[i]
			f_max = i
	f_max = f_max*f_step + f_start
	return f_max

def apdp(psd,width=3):
	p_f_max = 0
	i_max = 0
	for i in range (0,len(psd)):
		if (psd[i]>p_f_max):
			p_f_max=psd[i]
			i_max = i
	power = 0		
	for k in range (int(i_max-((width-1)/2)),int(i_max+1+(width-1)/2)):
		#print (len(psd))
		if (k>=0):
			if(k<len(psd)):
				power = power + psd[k]	
	return power	

def cgf(psd,f_start,f_step):
	psum = 0
	fpsum = 0
	for i in range (0,len(psd)):
		psum = psum + psd[i]
		fpsum = fpsum + (psd[i]*i)
	f = fpsum/psum
	f = f*f_step + f_start
	return f

def fv(psd,f_start,f_step):
	psum = 0
	pffsum = 0
	pf2sum = 0
	for i in range (0,len(psd)):
		f = freq(i,f_start,f_step)
		p = psd[i]
		pffsum = pffsum + (p*f*f)
		pf2sum = pf2sum + (p*f)
		psum = psum + p
	pf2sum = pf2sum*pf2sum
	fv = (pffsum/psum) - (pf2sum/(psum*psum))
	return fv	


