# coding: utf-8
from PySide import QtCore, QtGui
from uiExtension import Ui_MainWindow
import extension
import sys
import os

## -----------------------------------------------------------------------------
class Event(extension.ExtEvent, QtCore.QObject):
    """ interface data """
    news = QtCore.Signal(str)
        
    def __init__(self):
        QtCore.QObject.__init__(self)
        extension.ExtEvent.__init__(self)
        
    def set(self, info):
        self.news.emit(info)
        
## -----------------------------------------------------------------------------
class Loader(QtGui.QMainWindow):
    """ MainWin loader """
    def __init__(self):
        super(Loader, self).__init__()
        
        self.uiMainWindow = Ui_MainWindow()
        self.uiMainWindow.setupUi(self)
        
        self.joomlaChoosePath.clicked.connect(self.setDirectory )
        self.joomlaChoosePath.related = self.joomlaPath
        
        self.componentChoosePath.clicked.connect(self.setDirectory )
        self.componentChoosePath.related = self.componentPath
        
        self.pluginChoosePath.clicked.connect(self.setDirectory )
        self.pluginChoosePath.related = self.pluginPath
        
        self.btnRun.clicked.connect(self.onBtnRunClicked)
        
        self._event = Event()
        self._event.news.connect(self.onNews)
        self.runner = None
        
        self.readSettings()
        self.runningInfo.setVisible(False)
        
    def setDirectory(self):
        sender = self.sender()
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self, self.tr("Choose Dir"),
                                    sender.related.text(), options)
        sender.related.setText(directory if os.path.exists(directory) else sender.related.text())
        
    def onNews(self, info):
        self.eventLog.appendPlainText(info)
        
    def onBtnRunClicked(self):
        self.start() if self.btnRun.isChecked() else self.stop()
        
    def stop(self):
        self.stopRunner()
        
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
        
    def stopRunner(self):
        """ safe stop """
        if hasattr(self.runner, "stop"):
            self.rateCheck.valueChanged.disconnect(self.runner.setRate)
            self.runner.stop() ## stop thread
        
    def start(self):
        extentions = []
        joomla = self.joomlaPath.text()
        rate = self.rateCheck.value()
        
        if not self.isValidJoomlaPath(joomla): return
        
        if os.path.exists(self.componentPath.text()):
            name = self.componentName.text()
            path = self.componentPath.text()
            
            extentions.append(extension.Component(name, path, joomla))
            
        if os.path.exists(self.pluginPath.text()):
            name = self.pluginName.text()
            path = self.pluginPath.text()
            
            extentions.append(extension.Plugin(name, path, joomla))
        
        # run a new thread
        self.runner = extension.Runner(extentions, self._event, rate)
        self.runner.start()
        
        # taxa de atualização
        self.rateCheck.valueChanged.connect(self.runner.setRate)
        
    def __getattr__(self, name):
        return (getattr(self.uiMainWindow, name) if hasattr(self.uiMainWindow, name) else
                        super(Loader, self).__getattr__(name))
                
    def closeEvent(self, event):
        self.stopRunner()
        
        settings = QtCore.QSettings("Developer", "AutoUpdate")
        settings.setValue("mainWindow/geometry", self.saveGeometry())
        settings.setValue("mainWindow/windowState", self.saveState())
        settings.setValue("paths/joomla", self.joomlaPath.text())
        settings.setValue("paths/component", self.componentPath.text())
        settings.setValue("names/component", self.componentName.text())
        settings.setValue("paths/plugin", self.pluginPath.text())
        settings.setValue("names/plugin", self.pluginName.text())
        settings.setValue("values/rate", self.rateCheck.value())
        return super(Loader,self).closeEvent(event)
        
    def readSettings(self):
        settings = QtCore.QSettings("Developer", "AutoUpdate")
        self.restoreGeometry(settings.value("mainWindow/geometry"))
        self.restoreState(settings.value("mainWindow/windowState"))
        self.joomlaPath.setText(settings.value("paths/joomla"))
        self.componentPath.setText(settings.value("paths/component"))
        self.componentName.setText(settings.value("names/component"))
        self.pluginPath.setText(settings.value("paths/plugin"))
        self.pluginName.setText(settings.value("names/plugin"))
        self.rateCheck.setValue(float(settings.value("values/rate", 1.0)))
        
## ------------------------------------------------------------------------------------
app = QtGui.QApplication(sys.argv)

loader = Loader()
loader.show()

sys.exit(app.exec_())