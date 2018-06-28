#Codes for GUI and other visualizations

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *    
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import style
from scipy import stats
import itertools
from multiprocessing import Process
import time

'''Code for the gui used to visualize the entropies and how parameters change them. Check last lines for more info'''

class EntropyGUI(QWidget):
	
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
		self.sig_orig = []
		self.entropy = "shannon"
		self.w = int(self.w_in_s*250)
		self.delta = int(self.del_in_s*250)
		self.initUI()
		self.processes = []
		self.sig_ent = []
		self.start_point = 0
		self.stop_point = 0
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
		
		btn2 = QPushButton('Parameter_Selection', self)
		btn2.setToolTip('Push to edit relevant parameters')
		btn2.clicked.connect(self.on_click_get_par)
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

		btn5 = QPushButton('Plot current EEG signal', self)
		btn5.setToolTip('Push to plot')
		btn5.clicked.connect(self.on_click_plot_signal)
		btn5.resize(btn5.sizeHint())
		btn5.move(50, 150)       
		
		btn6 = QPushButton('Select sub-part', self)
		btn6.setToolTip('Push to select part of the signal')
		btn6.clicked.connect(self.on_click_sub_part)
		btn6.resize(btn6.sizeHint())
		btn6.move(250, 150) 

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
		i, okPressed = QInputDialog.getInt(self, "Insert Integer",par_name,curr_val, 0, 10000, 1)
		if okPressed:
			return i
		else :
			print ("cancelled")
			return curr_val    
 
	def getDouble(self,par_name,curr_val):
		d, okPressed = QInputDialog.getDouble(self, "Insert Double",par_name, curr_val, 0, 10000, 10)
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

	def on_click_entropy_select(self):
		self.entropy = self.getEntropyChoice()

	def on_click_get_par(self):
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
		print (self.w_in_s , self.del_in_s)
		self.w = int(self.w_in_s*250)
		self.delta = int(self.del_in_s*250)

	def on_click_read(self):    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", ":G/Harsh_Data_Backup/Readable_Data","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			print(fileName)
		self.file_name = fileName    
		self.sig = Read_File(self.file_name)  
		print (len(self.sig))
		self.stop_point = len(self.sig)//250
		self.sig_orig = self.sig

	def on_click_run(self):
		#self.a.close()
		print ("Wait , Calculating")
		self.sig_ent = sig_entropy (self.L,self.w,self.delta,self.sig, self.entropy, self.q,self.alpha,self.d,self.delay)
		print (self.L,self.w,self.delta, self.entropy, self.q,self.alpha,self.d,self.delay)
		print ("done")
		print (len(self.sig_ent))
		p = Process(target = plot, args = (self.sig_ent,))
		self.processes.append(p)
		p.start()
		# plot(self.sig_ent)
		print ("ready")

	def on_click_plot_signal(self):
		k = Process(target = plot, args = (self.sig,))
		self.processes.append(k)
		k.start()	

	def on_click_sub_part(self):
		self.start_point = int(250*self.getDouble("Enter start time in seconds ("+str(len(self.sig_orig)//250)+" )" , self.start_point//250))
		self.stop_point = int(250*self.getDouble("Enter stop time in seconds ("+str(len(self.sig_orig)//250)+" )" , self.stop_point//250))
		self.sig = self.sig_orig[self.start_point:self.stop_point+1]
		print (len(self.sig))


#Run this file to initalize the gui
#Comment the following 3 lines if you want to use this GUI somewhere else
app = QApplication(sys.argv)
ex = EntropyGUI()
sys.exit(app.exec_())		