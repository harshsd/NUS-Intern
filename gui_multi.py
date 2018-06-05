import sys
import os
from PyQt5.QtWidgets import (QWidget, QToolTip, 
	QPushButton, QApplication)
from PyQt5.QtGui import QFont    
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtCore import pyqtSlot, QThread
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import style
from scipy import stats
import itertools
from multiprocessing import Process

class Example(QWidget):
	
	def __init__(self):
		self.num = 0
		super().__init__()
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.title = "GUI for Time Dependent Entropy"
		self.w_in_s = 0.5
		self.del_in_s = 0.5
		self.L = 10
		self.q = 2
		self.alpha = 0.5
		self.d = 3
		self.delay = 2
		self.file_name = "Shit"
		self.sig = []
		self.entropy = "shannon"
		self.w = int(self.w_in_s*250)
		self.delta = int(self.del_in_s*250)
		self.initUI()
		self.processes = []
		#self.a = self.plot()
		#self.pool = multiprocessing.Pool()
		
		
	def initUI(self):
		
		QToolTip.setFont(QFont('SansSerif', 10))
		
		self.setToolTip('This is a <b>QWidget</b> widget')
		self.setWindowTitle("GUI for Time Dependent Entropy")
		btn1 = QPushButton('Select Entropy', self)
		btn1.setToolTip('Select Entropy to plot')
		btn1.clicked.connect(self.on_click_entropy_select)
		btn1.resize(btn1.sizeHint())
		btn1.move(50, 50)
		
		btn2 = QPushButton('Parameter_Selction', self)
		btn2.setToolTip('Push to edit relevant parameters')
		btn2.clicked.connect(self.on_click)
		btn2.resize(btn2.sizeHint())
		btn2.move(250, 50)

		btn3 = QPushButton('Select and Read_File', self)
		btn3.setToolTip('Push to read the file')
		btn3.clicked.connect(self.on_click_read)
		btn3.resize(btn3.sizeHint())
		btn3.move(50, 100)

		btn4 = QPushButton('Calculate and plot', self)
		btn4.setToolTip('Push to plot')
		btn4.clicked.connect(self.on_click_run)
		btn4.resize(btn4.sizeHint())
		btn4.move(250, 100)  

		# btn5 = QPushButton('Clean Plots', self)
		# btn5.setToolTip('Push to clean')
		# btn5.clicked.connect(self.on_click_clear)
		# btn5.resize(btn5.sizeHint())
		# btn5.move(450, 100)       
		
		# self.setGeometry(self.left, self.top, self.width, self.height)
		# a=self.getInteger()
		# #self.getText()
		# b=self.getDouble()
		# if (b<0):
		#   os.system("nautilus")
		# elif (a>5):
		#   os.system("python3")    
		# #self.getChoice()
		#print (self.w_in_s)
		self.show()
	 
	def closeEvent(self, event):
		
		reply = QMessageBox.question(self, 'Message',
			"Are you sure to quit?", QMessageBox.Yes | 
			QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()  

	def getInteger(self,par_name,curr_val):
		#print(self.w_in_s)
		i, okPressed = QInputDialog.getInt(self, "Insert Integer",par_name,curr_val, 0, 100, 1)
		if okPressed:
			return i
		else :
			return curr_val    
 
	def getDouble(self,par_name,curr_val):
		d, okPressed = QInputDialog.getDouble(self, "Insert Double",par_name, curr_val, 0, 100, 10)
		if okPressed:
			return d
		else :
			return curr_val    
 
	def getEntropyChoice(self):
		items = ("shannon","tsallis","renyi","permutation")
		item, okPressed = QInputDialog.getItem(self, "Entropy Selection","Entropy", items, 0, False)
		if okPressed and item:
			return item
		else :
			return "shannon"    
 
	def getText(self):
		text, okPressed = QInputDialog.getText(self, "Give file_name","File Name:", QLineEdit.Normal, "s5t1c1.txt")
		if okPressed and text != '':
			return text
					
	@pyqtSlot()

	# def on_click_clear(self):
	#   self.to_be_plotted=[]

	def on_click_entropy_select(self):
		self.entropy = self.getEntropyChoice()

	def on_click(self):
	   self.w_in_s = self.getDouble("Window_Size",self.w_in_s)
	   self.del_in_s = self.getDouble("Delta_in_S",self.del_in_s)
	   self.L = self.getInteger("Number of partitions",self.L)
	   if (self.entropy == "tsallis"):
		   self.q = self.getDouble("q for Tsallis",self.q)
	   elif (self.entropy == "renyi"):
		   self.alpha = self.getDouble("alpha for renyi",self.alpha)
	   elif (self.entropy == "permutation"):
		   self.d = self.getInteger("d for permutation",self.d)
		   self.delay = self.getInteger("delay for permutation",self.delay)        
		 

	def on_click_read(self):    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "/media/harsh/DATA/Readable_Data","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			print(fileName)
		self.file_name = fileName    
		self.sig = Read_File(self.file_name)  
		print (len(self.sig))

	def on_click_run(self):
		#self.a.close()
		print ("Wait , Calculating")
		sig_ent = sig_entropy (self.L,self.w,self.delta,self.sig, self.entropy, self.q,self.alpha,self.d,self.delay)
		print ("done")
		p = Process(target = plot, args = (sig_ent,))
		self.processes.append(p)
		p.start()
		print ("ready")

def plot(sig_ent):
	plt.figure()
	plt.plot(sig_ent)
	plt.show()
		
		
class PlotterThread(QThread):
	def __init__(self,sig):
		super(PlotterThread,self).__init__()
		self.sig = sig
		#plt.show()

	def run(self):
		plt.figure()
		plt.plot (self.sig)
		print ("done")
		plt.show()

	def __del__(self):
		print ("exiting")   





def Read_File (file_name):
	#os.chdir("/media/harsh/DATA/Readable_Data/Unfiltered_Data")
	f = open (file_name , 'r')
	sig = []
	for line in f:
		for word in line.split():   
				#print(word)
				sig.append(float(word))
	return sig          

def sig_entropy ( L , w, delta, sig, entropy_name,q,alpha,d,delay):
	#entropy_name = shannon/tsallis/renyi/permutation

	entropy = []
	K = len(sig)
	M = (K-w)//delta  # Should be an int
	M = int(M)
	#print (M)
	#print (maxp,minp)
	for m in range (0,M):
		partition = sig[m*delta:(w+(m*delta))+1]
		entropy.append(partition_entropy(partition,L,q,entropy_name,alpha,d,delay))
		#print(m/M)
		# print(entropy_name)
	return entropy

def partition_entropy( partition,L,q,entropy_name,alpha,d,delay):
	
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
		#print (sh_ent,ts_ent)
		#return (sh_ent,ts_ent,ren_ent)
		#amplitude intervals defined as [minp+ (k) (slot_height) , minp + (k+1) (slot_height)] k belongs to 0 to L-1
		#Number of s(k) in partition is w

def P_m_l(partition,k,slot_height,maxp,minp): #k from 0 to L-1

		count = 0
		w = len(partition)
		#print(w)
		for i in range (0,w-1):
			if ((partition[i] >= minp + k*(slot_height)) & (partition[i] <= minp + (k+1)*(slot_height))):
					count = count + 1
		#print count
		#print (count/w)            
		return (count/w)

def Shannon_entropy(L,partition,slot_height,maxp,minp):
	sh_ent = 0.00
	for it in range (0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		if(prob_m_l > 0):
			sh_ent = sh_ent - (prob_m_l*math.log(prob_m_l));
	#print sh_ent       
	return sh_ent
	
def Tsallis_entropy(L,partition,slot_height,maxp,minp,q):
	ts_ent = 0.00
	for it in range (0,L-1):
		prob_m_l = P_m_l(partition,it,slot_height,maxp,minp)
		if(prob_m_l > 0):
			ts_ent = ts_ent - (pow(prob_m_l,q)-prob_m_l);
	ts_ent = ts_ent/(q-1)       
	return ts_ent

def Renyi_entropy(L,partition,slot_height,maxp,minp,alpha):
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
		
if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())