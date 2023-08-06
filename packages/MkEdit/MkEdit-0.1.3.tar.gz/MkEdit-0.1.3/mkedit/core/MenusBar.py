#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QWidget, QFileSystemModel, QTreeView, QAction, QMenu, QVBoxLayout, QAbstractItemView
from PySide2 import QtCore
from PySide2.QtCore import QMargins, QFileInfo
from PySide2.QtGui import QMouseEvent
from .FileUtils import createFile, createDir, deleteDir, deleteFile
from .DataClass import FileInfo
import uuid
from rxbus.core import RxBus
from .Dialog import Dialog as MKDialog
import json
import os
from .FileUtils import createFile


class MemusBar(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.lastSettingFile = "lastSettingFile"
        self.init()
        self._initUI()
        self.defaultForCreateMD = ["metaData-id:%s" % uuid.uuid1(), "metaData-title:"]
        self.initEvent()

    def __del__(self):
        RxBus.instance.unRegister(self)

    def init(self):
        self.workDir = ""

    def createDir(self, value):
        createDir(self.workDir, value)

    def createFile(self, value, default: str = ""):
        createFile(self.workDir, value, self.defaultForCreateMD)

    def initEvent(self):
        pass

    def getSettingFile(self):
        if not os.path.exists("lastSettingFile.json"):
            with open('lastSettingFile.json', mode='w')  as jsonFile:
                pass
        with open('lastSettingFile.json', mode='r') as jsonFile:
            try:
                data = json.load(jsonFile)
                return data
            except Exception as e:
                print(e)
                return {}

    def saveSettingFile(self, setting):
        with open('lastSettingFile.json', mode='w') as jsonFile:
            json.dump(setting, jsonFile)

    def getLastWorkDirRecord(self):
        setting: dict = self.getSettingFile()
        value = setting.get("lastWorkDirRecord")
        if value:
            return value
        else:
            return "/"

    def saveWorkDirRecord(self, value):
        setting = self.getSettingFile()
        setting["lastWorkDirRecord"] = value
        self.saveSettingFile(setting)

    def updateWorkDir(self, value: str = ""):
        if not value or value == "":
            # 去最后一次的目录信息
            self.workDir = self.getLastWorkDirRecord()
        else:
            self.workDir = value
            self.saveWorkDirRecord(value)
        self.treeModel.setRootPath(self.workDir)
        self.treeView.setRootIndex(self.treeModel.index(self.workDir))
        self.treeModel.setNameFilters(['*.md'])

    def _initUI(self):
        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))

        self.treeModel = QFileSystemModel(self)
        self.treeModel.setReadOnly(False)
        self.treeView = QTreeView(self)
        self.treeView.setDragDropMode(QAbstractItemView.InternalMove)
        self.treeView.setDragEnabled(True)
        self.treeView.setAcceptDrops(True)
        self.treeView.setDropIndicatorShown(True)
        self.setMinimumHeight(100)
        self.treeView.setModel(self.treeModel)
        self.treeView.setSortingEnabled(True)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.showContextMenu)
        self.treeView.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)
        self.mainLayout.addWidget(self.treeView, 1)
        self.setLayout(self.mainLayout)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            # 是否按下左键
            index = self.treeView.indexAt(event.pos())
            if index.isValid():
                fileInfo = self.treeModel.fileInfo(index)
                if fileInfo.isFile():
                    fileInfo = FileInfo(fileInfo.fileName(), fileInfo.filePath())
                    self.openFileCallBack(fileInfo)
        else:
            event.accept()

    def showContextMenu(self, pos):
        index = self.treeView.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            action = QAction(menu)
            action.setObjectName("create_dir")
            action.setProperty("pos", pos)
            action.setText("创建目录")
            action.triggered.connect(self.actionHandler)
            menu.addAction(action)

            action = QAction(menu)
            action.setObjectName("delete_dir")
            action.setProperty("pos", pos)
            action.setText("删除目录")
            action.triggered.connect(self.actionHandler)
            menu.addAction(action)

            action = QAction(menu)
            action.setObjectName("create_file")
            action.setProperty("pos", pos)
            action.setText("创建文件")
            action.triggered.connect(self.actionHandler)
            menu.addAction(action)

            action = QAction(menu)
            action.setObjectName("delete_file")
            action.setProperty("pos", pos)
            action.setText("删除文件")
            menu.addAction(action)
            action.triggered.connect(self.actionHandler)
            menu.exec_(self.treeView.mapToGlobal(pos))

    def actionHandler(self):
        print("actionHandler")
        type = self.sender().objectName()
        pos = self.sender().property("pos")
        print("pos:%s" % pos)
        fileInfo = self.treeModel.fileInfo(self.treeView.currentIndex())
        print("fileInfo %s" % fileInfo)
        print(fileInfo.fileName())
        print(fileInfo.filePath())
        print(fileInfo.path())
        print(fileInfo.isRoot())
        path = ""
        file = fileInfo.filePath()
        print("filePath: %s" % fileInfo.filePath())
        print("path: %s" % fileInfo.path())
        print("fileName: %s" % fileInfo.fileName())

        path = fileInfo.path()

        # if path == AppConfig.articleRootPath:
        #     return
        if type == "create_dir":
            print("创建目录")
            text = MKDialog().inputDirNameDialog()
            if text:
                print(text)
                createDir(self.getDir(fileInfo), text)
            if fileInfo.isDir():
                print("是目录")
        elif type == "delete_dir":
            print("删除目录")
            deleteDir(fileInfo.filePath())
        elif type == "create_file":
            print("创建文件")
            text = MKDialog().inputFileNameDialog()
            if text:
                print(text)
                createFile(self.getDir(fileInfo), text)
        elif type == "delete_file":
            print("删除文件")
            deleteFile(file)

    def setDefaultValue(self, value: str = ""):
        self.defaultForCreateFile = value

    @property
    def getDefaultValue(self):
        return self.defaultForCreateMD

    def getDir(self, fileInfo: QFileInfo):
        if fileInfo.isFile():
            return fileInfo.path()
        else:
            return fileInfo.filePath()

    def openFileCallBack(self, value):
        pass
