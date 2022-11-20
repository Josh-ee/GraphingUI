# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 13:40:36 2022

@author: danie

simple graph 

"""


import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMessageBox, QMainWindow, QApplication, QLabel, QPlainTextEdit, QPushButton, QWidget, QLineEdit, 
                             QComboBox, QDoubleSpinBox, QMenu, QMenuBar, QStatusBar, QTabWidget, QSpinBox, QAction, QDialog, QCompleter)
 
#from PyQt5.QtWidgets import QComboBox, QDoubleSpinBox, QMenu, QMenuBar, QStatusBar, QTabWidget, QSpinBox, QAction, QDialog, QCompleter 
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
        
        #Below are the button connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.plotButton.clicked.connect(self.plotFunction)
        
        #Below sets up the graph
        '''
        self.canvas = MatplotlibCanvas(self)
        
        self.toolbar = Navi(self.canvas, self.centralwidget)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)
        self.toolbar.setStyleSheet("background-color: rgb(255,255,255);")
        
       # fig.canvas.mpl_connect("plot_event", self.press)
        
        self.canvas.axes.cla()
        self.canvas.draw()
        '''
        self.canvas = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canvas, self.centralwidget)
        self.toolbar.setStyleSheet("background-color: rgb(255,255,255);")
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)

        
        self.show()

    def browseFiles(self):
        print("yes")
        
    def press(self, event):
        if event.button == 3:
            pass
           # print(event.x, event.y)
        
        
    def plotFunction(self):
       # x = np.linspace(-5,5,100)
        x = np.linspace(-5,5,100)
        y = x**3
        fucntion = self.functionEdit.text()
        print(fucntion)
        y = eval(fucntion)
        ax = self.canvas.axes
       # ax.spines['left'].set_position('center')
       # ax.spines['bottom'].set_position('center')
       # ax.spines['right'].set_color('none')
       # ax.spines['top'].set_color('none')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.minorticks_on()
        ax.axvline(x = 0, color = 'k')
        ax.axhline(y = 0, color = 'k')#, linestyle = '-')
#        ax.plot(b,c,'k')
        ax.plot(x,y,'g')
        self.canvas.draw()
      #  print("no")



if __name__ == "__main__":
    sys.excepthook = fatalError
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()