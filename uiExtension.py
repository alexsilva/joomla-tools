# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'extension.ui'
#
# Created: Sat Mar 23 16:39:11 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1110, 676)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("media/joomla_logo_black.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabConfig = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabConfig.sizePolicy().hasHeightForWidth())
        self.tabConfig.setSizePolicy(sizePolicy)
        self.tabConfig.setObjectName("tabConfig")
        self.tab = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(self.tab)
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(8)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_3 = QtGui.QFrame(self.groupBox)
        self.frame_3.setFrameShape(QtGui.QFrame.Box)
        self.frame_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.joomlaChoosePath = QtGui.QToolButton(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        self.joomlaChoosePath.setFont(font)
        self.joomlaChoosePath.setObjectName("joomlaChoosePath")
        self.horizontalLayout.addWidget(self.joomlaChoosePath)
        self.joomlaPath = QtGui.QLineEdit(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.joomlaPath.setFont(font)
        self.joomlaPath.setReadOnly(True)
        self.joomlaPath.setObjectName("joomlaPath")
        self.horizontalLayout.addWidget(self.joomlaPath)
        self.verticalLayout_4.addWidget(self.frame_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(8)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.frame_4 = QtGui.QFrame(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QtGui.QFrame.Box)
        self.frame_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtGui.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.componentName = QtGui.QLineEdit(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.componentName.setFont(font)
        self.componentName.setObjectName("componentName")
        self.horizontalLayout_4.addWidget(self.componentName)
        self.horizontalLayout_7.addWidget(self.frame_4)
        self.frame_2 = QtGui.QFrame(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtGui.QFrame.Box)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.componentChoosePath = QtGui.QToolButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        self.componentChoosePath.setFont(font)
        self.componentChoosePath.setObjectName("componentChoosePath")
        self.horizontalLayout_2.addWidget(self.componentChoosePath)
        self.componentPath = QtGui.QLineEdit(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.componentPath.setFont(font)
        self.componentPath.setReadOnly(True)
        self.componentPath.setObjectName("componentPath")
        self.horizontalLayout_2.addWidget(self.componentPath)
        self.pushButton = QtGui.QPushButton(self.frame_2)
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("media/zip.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout_7.addWidget(self.frame_2)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(8)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.frame_5 = QtGui.QFrame(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setFrameShape(QtGui.QFrame.Box)
        self.frame_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtGui.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.pluginName = QtGui.QLineEdit(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pluginName.setFont(font)
        self.pluginName.setObjectName("pluginName")
        self.horizontalLayout_5.addWidget(self.pluginName)
        self.horizontalLayout_8.addWidget(self.frame_5)
        self.frame = QtGui.QFrame(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pluginChoosePath = QtGui.QToolButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        self.pluginChoosePath.setFont(font)
        self.pluginChoosePath.setObjectName("pluginChoosePath")
        self.horizontalLayout_3.addWidget(self.pluginChoosePath)
        self.pluginPath = QtGui.QLineEdit(self.frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.pluginPath.setFont(font)
        self.pluginPath.setReadOnly(True)
        self.pluginPath.setObjectName("pluginPath")
        self.horizontalLayout_3.addWidget(self.pluginPath)
        self.pushButton_2 = QtGui.QPushButton(self.frame)
        self.pushButton_2.setText("")
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.horizontalLayout_8.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_5 = QtGui.QGroupBox(self.tab)
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.frame_7 = QtGui.QFrame(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setFrameShape(QtGui.QFrame.Box)
        self.frame_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.frame_7)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_3 = QtGui.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_9.addWidget(self.label_3)
        self.rateCheck = QtGui.QDoubleSpinBox(self.frame_7)
        self.rateCheck.setMaximum(300.0)
        self.rateCheck.setSingleStep(0.5)
        self.rateCheck.setProperty("value", 1.0)
        self.rateCheck.setObjectName("rateCheck")
        self.horizontalLayout_9.addWidget(self.rateCheck)
        self.horizontalLayout_10.addWidget(self.frame_7)
        self.frame_6 = QtGui.QFrame(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setFrameShape(QtGui.QFrame.Box)
        self.frame_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.frame_6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtGui.QLabel(self.frame_6)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.scanFilesRate = QtGui.QDoubleSpinBox(self.frame_6)
        self.scanFilesRate.setMinimum(10.0)
        self.scanFilesRate.setMaximum(1800.0)
        self.scanFilesRate.setSingleStep(5.0)
        self.scanFilesRate.setObjectName("scanFilesRate")
        self.horizontalLayout_6.addWidget(self.scanFilesRate)
        self.scanFilesNow = QtGui.QPushButton(self.frame_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scanFilesNow.sizePolicy().hasHeightForWidth())
        self.scanFilesNow.setSizePolicy(sizePolicy)
        self.scanFilesNow.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("media/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scanFilesNow.setIcon(icon2)
        self.scanFilesNow.setObjectName("scanFilesNow")
        self.horizontalLayout_6.addWidget(self.scanFilesNow)
        self.horizontalLayout_10.addWidget(self.frame_6)
        self.frame_8 = QtGui.QFrame(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setFrameShape(QtGui.QFrame.Box)
        self.frame_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_11 = QtGui.QHBoxLayout(self.frame_8)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.runningInfo = QtGui.QLabel(self.frame_8)
        self.runningInfo.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runningInfo.sizePolicy().hasHeightForWidth())
        self.runningInfo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("AR DELANEY")
        font.setPointSize(10)
        font.setItalic(True)
        self.runningInfo.setFont(font)
        self.runningInfo.setAutoFillBackground(False)
        self.runningInfo.setStyleSheet("color: rgb(0, 0, 255);")
        self.runningInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.runningInfo.setObjectName("runningInfo")
        self.horizontalLayout_11.addWidget(self.runningInfo)
        self.stoppedInfo = QtGui.QLabel(self.frame_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stoppedInfo.sizePolicy().hasHeightForWidth())
        self.stoppedInfo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("AR DELANEY")
        font.setPointSize(10)
        font.setItalic(True)
        self.stoppedInfo.setFont(font)
        self.stoppedInfo.setStyleSheet("color: rgb(170, 0, 0);")
        self.stoppedInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.stoppedInfo.setObjectName("stoppedInfo")
        self.horizontalLayout_11.addWidget(self.stoppedInfo)
        self.btnRun = QtGui.QPushButton(self.frame_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRun.sizePolicy().hasHeightForWidth())
        self.btnRun.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(10)
        self.btnRun.setFont(font)
        self.btnRun.setCheckable(True)
        self.btnRun.setObjectName("btnRun")
        self.horizontalLayout_11.addWidget(self.btnRun)
        self.horizontalLayout_10.addWidget(self.frame_8)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.tabConfig.addTab(self.tab, "")
        self.tabBrowser = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabBrowser.sizePolicy().hasHeightForWidth())
        self.tabBrowser.setSizePolicy(sizePolicy)
        self.tabBrowser.setObjectName("tabBrowser")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabBrowser)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabConfig.addTab(self.tabBrowser, "")
        self.verticalLayout.addWidget(self.tabConfig)
        self.groupBox_4 = QtGui.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.eventLog = QtGui.QPlainTextEdit(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eventLog.sizePolicy().hasHeightForWidth())
        self.eventLog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.eventLog.setFont(font)
        self.eventLog.setReadOnly(True)
        self.eventLog.setPlainText("")
        self.eventLog.setObjectName("eventLog")
        self.verticalLayout_5.addWidget(self.eventLog)
        self.verticalLayout.addWidget(self.groupBox_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1110, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabConfig.setCurrentIndex(0)
        QtCore.QObject.connect(self.btnRun, QtCore.SIGNAL("toggled(bool)"), self.stoppedInfo.setHidden)
        QtCore.QObject.connect(self.btnRun, QtCore.SIGNAL("toggled(bool)"), self.runningInfo.setVisible)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pluginPath, self.componentChoosePath)
        MainWindow.setTabOrder(self.componentChoosePath, self.componentPath)
        MainWindow.setTabOrder(self.componentPath, self.pluginChoosePath)
        MainWindow.setTabOrder(self.pluginChoosePath, self.joomlaPath)
        MainWindow.setTabOrder(self.joomlaPath, self.joomlaChoosePath)
        MainWindow.setTabOrder(self.joomlaChoosePath, self.componentName)
        MainWindow.setTabOrder(self.componentName, self.pluginName)
        MainWindow.setTabOrder(self.pluginName, self.eventLog)
        MainWindow.setTabOrder(self.eventLog, self.btnRun)
        MainWindow.setTabOrder(self.btnRun, self.rateCheck)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Joomla - AutoUp", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Joomla", None, QtGui.QApplication.UnicodeUTF8))
        self.joomlaChoosePath.setText(QtGui.QApplication.translate("MainWindow", "Choose Path", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Component", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.componentChoosePath.setText(QtGui.QApplication.translate("MainWindow", "Choose Path", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Zip all content.", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Plugin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginChoosePath.setText(QtGui.QApplication.translate("MainWindow", "Choose Path", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setToolTip(QtGui.QApplication.translate("MainWindow", "Zip all content.", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("MainWindow", "Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Rate check", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Scan Files", None, QtGui.QApplication.UnicodeUTF8))
        self.scanFilesNow.setToolTip(QtGui.QApplication.translate("MainWindow", "Rescan all files.", None, QtGui.QApplication.UnicodeUTF8))
        self.runningInfo.setText(QtGui.QApplication.translate("MainWindow", "RUNNING", None, QtGui.QApplication.UnicodeUTF8))
        self.stoppedInfo.setText(QtGui.QApplication.translate("MainWindow", "STOPPED", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRun.setText(QtGui.QApplication.translate("MainWindow", "execute", None, QtGui.QApplication.UnicodeUTF8))
        self.tabConfig.setTabText(self.tabConfig.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Configs", None, QtGui.QApplication.UnicodeUTF8))
        self.tabConfig.setTabText(self.tabConfig.indexOf(self.tabBrowser), QtGui.QApplication.translate("MainWindow", "Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("MainWindow", "Logs", None, QtGui.QApplication.UnicodeUTF8))

