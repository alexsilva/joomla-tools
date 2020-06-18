# coding: utf-8
import os
import sys

from PySide import QtCore, QtGui

import extension
from uiExtension import Ui_MainWindow


## -----------------------------------------------------------------------------
class Event(extension.ExtEvent, QtCore.QObject):
    """ interface data """
    onInfo = QtCore.Signal(str)
    onError = QtCore.Signal(str)
    onStop = QtCore.Signal(str)
    onChanges = QtCore.Signal(str)

    def __init__(self):
        QtCore.QObject.__init__(self)
        extension.ExtEvent.__init__(self)

    def info(self, value):
        self.onInfo.emit(value)

    def error(self, value):
        self.onError.emit(value)

    def stop(self, value):
        self.onStop.emit(value)

    def changes(self, value):
        self.onChanges.emit(value)


## -----------------------------------------------------------------------------
class Loader(QtGui.QMainWindow):
    """ MainWin loader """

    def __init__(self):
        super(Loader, self).__init__()
        self.runner = None

        self.uiMainWindow = Ui_MainWindow()
        self.uiMainWindow.setupUi(self)
        self.runningInfo.setVisible(False)

        self.joomlaChoosePath.clicked.connect(self.setDirectory)
        self.joomlaChoosePath.related = self.joomlaPath

        self.componentChoosePath.clicked.connect(self.setDirectory)
        self.componentChoosePath.related = self.componentPath

        self.pluginChoosePath.clicked.connect(self.setDirectory)
        self.pluginChoosePath.related = self.pluginPath

        self.moduleChoosePath.clicked.connect(self.setDirectory)
        self.moduleChoosePath.related = self.modulePath

        self.btnRun.clicked.connect(self.onBtnRunClicked)

        # taxa de atualização
        self.rateCheck.valueChanged.connect(self.setRate)
        # taxa de escaneamento de arquivos
        self.scanFilesRate.valueChanged.connect(self.setScanRate)
        # força o escaneamento dos arquivos
        self.scanFilesNow.clicked.connect(self.scanNow)

        self._event = Event()
        self._event.onInfo.connect(self.onInfo)
        self._event.onError.connect(self.onError)
        self._event.onStop.connect(self.onStop)
        self._event.onChanges.connect(self.onChanges)

        self.readSettings()

    def onInfo(self, info):
        self.eventLog.appendHtml('<p style="color:#184a7d;">%s</p>' % info)

    def onError(self, info):
        self.eventLog.appendHtml('<p style="color:red;">%s</p>' % info)
        self.btnRun.setChecked(False)  # stop on error

    def onStop(self, info):
        self.eventLog.appendHtml('<p style="color:blue;">%s</p>' % info)

    def onChanges(self, info):
        self.eventLog.appendHtml('<p style="color:green;">%s</p>' % info)

    def setDirectory(self):
        sender = self.sender()
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self, self.tr("Choose Dir"),
                                                           sender.related.text(), options)
        sender.related.setText(directory if os.path.exists(directory) else sender.related.text())

    def onBtnRunClicked(self):
        self.start() if self.btnRun.isChecked() else self.stop()

    def isValidJoomlaPath(self, path):
        if not os.path.exists(path):
            QtGui.QMessageBox.critical(self, self.tr("Path Invalid!"),
                                       self.tr("Joomla path not set or is invalid."),
                                       QtGui.QMessageBox.Ok)
            self.btnRun.setChecked(False)
            valid = False
        else:
            valid = True
        return valid

    def setRate(self, value):
        if self.runner: self.runner.setRate(value)

    def setScanRate(self, value):
        if self.runner: self.runner.setScanRate(value)

    def scanNow(self):
        if self.runner: self.runner.scanFiles()

    def start(self):
        extentions = []
        joomla = self.joomlaPath.text()

        scanRate = self.scanFilesRate.value()
        rate = self.rateCheck.value()

        if not self.isValidJoomlaPath(joomla):
            return

        if os.path.exists(self.componentPath.text()):
            name = self.componentName.text()
            path = self.componentPath.text()
            extentions.append(extension.Component(name, path, joomla, self._event))

        if os.path.exists(self.pluginPath.text()):
            name = self.pluginName.text()
            path = self.pluginPath.text()
            extentions.append(extension.Plugin(name, path, joomla, self._event))

        if os.path.exists(self.modulePath.text()):
            name = self.moduleName.text()
            path = self.modulePath.text()
            extentions.append(extension.Module(name, path, joomla, self._event))

        # run a new thread
        self.runner = extension.Runner(extentions, self._event, scanRate, rate)
        self.runner.start()

    def stop(self):
        if self.runner: self.runner.stop()  ## stop thread

    def __getattr__(self, name):
        return (getattr(self.uiMainWindow, name) if hasattr(self.uiMainWindow, name) else
                super(Loader, self).__getattr__(name))

    def closeEvent(self, event):
        settings = QtCore.QSettings("Developer", "AutoUpdate")

        settings.setValue("mainWindow/geometry", self.saveGeometry())
        settings.setValue("mainWindow/windowState", self.saveState())

        settings.setValue("paths/joomla", self.joomlaPath.text())

        settings.setValue("paths/component", self.componentPath.text())
        settings.setValue("names/component", self.componentName.text())

        settings.setValue("paths/plugin", self.pluginPath.text())
        settings.setValue("names/plugin", self.pluginName.text())

        settings.setValue("paths/module", self.modulePath.text())
        settings.setValue("names/module", self.moduleName.text())

        settings.setValue("values/rate", self.rateCheck.value())
        settings.setValue("values/scanFiles", self.scanFilesRate.value())

        return super(Loader, self).closeEvent(event)

    def readSettings(self):
        settings = QtCore.QSettings("Developer", "AutoUpdate")

        self.restoreGeometry(settings.value("mainWindow/geometry"))
        self.restoreState(settings.value("mainWindow/windowState"))

        self.joomlaPath.setText(settings.value("paths/joomla"))

        self.componentPath.setText(settings.value("paths/component"))
        self.componentName.setText(settings.value("names/component"))

        self.pluginPath.setText(settings.value("paths/plugin"))
        self.pluginName.setText(settings.value("names/plugin"))

        self.modulePath.setText(settings.value("paths/module"))
        self.moduleName.setText(settings.value("names/module"))

        self.rateCheck.setValue(float(settings.value("values/rate", 1.0)))
        self.scanFilesRate.setValue(float(settings.value("values/scanFiles", 10.0)))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    loader = Loader()
    loader.show()

    sys.exit(app.exec_())
