# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 13:40:36 2022

@author: danie

simple graphing calculator

To do:
    Pop up the fatal error hook
    movable legend
    add icon
    add clear history button
    mouse click on graph
"""


import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMessageBox, QMainWindow, QApplication, QLabel, QPlainTextEdit, QPushButton, QWidget, QLineEdit, 
                             QComboBox, QDoubleSpinBox, QMenu, QMenuBar, QStatusBar, QTabWidget, QSpinBox, QAction, QDialog, QCompleter)
 
from PyQt5.QtGui import QCursor
from PyQt5 import uic
import sys

import matplotlib
import matplotlib.colors as clrs
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
matplotlib.use('Qt5Agg')

import sip

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
import pandas as pd
import numpy as np


def fatalError(type, value, traceback, oldhook=sys.excepthook):
    oldhook(type, value, traceback)
    print(value)
    return

class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self, parent = None, width = 5, heigh = 5, dpi = 150):
        global fig
        plt.rcParams.update(plt.rcParamsDefault)
        fig = Figure()
        #format the graph
        plt.rcParams.update({"axes.titleweight": "bold", "axes.labelweight": "bold"})
        
        self.axes = fig.add_subplot(111)
        
        
        super(MatplotlibCanvas, self).__init__(fig)
        
        


class UI(QMainWindow):
    
    def __init__(self):
        super(UI, self).__init__()
        
        #self.setWindowIcon(QtGui.QIcon('fileName.png'))
        
        #point to UI file to use
        uic.loadUi("ui_files/graph_layout.ui", self)
        self.setContentsMargins(0,0,0,0) 
        self.setWindowTitle("Josh's Graphing Calculator")
        #Button connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.plotButton.clicked.connect(self.plotFunction)
        self.clearButton.clicked.connect(self.clearPlot)
        
        #configure defualts and rules
        self.x_startSpinBox.setMinimum(-9999999999999)
        self.x_startSpinBox.setMaximum(9999999999999)
        self.x_endSpinBox.setMinimum(-9999999999999)
        self.x_endSpinBox.setMaximum(9999999999999)
        self.x_endSpinBox.setValue(10)
        
        self.y_startSpinBox.setMinimum(-9999999999999)
        self.y_startSpinBox.setMaximum(9999999999999)
        self.y_endSpinBox.setMinimum(-9999999999999)
        self.y_endSpinBox.setMaximum(9999999999999)
        self.y_endSpinBox.setValue(10)
        
        self.historyTextEdit.setReadOnly(True)
        
        
        #Set up the graph
        self.canvas = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canvas, self.centralwidget)
        self.toolbar.setStyleSheet("background-color: rgb(255,255,255);")
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)
        
        self.on_plot = []
        
        self.show()

    def browseFiles(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Default Save Location", "C:/")
        if fname:
            self.save_location = fname + '/'
            plt.rcParams["savefig.directory"] = self.save_location
            self.saveLabel.setText(f"Save Location: {self.save_location}")
        
    def press(self, event):
        if event.button == 3:
            pass
           # print(event.x, event.y)
    
        
    def plotFunction(self):
        #connect and format graph
        ax = self.canvas.axes
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.minorticks_on()
        ax.axvline(x = 0, color = 'k') #puts black lines on Axies
        ax.axhline(y = 0, color = 'k')
        
        #read values from spin boxes
        x_start = self.x_startSpinBox.value()
        x_end = self.x_endSpinBox.value()
        y_start = self.y_startSpinBox.value()
        y_end = self.y_endSpinBox.value()
        x = np.linspace(x_start,x_end,100)
        
        #reads string in y = x line
        fucntion = self.functionEdit.text()
        
        #print(self.on_plot)
        
        if 'x' in fucntion:
            y = eval(fucntion) #turns string into funtion 
            
        else:
            y = [eval(fucntion)]*100
        
        if fucntion in self.on_plot: #prevents plotting same line
            ax.cla()
            for item in self.on_plot:
                if 'x' in item:
                    y = eval(item) #turns string into funtion 
                else:
                    y = [eval(item)]*100
                ax.plot(x,y)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True)
            ax.minorticks_on()
            ax.axvline(x = 0, color = 'k') #puts black lines on Axies
            ax.axhline(y = 0, color = 'k')
            ax.axis(xmin=x_start,xmax=x_end)
            ax.axis(ymin=y_start,ymax=y_end)
            self.canvas.draw()
            return
        else:
            self.on_plot.append(fucntion)
            self.historyTextEdit.append(fucntion) 
        
        ax.plot(x,y)#'g')
        ax.axis(xmin=x_start,xmax=x_end)
        ax.axis(ymin=y_start,ymax=y_end)
        
       # ax.axis.ylim(self.y_startSpinBox.value(), self.y_endSpinBox.value())
        self.canvas.draw()
        
      
    def clearPlot(self):
        self.on_plot = []
        sip.delete(self.toolbar)
        sip.delete(self.canvas)
        ax = self.canvas.axes
        self.canvas = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canvas, self.centralwidget)
        self.toolbar.setStyleSheet("background-color: rgb(255,255,255);")
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)
        self.historyTextEdit.append("cleared")
        

      
      



if __name__ == "__main__":
    sys.excepthook = fatalError
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()