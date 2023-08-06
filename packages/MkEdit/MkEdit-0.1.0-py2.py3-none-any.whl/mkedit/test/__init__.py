#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QWidget, QVBoxLayout, QFileDialog, QDialog
from rxbus.core import RxBus
from mkedit.core.DataClass import WorkdirInfo, CreateFileInfo, CreateDirInfo
from rx import operators as ops, scheduler
from PySide2.QtCore import qtTrId
from mkedit.core.EditCenter import EditCenter
from mkedit.core.Dialog import Dialog as MKDialog


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.init()
        self.initSize()
        self.initUI()
        self.initEvent()
        self.updateMenuBar()
        self.initData()

    def init(self):
        self.editCenter = EditCenter(self)

    def initSize(self):
        desktop = QApplication.desktop()
        self.screenWidth = desktop.width() * 0.8
        self.screenHeight = desktop.height() * 1
        print("screen width is %d height is %d" % (self.screenWidth, self.screenHeight))
        self.resize(self.screenWidth, self.screenHeight)

    def initUI(self):
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.editCenter)
        self.setCentralWidget(self.mainWidget)

    def initEvent(self):
        RxBus.instance.register(self, WorkdirInfo).subscribe(
            on_next=lambda value: self.editCenter.getMenusBar.updateWorkDir(value.dirPath))

        RxBus.instance.register(self, CreateFileInfo).pipe(
            ops.subscribe_on(scheduler.ThreadPoolScheduler())
        ).subscribe(on_next=lambda value: self.editCenter.getMenusBar.createFile(value.dirPath))

        RxBus.instance.register(self, CreateDirInfo).pipe(
            ops.subscribe_on(scheduler.ThreadPoolScheduler())
        ).subscribe(on_next=lambda value: self.editCenter.getMenusBar.createDir(value.dirPath))

    def updateMenuBar(self):
        menuBar = QMenuBar()
        winmenu = menuBar.addMenu(qtTrId("File"))
        selectProjectDirAction = QAction(qtTrId("选择工作目录"), self)
        selectProjectDirAction.triggered.connect(self.openFileDir)
        winmenu.addAction(selectProjectDirAction)

        createDirAction = QAction(qtTrId("创建目录"), self)
        createDirAction.triggered.connect(self.createDir)
        winmenu.addAction(createDirAction)

        createFileAction = QAction(qtTrId("创建文件"), self)
        createFileAction.triggered.connect(self.createFile)
        winmenu.addAction(createFileAction)
        self.setMenuBar(menuBar)

    def initData(self):
        self.editCenter.getMenusBar.updateWorkDir("/")

    def openFileDir(self):
        print("openFileDir")
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.Directory)
        ret = fileDialog.exec_()
        if ret == QDialog.Accepted:
            fileName = fileDialog.selectedFiles()
            RxBus.instance.post(WorkdirInfo(fileName[0]))

    def createDir(self):
        print("createDir")
        text = MKDialog().inputDirNameDialog()
        if text:
            print(text)
            RxBus.instance.post(CreateDirInfo(text))

    def createFile(self):
        print("createFile")
        text = MKDialog().inputFileNameDialog()
        if text:
            print(text)
            RxBus.instance.post(CreateFileInfo(text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
