from __future__ import division
import numpy as np
import itertools
from scipy import signal

def butter_filter(input_sig,sample_freq,lowf,highf,order=4):
	'''Computes the filtered value of a given discrete time signal using a butterwort filter.
	Args:
	input_sig: Input Signal
	sample_freq: Sampling frequency of the input signal
	lowf: Lower cut-off of the filter
	highf: Higher cut-off of the filter
	order: order of the filter to be used

	Returns:
	An array with the filtered signal'''
	r = sample_freq/2
	band = [lowf/r,highf/r]
	b,a = signal.butter(order,band,'band')
	output = signal.filtfilt(b,a,input_sig)
	return output
