import sys
import os
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication)
from PyQt5.QtGui import QFont    
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSlot

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.title = "GUI for Time Dependent Entropy"
        
    def initUI(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.clicked.connect(self.on_click)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)       
        
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("GUI for Time Dependent Entropy")
        a=self.getInteger()
        self.getText()
        b=self.getDouble()
        if (b<0):
        	os.system("nautilus")
        elif (a>5):
        	os.system("python3")	
        self.getChoice()
 
        self.show()
     
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  

    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 28, 0, 100, 1)
        if okPressed:
            return i
 
    def getDouble(self):
        d, okPressed = QInputDialog.getDouble(self, "Get double","Value:", 10.50, 0, 100, 10)
        if okPressed:
            return d
 
    def getChoice(self):
        items = ("Red","Blue","Green")
        item, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
        if okPressed and item:
            print(item)
 
    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
                    
    @pyqtSlot()
    def on_click(self):
       os.system("nautilus")  

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())