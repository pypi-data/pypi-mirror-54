#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QHBoxLayout
from PySide2.QtCore import QMargins
from .DataClass import FileInfo
from .MkEdit import MkEdit
from .MenusBar import MemusBar


class EditCenter(QWidget):
    def __init__(self, parent=None):
        print("EditCenter __init__")

        QWidget.__init__(self, parent)
        self._initUI()
        self._initData()
        self._initEvent()

    def __del__(self):
        print("EditCenter __del__")

    def _initEvent(self):
        self.getMenusBar.openFileCallBack = self.openFileCallBack

    def openFileCallBack(self, value):
        self.openFileInfo(value)

    def openFileInfo(self, value: FileInfo):
        has = False
        for index in range(0, self.mdiare.count()):
            tab = self.mdiare.widget(index)
            if tab.property("title") == value.filePath:
                self.mdiare.setCurrentIndex(index)
                has = True
                break
        if not has:
            edit = MkEdit(self)
            edit.loadData(value.filePath)
            edit.setProperty("title", value.filePath)
            self.mdiare.addTab(edit, value.fileName)
            self.mdiare.setTabToolTip(self.mdiare.count() - 1, value.filePath)
            self.mdiare.setCurrentIndex(self.mdiare.count() - 1)

    def tabCloseRequested(self, index):
        _currentTab: MkEdit = self.mdiare.widget(index)
        if not _currentTab.interceptClose():
            self.tabDatas.remove(_currentTab.property("title"))
            self.mdiare.removeTab(index)

    def tabBarClicked(self, index):
        print("tabBarClicked index : %s" % index)

    def tabBarDoubleClicked(self, index):
        print("tabBarDoubleClicked index : %s" % index)

    def currentChanged(self, index):
        print("currentChanged index : %s" % index)

    def destroy(self, destroyWindow: bool = ..., destroySubWindows: bool = ...):
        print("destroy")
        QWidget(EditCenter, self).destroy(destroyWindow, destroySubWindows)

    def create(self, arg__1: int = ..., initializeWindow: bool = ..., destroyOldWindow: bool = ...):
        print("create")
        QWidget(EditCenter, self).create(arg__1, initializeWindow, destroyOldWindow)

    def _initUI(self):
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.menuBar = MemusBar(self)
        self.mainLayout.addWidget(self.menuBar)
        self.rightLayout = QVBoxLayout(self)
        self.rightLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.mdiare = QTabWidget(self)
        self.mdiare.setDocumentMode(True)
        # 注册关闭按钮信号
        self.mdiare.tabCloseRequested.connect(self.tabCloseRequested)
        self.mdiare.tabBarClicked.connect(self.tabBarClicked)
        self.mdiare.tabBarDoubleClicked.connect(self.tabBarDoubleClicked)
        self.mdiare.currentChanged.connect(self.currentChanged)
        self.mdiare.setMovable(True)
        self.mdiare.setTabsClosable(True)
        self.rightLayout.addWidget(self.mdiare)
        self.mainLayout.addLayout(self.rightLayout, 1)
        self.setLayout(self.mainLayout)

    def _initData(self):
        pass
        # edit = Edit(self)
        # self.mdiare.addTab(edit, "xxxx")
        # for i in range(10):

    @property
    def getMenusBar(self):
        return self.menuBar
