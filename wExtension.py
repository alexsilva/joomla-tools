from PySide import QtCore, QtGui
from uiExtension import Ui_MainWindow
import extension
import sys
import os

## -----------------------------------------------------------------------------
class Event(extension.ExtEvent):
    """ interface test """
    
    def __init__(self):
        super(Event, self).__init__()
        
    def set(self, info):
        print info
        
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
        
        self.btnRun.clicked.connect(self.start)
        
    def setDirectory(self):
        sender = self.sender()
        
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self, self.tr("Choose Dir"),
                                       sender.related.text(), options)
        sender.related.setText( directory )
    
    def start(self):
        extentions = []
        joomla = self.joomlaPath.text()
        
        if os.path.exists(self.componentPath.text()):
            name = self.componentName.text()
            path = self.componentPath.text()
            
            extentions.append(extension.Component(name, path, joomla))
        
        if os.path.exists(self.pluginPath.text()):
            name = self.pluginName.text()
            path = self.pluginPath.text()
            
            extentions.append(extension.Plugin(name, path, joomla))
        
        # run a new thread
        runner = extension.Runner(extentions, )
        runner.start()
        
## ------------------------------------------------------------------------------------
app = QtGui.QApplication(sys.argv)

loader = Loader()
loader.show()

sys.exit(app.exec_())