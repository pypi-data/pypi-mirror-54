#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPlainTextEdit, QSizePolicy, QMessageBox, QShortcut
from mistune import Markdown, Renderer
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtGui import QFont, QFontMetrics, QKeySequence, QKeyEvent
from PySide2.QtCore import QMargins
from os import path
from rx import operators as ops, scheduler
from .FileUtils import updateFile


class RightWebView(QWebEngineView):
    def __init__(self, parent=None):
        super(RightWebView, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__html = ''

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, html):
        self.__html = html
        self.setHtml(html)

    def notifyScroll(self, dx, dy):
        print("notifyScroll dx:%s dy:%s" % (dx, dy))
        self.scroll(dx, dy)


class LeftEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)
        self.init()
        self.haseSave = True

    def init(self):
        self.scrollCallBack = None

    def scroll(self, dx: int, dy: int):
        print("scroll dx:%s dy:%s" % (dx, dy))
        super(LeftEdit, self).scroll(dx, dy)

    def scrollContentsBy(self, dx: int, dy: int):
        print("scrollContentsBy dx:%s dy:%s" % (dx, dy))
        super(LeftEdit, self).scrollContentsBy(dx, dy)
        if self.scrollCallBack:
            self.scrollCallBack(dx, dy)

    def setScrollCallBack(self, callback):
        self.scrollCallBack = callback

    def keyPressEvent(self, e: QKeyEvent):
        print(e.key())
        print(e.text())
        if e.key() == 16777217:
            print("tab 被按下")
            self.handleTest(e)
        else:
            super(LeftEdit, self).keyPressEvent(e)

    def handleTest(self, e: QKeyEvent):
        tab = "\t"

        cursor = self.textCursor()

        if cursor.hasSelection():
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            # 设置游标位置到最后
            cursor.setPosition(end)

            # 移动到选择的行的最后位置
            cursor.movePosition(cursor.StartOfLine)
            # 获取选择的段落的最终位置
            end = cursor.position()
            # cursor.movePosition(cursor.StartOfBlock)
            # endNumber = cursor.blockNumber()

            # 游标恢复到选择的开始位置
            cursor.setPosition(start)
            # cursor.movePosition(cursor.StartOfBlock)
            # startNumber = cursor.blockNumber()
            # print("startNumber = %s and endNumber = %s" % (startNumber, endNumber))
            # self.insertTab(startNumber, endNumber)
            # 移动到开始的问题的行头
            cursor.movePosition(cursor.StartOfLine)
            # 获取开始位置
            start = cursor.position()

            while start < end:
                cursor.movePosition(cursor.StartOfLine)

                _left = cursor.position()
                cursor.movePosition(cursor.EndOfLine)
                _right = cursor.position()

                cursor.movePosition(cursor.StartOfLine)
                cursor.insertText(tab)
                cursor.movePosition(cursor.NextBlock)
                cursor.movePosition(cursor.StartOfLine)
                lineLenght = _right - _left
                start = start + lineLenght
                # cursor.movePosition(cursor.StartOfLine)
        else:
            super(LeftEdit, self).keyPressEvent(e)

    def insertTab(self, satrt, end):
        self.document()
        txt = self.toPlainText()
        lines = txt.split("\n")
        for index, value in enumerate(lines):
            if index >= satrt and index <= end:
                lines[index] = "%s%s\n" % ("\t", value)
            else:
                lines[index] = "%s\n" % value

        self.setPlainText("".join(lines))


class MkEdit(QWidget):
    def __init__(self, parent=None):
        print("EditWidget __init__")
        QWidget.__init__(self, parent)
        self.init()
        self.initUI()
        self.initEvent()

    def interceptClose(self):
        if not self.haseSave:
            msgBox = QMessageBox()
            msgBox.setText("%s-文档已被修改" % self.fileName)
            msgBox.setInformativeText("是否保存修改后的文档")
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Save)
            ret = msgBox.exec_()
            print("ret:%s" % ret)
            if ret == QMessageBox.Save:
                print("save")
                self.save()
                self.haseSave = True
            elif ret == QMessageBox.Cancel:
                print("cancel")
                self.haseSave = False
            elif ret == QMessageBox.Discard:
                return False

        return not self.haseSave

    def save(self):
        if not self.haseSave:
            print("satrt save data")
            updateFile(self.filePath, self.leftEdit.toPlainText()).pipe(
                ops.subscribe_on(scheduler.ThreadPoolScheduler())
            ).subscribe(on_completed=lambda: self.handlerSaveResult())

    def handlerSaveResult(self):
        self.haseSave = True

    def loadData(self, filePath):
        self.filePath = filePath
        self.fileName = path.basename(self.filePath)
        result = list()
        with open(self.filePath, mode='r') as f:
            # for line in f.readlines():
            #     result.append(line)
            self.leftEdit.setPlainText("".join(f.readlines()))

    def __del__(self):
        print("EditWidget __del__")

    def setPlainText(self, text: str = ""):
        self.leftEdit.setPlainText(text)

    def init(self):
        renderer = Renderer(escape=True, hard_wrap=True)

        self.markdown = Markdown(renderer=renderer)

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.contentLayout = QHBoxLayout(self)
        self.contentLayout.setSpacing(0)
        self.leftEdit = LeftEdit(self)
        self.initLeftEdit()
        self.rightWebView = RightWebView(self)
        self.contentLayout.addWidget(self.leftEdit, 1)
        self.contentLayout.addWidget(self.rightWebView, 1)
        self.mainLayout.addLayout(self.contentLayout)
        self.setLayout(self.mainLayout)

    def initLeftEdit(self):
        shortcut = QShortcut(QKeySequence("Ctrl+S"), self.leftEdit)
        shortcut.activated.connect(self.save)
        font = QFont("Menlo", 14)
        self.leftEdit.setFont(font)
        self.leftEdit.setTabStopWidth(4 * QFontMetrics(font).width(" "))

    def initEvent(self):
        self.leftEdit.textChanged.connect(self.leftEditTextChange)

    def leftEditTextChange(self):
        self.haseSave = False
        self.rightWebView.setHtml(self.markdown.parse(self.leftEdit.toPlainText()))
