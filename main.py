# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 13:40:36 2022

@author: danie

simple graphing calculator

To do:
    movable legend
    add icon
    add auto resize
    
"""


import math
from math import sin, cos, tan
#from math import sin
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
    #pop up the error to the user
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText("Error")
    msg.setInformativeText(f"Info: {value}")
    msg.exec_()
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
        
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        
        #point to UI file to use
        uic.loadUi("ui_files/graph_layout.ui", self)
        self.setContentsMargins(0,0,0,0) 
        self.setWindowTitle("Josh's Graphing Calculator")
        #Button connections
        self.browseButton.clicked.connect(self.browseFiles)
        self.plotButton.clicked.connect(self.plotFunction)
        self.clearButton.clicked.connect(self.clearPlot)
        self.clearHistoryButton.clicked.connect(self.clearHistory)
        
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
        self.toolbar.setStyleSheet("background-color: rgb(255,255,255);\n"
                                   "color: rgb(70, 140, 0);\n"
                                   "font: 12 12pt \"Segoe UI Semibold\";\n""")
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)
        #fig.canvas.mpl_connect('button_press_event', self.press)
        self.canvas.draw()
        
        self.lines_on_plot = []
        self.points_on_plot = []
        
        self.show()

    def browseFiles(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Default Save Location", "C:/")
        if fname:
            self.save_location = fname + '/'
            plt.rcParams["savefig.directory"] = self.save_location
            self.saveLabel.setText(f"Save Location: {self.save_location}")
        
    def press(self, event):
        if event.button == 2:#middle click event
            ax = self.canvas.axes
            x = round(event.xdata,1)
            y = round(event.ydata,1)
            self.points_on_plot.append([event.xdata, event.ydata])
            ax.plot(event.xdata, event.ydata, marker="o", markersize=5,markerfacecolor="red",  markeredgecolor="red")
            ax.text(event.xdata, event.ydata+.4, '({}, {})'.format(x, y))
            
            self.canvas.draw()
            
    
    
    def plotFunction(self):
        #connect graph
        def cos(x): 
            return np.cos(x)
        def sin(x): 
            return np.sin(x)
        def tan(x): 
            return np.tan(x)
        ax = self.canvas.axes
        #read values from spin boxes
        x_start = self.x_startSpinBox.value()
        x_end = self.x_endSpinBox.value()
        y_start = self.y_startSpinBox.value()
        y_end = self.y_endSpinBox.value()
        x = np.linspace(x_start-50,x_end+50,500)
        
        function = self.functionEdit.text()
        if "^" in function: #this converts ^ to exponent
            function = function.replace('^', '**')
            
        if function not in self.lines_on_plot:
            self.lines_on_plot.append(function)
        
        fig.canvas.mpl_connect('button_press_event', self.press)   
        ax.cla()
        start_chars = ["x", "s", "c", "t"]
        par_check = False
        for item in self.lines_on_plot:
            #below is alot of string comprehesion
                            
            if 'x' in item:
                try:
                    y = eval(item) #turns string into funtion 
                except SyntaxError: #when a * is left out
                    s = ''
                    for i in range(len(item)-1):
                        s += (item[i])
                        if item[i] == '(':
                            par_check = True
                        elif item[i+1] in start_chars :
                            s+='*'
                    s+=item[-1]
                    if par_check: #if they forget to close the par
                        if ')' not in s:
                            s+= ')'
                    try:
                        y = eval(s) 
                    except:
                        self.lines_on_plot.pop()
                        raise
                except NameError:
                    self.lines_on_plot.pop()
                    raise
                ax.plot(x,y) 
            else:
                y = [eval(item)]*500
                ax.plot(x,y) 
                
        for dot in self.points_on_plot: #redraw the dots
            x,y = dot
            ax.plot(x, y, marker="o", markersize=5,markerfacecolor="red",  markeredgecolor="red")
            ax.text(x, y+.4, '({}, {})'.format(round(x,1), round(y, 1)))
            
        #format and draw the graph
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.minorticks_on()
        ax.axvline(x = 0, color = 'k') #puts black lines on Axies
        ax.axhline(y = 0, color = 'k')
        ax.axis(xmin=x_start,xmax=x_end)
        ax.axis(ymin=y_start,ymax=y_end)
        self.canvas.draw()
        
    

        self.canvas.draw()
      
    def clearPlot(self):
        self.lines_on_plot = []
        self.points_on_plot = []
        sip.delete(self.toolbar)
        sip.delete(self.canvas)
        #ax = self.canvas.axes
        self.canvas = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canvas, self.centralwidget)
        self.toolbar.setStyleSheet("background-color: rgb(255,255,255);\n"
                                   "color: rgb(70, 140, 0);\n"
                                   "font: 12 12pt \"Segoe UI Semibold\";\n""")
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)
        self.historyTextEdit.append("cleared")
        #fig.canvas.mpl_connect('button_press_event', self.press)
        
    def clearHistory(self):
        self.historyTextEdit.clear()
        
        


if __name__ == "__main__":
    sys.excepthook = fatalError
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()