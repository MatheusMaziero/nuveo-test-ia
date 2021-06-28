from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidget,QTableWidget
from PyQt5.QtWidgets import QMessageBox
from GUI.SMSSpamDetection_Interface import Ui_MainWindow
from scr.spamhamclass import SpamDetector
import sys
import os
import cv2
import tensorflow as tf
import numpy as np
import time
import csv
import warnings
warnings.filterwarnings('ignore') 

__appname__ = "SMS SpamDetection Interface Test"




class mainProgram(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setupUi(self)
        self.labellist=[]
        self.labelHist = []
        self.modelinfolist=[]
        self.mImgList = []
        self.mImgListFinal=[]
        self.labels={}
        self.dirname = None
        self.listpath=''
        self.modelpath=''
        self.modelname=None
        self.modelextension=None
        self.modeldirname=None
        self.lastOpenDir = None
        self.resultprob=None
        self.resulttorf=None
        self.cntr = 0
        self.numlabellist=0
        self.nummodellist=0
        self.centerboxeslist=[]
        self.spamham=None
        


    def all_callbacks(self):
          self.Next_String_Btn.clicked.connect(self.nextstring)
          self.Back_String_Btn.clicked.connect(self.prevstring)
          self.FileFonder.clicked.connect(self.openfilelist)
          self.Classifcation_Table.cellDoubleClicked.connect(self.doubleClicked_table)
          self.SelectModel.clicked.connect(self.openfilemodel)
          self.Save_Classication_Btn.clicked.connect(self.savefile)
          self.Clear_Classication_Btn.clicked.connect(self.cleralltable)


             
    def openfilemodel(self):
        self.modelpath=''
        self.modelname=None
        self.modelextension=None
        self.modeldirname=None
        self.modelpath = QFileDialog.getOpenFileName(filter="Model files (*.pkl)")[0]
        if self.modelpath =='':
            return
        elif self.modelpath !='':
            self.modeldir, self.modelname = os.path.split(self.modelpath)
            self.modeldirname=os.path.dirname(self.modelpath)
            self.ModelDirLabel.setText(self.modelname)

        
        
            
    def openfilelist(self):
        self.Classifcation_Table.clearContents()
        self.listpath=None
        self.cntr=0
        self.listlist=[]
        self.csvreader=None
        self.numlistlist=0
        self.resultprob=None
        self.resulttorf=None
        self.resultspamhamensagem=None
        self.spamham=None
        self.spamham=SpamDetector()
        self.listpath = QFileDialog.getOpenFileName(filter="Text files (*.csv)")[0]
        if self.listpath =='':
                return
        elif self.listpath != '':
            if self.modelpath =='':
                QMessageBox.about(self,'Warning','Select Model Firt')
            elif self.modelpath !='':
                self.listdir, self.listname = os.path.split(self.listpath)
                self.FileDirLabel.setText(self.listname)
                with open(self.listpath, 'r') as f:
                    self.csvreader= csv.reader(f, delimiter=';')
                    for row in self.csvreader:
                        self.listlist.append(row[0]+row[1]+row[2]+row[3]+row[4])
                self.numlistlist=len(self.listlist)
                self.Classifcation_Table.setRowCount(self.numlistlist)
                for i in range(0,self.numlistlist):
                    self.Classifcation_Table.setItem(i,0,QtWidgets.QTableWidgetItem(self.listlist[i]))
                self.Classifcation_Table.setCurrentCell(self.cntr,0)
                self.resultprob=self.spamham.prob_spam(self.listlist[self.cntr],self.modelpath)
                self.resulttorf,self.resultspamhamensagem=self.spamham.is_spam(self.listlist[self.cntr],self.modelpath)
                self.Classifcation_Table.setItem(self.cntr,1,QtWidgets.QTableWidgetItem(str(self.resultprob)))
                self.Classifcation_Table.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.resulttorf)))
                self.Classifcation_Table.setItem(self.cntr,3,QtWidgets.QTableWidgetItem(str(self.resultspamhamensagem)))
                
                
            

            



    def nextstring(self):
        if self.listlist==[]:
            return
        elif self.listlist !=[]:
            if self.cntr < self.numlistlist -1:
                self.cntr += 1
                self.Classifcation_Table.setCurrentCell(self.cntr,0)
                self.resultprob=self.spamham.prob_spam(self.listlist[self.cntr],self.modelpath)
                self.resulttorf,self.resultspamhamensagem=self.spamham.is_spam(self.listlist[self.cntr],self.modelpath)
                self.Classifcation_Table.setItem(self.cntr,1,QtWidgets.QTableWidgetItem(str(self.resultprob)))
                self.Classifcation_Table.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.resulttorf)))
                self.Classifcation_Table.setItem(self.cntr,3,QtWidgets.QTableWidgetItem(str(self.resultspamhamensagem)))
                
            
            
    def prevstring(self):
        if self.listlist==[]:
            return
        elif self.listlist !=[]:
            if self.cntr > 0:
                self.cntr -= 1
                self.Classifcation_Table.setCurrentCell(self.cntr,0)
                self.resultprob=self.spamham.prob_spam(self.listlist[self.cntr],self.modelpath)
                self.resulttorf,self.resultspamhamensagem=self.spamham.is_spam(self.listlist[self.cntr],self.modelpath)
                self.Classifcation_Table.setItem(self.cntr,1,QtWidgets.QTableWidgetItem(str(self.resultprob)))
                self.Classifcation_Table.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.resulttorf)))
                self.Classifcation_Table.setItem(self.cntr,3,QtWidgets.QTableWidgetItem(str(self.resultspamhamensagem)))
            
    def doubleClicked_table(self,row, column):
        self.cntr = row
        self.Classifcation_Table.setCurrentCell(self.cntr,0)
        self.resultprob=self.spamham.prob_spam(self.listlist[self.cntr],self.modelpath)
        self.resulttorf,self.resultspamhamensagem=self.spamham.is_spam(self.listlist[self.cntr],self.modelpath)
        self.Classifcation_Table.setItem(self.cntr,1,QtWidgets.QTableWidgetItem(str(self.resultprob)))
        self.Classifcation_Table.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.resulttorf)))
        self.Classifcation_Table.setItem(self.cntr,3,QtWidgets.QTableWidgetItem(str(self.resultspamhamensagem)))
        self.Classifcation_Table.setCurrentCell(self.cntr,0)
        

        
    def savefile(self):
        path = QFileDialog.getSaveFileName(
                self, 'Save File', '', 'CSV(*.csv)')
        rowdata=list()
        if path == ('', ''):
            return
        elif path != ('', ''):
            with open(str(path[0]), 'w') as stream:
                writer = csv.writer(stream)
                r=self.Classifcation_Table.rowCount()
                if r == 0:
                    return
                elif r != 0:
                    for row in range(0,r):
                        item1=None
                        item2=None
                        item3=None
                        item4=None
                        item1 = self.Classifcation_Table.item(row, 0)
                        item2 = self.Classifcation_Table.item(row, 1)
                        item3 = self.Classifcation_Table.item(row, 2)
                        item4 = self.Classifcation_Table.item(row, 3)
                        if item2 !=None:
                            rowdata.append([str(item1.text()),str(item2.text()),str(item3.text()),str(item4.text())])
                        elif item2==None:
                            rowdata.append([str(item1.text()),"","",""])
                writer.writerows(rowdata)
                return
            
    def cleralltable(self):
        self.Classifcation_Table.clearContents()
        if self.listlist==[]:
            return
        elif self.listlist!=[]:
            self.numlistlist=len(self.listlist)
            self.Classifcation_Table.setRowCount(self.numlistlist)
            for i in range(0,self.numlistlist):
                self.Classifcation_Table.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.listlist[i])))
            self.cntr=0
            self.Classifcation_Table.setCurrentCell(self.cntr,0)
            self.resultprob=self.spamham.prob_spam(self.listlist[self.cntr],self.modelpath)
            self.resulttorf,self.resultspamhamensagem=self.spamham.is_spam(self.listlist[self.cntr],self.modelpath)
            self.Classifcation_Table.setItem(self.cntr,1,QtWidgets.QTableWidgetItem(str(self.resultprob)))
            self.Classifcation_Table.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.resulttorf)))
            self.Classifcation_Table.setItem(self.cntr,3,QtWidgets.QTableWidgetItem(str(self.resultspamhamensagem)))
                

                



    
        
if __name__=='__main__':
    app=QApplication([])
    app.setApplicationName(__appname__) 
    inferencegui = mainProgram()
    inferencegui.all_callbacks()
    inferencegui.show()
    app.exec_()
    
