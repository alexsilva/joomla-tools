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
        self.news.emit( info )
        
## -----------------------------------------------------------------------------
class Loader(QtGui.QMainWindow):
    
    def __getattr__(self, name):
        if hasattr(self.uiMainWindow, name):
            attr = getattr(self.uiMainWindow, name);
        else:
            try: attr = super(Loader, self).__getattr__(name)
            except AttributeError as err:
                print "AttributeError: invalid name '%s'" % name
                raise err
        return attr
    
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
        
    def setDirectory(self):
        sender = self.sender()
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self, self.tr("Choose Dir"),
                                       sender.related.text(), options)
        sender.related.setText( directory )
    
    def onNews(self, info):
        self.eventLog.insertPlainText(info+"\n")
    
    def onBtnRunClicked(self):
        self.start() if self.btnRun.isChecked() else self.stop()
        
    def stop(self):
        self.runner.stop()
        
    def start(self):
        extentions = []
        joomla = self.joomlaPath.text()
        rate = self.rateCheck.value()
        
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
        
## ------------------------------------------------------------------------------------
app = QtGui.QApplication(sys.argv)

loader = Loader()
loader.show()

sys.exit(app.exec_())