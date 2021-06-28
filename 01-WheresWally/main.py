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
from GUI.WheresWally import Ui_MainWindow
from scr.yolo_image import YoloTest
import sys
import os
import cv2
import tensorflow as tf
import numpy as np
import time
import csv

__appname__ = "Wheres Wally Detection Inference "

VALID_FORMAT = ('.BMP', '.GIF', '.JPG', '.JPEG', '.PNG', '.PBM', '.PGM', '.PPM', '.TIFF', '.XBM')  # Image formats supported by Qt

def getImages(folder):
    ''' Get the names and paths of all the images in a directory. '''
    image_list = []
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if file.upper().endswith(VALID_FORMAT):
                im_path = os.path.join(folder, file)
                image_list.append(im_path)
    return image_list


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
        self.labelpath=None
        self.modelpath=None
        self.modelname=None
        self.modelextension=None
        self.modeldirname=None
        self.yolomodelweight =None
        self.lastOpenDir = None
        self.op=None
        self.cntr = 0
        self.numlabellist=0
        self.nummodellist=0
        self.centerboxeslist=[]
        


    def all_callbacks(self):
          self.SelectFolder.clicked.connect(self.openDirDialog)
          self.Next_Image.clicked.connect(self.nextImg)
          self.PrevImage.clicked.connect(self.prevImg)
          self.ImageList.itemDoubleClicked.connect(self.list_click)
          self.LabelFonder.clicked.connect(self.openfilelabel)
          self.AllImageTable.cellDoubleClicked.connect(self.doubleClicked_table)
          self.SelectModel.clicked.connect(self.openfilemodel)
          self.Saved_Btn.clicked.connect(self.savefile)
          self.Clear_Btn.clicked.connect(self.cleralltable)


    def modeselection(self):
        if self.ClassiificationMode.isChecked():
            self.op='Classfication'
        elif self.ObjDetectionMode.isChecked():
            self.op='Object Detection'
        self.ModeLab.setText(self.op)
             
    def openfilemodel(self):
        self.ModelInfoList.clearContents()
        self.modelpath=None
        self.modelname=None
        self.modelextension=None
        self.modeldirname=None
        self.yolomodelweight =None
        self.modelinfolist=[]
        self.nummodellist=0
        self.modelpath = QFileDialog.getOpenFileName(filter="Model files (*.pb *.tflite *.cfg)")[0]
        self.modelname, self.modelextension = os.path.splitext(self.modelpath)
        self.modeldirname=os.path.dirname(self.modelpath)
        QMessageBox.about(self,'Mode yolo','Select Weights file to Yolo mode')
        self.yolomodelweight = QFileDialog.getOpenFileName(filter="Yolo files (*.weights)")[0]
        self.modelinfolist.append(self.modelname)
        self.modelinfolist.append(self.yolomodelweight)
        self.nummodellist=len(self.modelinfolist)
        self.ModelInfoList.setRowCount(self.nummodellist)
        for i in range(0,self.nummodellist):
            self.ModelInfoList.setItem(i,0 ,QtWidgets.QTableWidgetItem(str(self.modelinfolist[i])))
            
    def openfilelabel(self):
        self.labellisttable.clearContents()
        self.labelpath=None
        self.COLORS=None
        self.labellist=[]
        self.numlabellist=0
        self.labelpath = QFileDialog.getOpenFileName(filter="Text files (*.txt)")[0]
        if self.labelpath =='':
            return
        elif self.labelpath != '':
            with open(self.labelpath, 'r') as f:
                self.labellist = [line.strip() for line in f.readlines()]
            self.numlabellist=len(self.labellist)
            self.COLORS = np.random.randint(0, 255, size=(self.numlabellist, 3), dtype="uint8")
            self.labellisttable.setRowCount(self.numlabellist)
            for i in range(0,self.numlabellist):
                self.labellisttable.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.labellist[i])))


   

    def openDirDialog(self):
        self.rowcont=0
        self.cntr=0
        self.numImages=0
        self.ImageList.clear()
        self.LabelImage.clear()
        self.AllImageTable.clearContents()
        self.folder=None
        self.imagetable=None
        self.tmp = None
        self.mImgList=[]
        self.mImgListFinal=[]
        self.results=[]
        self.centerboxeslist=[]
        self.numresult=0
        self.image=None
        dialog = QFileDialog()
        self.folder = dialog.getExistingDirectory(None, "Select Folder")
        if self.folder=='':
            QMessageBox.about(self,'Atention','Select dir')
            return
        elif self.folder!='':
            self.mImgList = getImages(self.folder)
            for itemPath in self.mImgList:
                self.mImgListFinal.append(itemPath.replace('\\','/'))
            self.numImages=len(self.mImgListFinal)
            for itemPath in self.mImgListFinal:
                self.ImageList.addItem(itemPath)
            self.AllImageTable.setRowCount(self.numImages)
            for i in range(0,self.numImages):
                self.AllImageTable.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.mImgListFinal[i])))
            yolo=YoloTest()
            self.results,self.image,self.centerboxeslist=yolo.YoloImage(self.modelpath,self.yolomodelweight,self.mImgListFinal[self.cntr],self.labellist,self.COLORS)
            self.numresult=len(self.results)
            self.ResultTableList.setRowCount(self.numresult)
            for i in range(0,self.numresult):
                self.ResultTableList.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.results[i]['id'])))
                self.ResultTableList.setItem(i,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist[i])))
                self.ResultTableList.setItem(i,2,QtWidgets.QTableWidgetItem(str(self.results[i]['score'])))
            self.AllImageTable.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.results)))
            self.AllImageTable.setItem(self.cntr,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist)))
            self.ImageList.setCurrentRow(self.cntr)
            self.AllImageTable.setCurrentCell(self.cntr,0)
            self.loadImage(self.image)
            #self.imagetable=self.loadtableimage(self.image)
            #self.AllImageTable.setCellWidget(self.cntr,0,self.imagetable)
        
    


    def nextImg(self):
        self.ResultTableList.clearContents()
        if self.mImgListFinal ==[]:
            return
        elif self.mImgListFinal !=[]:
            if self.cntr < self.numImages -1:
                self.cntr += 1
                yolo=YoloTest()
                self.results,self.image,self.centerboxeslist=yolo.YoloImage(self.modelpath,self.yolomodelweight,self.mImgListFinal[self.cntr],self.labellist,self.COLORS)
                self.numresult=len(self.results)
                self.ResultTableList.setRowCount(self.numresult)
                for i in range(0,self.numresult):
                    self.ResultTableList.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.results[i]['id'])))
                    self.ResultTableList.setItem(i,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist[i])))
                    self.ResultTableList.setItem(i,2,QtWidgets.QTableWidgetItem(str(self.results[i]['score'])))
                self.AllImageTable.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.results)))
                self.AllImageTable.setItem(self.cntr,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist)))
                self.loadImage(self.image)
                self.AllImageTable.setCurrentCell(self.cntr,0)
                self.ImageList.setCurrentRow(self.cntr)
            
            
    def prevImg(self):
        self.ResultTableList.clearContents()
        if self.mImgListFinal ==[]:
            return
        elif self.mImgListFinal !=[]:
            if self.cntr > 0:
                self.cntr -= 1
                yolo=YoloTest()
                self.results,self.image,self.centerboxeslist=yolo.YoloImage(self.modelpath,self.yolomodelweight,self.mImgListFinal[self.cntr],self.labellist,self.COLORS)
                self.numresult=len(self.results)
                self.ResultTableList.setRowCount(self.numresult)
                for i in range(0,self.numresult):
                    self.ResultTableList.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.results[i]['id'])))
                    self.ResultTableList.setItem(i,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist[i])))
                    self.ResultTableList.setItem(i,2,QtWidgets.QTableWidgetItem(str(self.results[i]['score'])))
                self.AllImageTable.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.results)))
                self.AllImageTable.setItem(self.cntr,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist)))
                self.loadImage(self.image)
                self.AllImageTable.setCurrentCell(self.cntr,0)
                self.ImageList.setCurrentRow(self.cntr)
            
    def list_click(self, item=None):
        self.ResultTableList.clearContents()
        self.cntr = self.mImgListFinal.index(str(item.text()))
        yolo=YoloTest()
        self.results,self.image,self.centerboxeslist=yolo.YoloImage(self.modelpath,self.yolomodelweight,self.mImgListFinal[self.cntr],self.labellist,self.COLORS)
        self.numresult=len(self.results)
        self.ResultTableList.setRowCount(self.numresult)
        for i in range(0,self.numresult):
            self.ResultTableList.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.results[i]['id'])))
            self.ResultTableList.setItem(i,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist[i])))
            self.ResultTableList.setItem(i,2,QtWidgets.QTableWidgetItem(str(self.results[i]['score'])))
        self.AllImageTable.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.results)))
        self.AllImageTable.setItem(self.cntr,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist)))
        self.loadImage(self.image)
        self.AllImageTable.setCurrentCell(self.cntr,0)
        self.ImageList.setCurrentRow(self.cntr)

    def doubleClicked_table(self,row, column):
        self.ResultTableList.clearContents()
        self.cntr = row
        yolo=YoloTest()
        self.results,self.image,self.centerboxeslist=yolo.YoloImage(self.modelpath,self.yolomodelweight,self.mImgListFinal[self.cntr],self.labellist,self.COLORS)
        self.numresult=len(self.results)
        self.ResultTableList.setRowCount(self.numresult)
        for i in range(0,self.numresult):
            self.ResultTableList.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.results[i]['id'])))
            self.ResultTableList.setItem(i,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist[i])))
            self.ResultTableList.setItem(i,2,QtWidgets.QTableWidgetItem(str(self.results[i]['score'])))
        self.AllImageTable.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.results)))
        self.loadImage(self.image)
        self.AllImageTable.setCurrentCell(self.cntr,0)
        self.ImageList.setCurrentRow(self.cntr)
        
    def loadImage(self,loadPath):
        self.imagepathq = loadPath
        frame = cv2.cvtColor(self.imagepathq , cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.LabelImage.setPixmap(QtGui.QPixmap.fromImage(image))
        self.LabelImage.setScaledContents(True)
        self.LabelImage.show()
        
    def savefile(self):
        path = QFileDialog.getSaveFileName(
                self, 'Save File', '', 'CSV(*.csv)')
        rowdata=list()
        if path == ('', ''):
            return
        elif path != ('', ''):
            with open(str(path[0]), 'w') as stream:
                writer = csv.writer(stream)
                r=self.AllImageTable.rowCount()
                if r == 0:
                    return
                elif r != 0:
                    for row in range(0,r):
                        item1=None
                        item2=None
                        item3=None
                        item1 = self.AllImageTable.item(row, 0)
                        item2 = self.AllImageTable.item(row, 1)
                        item3 = self.AllImageTable.item(row, 2)
                        if item2 !=None:
                            rowdata.append([str(item1.text()),str(item2.text()),str(item3.text())])
                        elif item2==None:
                            rowdata.append([str(item1.text()),"",""])
                writer.writerows(rowdata)
                return
            
    def cleralltable(self):
        self.AllImageTable.clearContents()
        if self.mImgListFinal==[]:
            return
        elif self.mImgListFinal!=[]:
            self.numImages=len(self.mImgListFinal)
            self.AllImageTable.setRowCount(self.numImages)
            for i in range(0,self.numImages):
                self.AllImageTable.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.mImgListFinal[i])))
            yolo=YoloTest()
            self.cntr=0
            self.results,self.image,self.centerboxeslist=yolo.YoloImage(self.modelpath,self.yolomodelweight,self.mImgListFinal[self.cntr],self.labellist,self.COLORS)
            self.numresult=len(self.results)
            self.ResultTableList.setRowCount(self.numresult)
            for i in range(0,self.numresult):
                self.ResultTableList.setItem(i,0,QtWidgets.QTableWidgetItem(str(self.results[i]['id'])))
                self.ResultTableList.setItem(i,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist[i])))
                self.ResultTableList.setItem(i,2,QtWidgets.QTableWidgetItem(str(self.results[i]['score'])))
            self.AllImageTable.setItem(self.cntr,2,QtWidgets.QTableWidgetItem(str(self.results)))
            self.AllImageTable.setItem(self.cntr,1,QtWidgets.QTableWidgetItem(str(self.centerboxeslist)))
            self.loadImage(self.image)
            self.AllImageTable.setCurrentCell(self.cntr,0)
            self.ImageList.setCurrentRow(self.cntr)
            
                



    
        
if __name__=='__main__':
    app=QApplication([])
    app.setApplicationName(__appname__) 
    inferencegui = mainProgram()
    inferencegui.all_callbacks()
    inferencegui.show()
    app.exec_()
    
