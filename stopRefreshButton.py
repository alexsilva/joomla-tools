# coding: utf-8

import os

from PySide import QtGui


class StopRefreshButton(QtGui.QPushButton):
    def __init__(self, *arg):
        super(StopRefreshButton, self).__init__()
        self.btnState = {}
        self.setRefreshState()

    def setRefreshState(self):
        path = os.path.join("media", "refresh.png")
        self.setIcon(QtGui.QIcon(path))
        self.btnState["state"] = "refresh"
        self.setToolTip(self.tr("<b>reload</b>"))

    def setStopState(self):
        qicon = QtGui.QIcon(os.path.join("media", "btnstop-blue.png"))
        self.setIcon(qicon)
        self.btnState["state"] = "stop"
        self.setToolTip(self.tr("<b>stop</b>"))

    def __getitem__(self, key):
        return self.btnState[key]
