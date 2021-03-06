# coding: utf-8
import os
import sys

from PySide import QtCore
from PySide import QtGui
from PySide import QtWebKit

from stopRefreshButton import StopRefreshButton


class mWebView(QtWebKit.QWebView):

    def __init__(self, parent=None):
        super(mWebView, self).__init__(parent)
        self.movieSpin = QtGui.QMovie(os.path.join("media", "spin-progress.gif"))
        self.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        self.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)

    @staticmethod
    def setStrUrl(url):
        return url if isinstance(url, (str, unicode)) else url.toString()

    def getMovieSpinPixmap(self):
        return self.movieSpin.currentPixmap()

    def getCurrentUrl(self):
        return self.currentUrl

    def isLoadingPage(self):
        return self.loadingPage

    def onChangeUrl(self, url):
        self.currentUrl = self.setStrUrl(url)

    def onPageLoad(self):
        self.movieSpin.start()
        self.loadingPage = True

    def onPageFinished(self):
        self.loadingPage = False
        self.movieSpin.stop()

    def onProgress(self, progress):
        self.movieSpin.jumpToNextFrame()

    def load(self, url):
        self.currentUrl = self.setStrUrl(url)
        return super(mWebView, self).load(url)


class Browser(QtGui.QWidget):
    searchEngine = "http://localhost/web/administrator/"

    def __init__(self, parent=None):
        super(Browser, self).__init__(parent)
        vBox = QtGui.QVBoxLayout()

        self.webView = None
        self.mainWin = parent

        self.starEnableIcon = QtGui.QIcon(os.path.join(os.path.join("media", "btnstart-blue.png")))
        self.starDisableIcon = self.starEnableIcon.pixmap(QtCore.QSize(22, 22),
                                                          QtGui.QIcon.Disabled, QtGui.QIcon.Off)

        self.tabPagePanel = QtGui.QTabWidget(self)
        self.tabPagePanel.setTabsClosable(True)
        self.tabPagePanel.currentChanged.connect(self.updateWebView)
        self.tabPagePanel.tabCloseRequested.connect(self.handleTabCloseRequest)
        vBox.addLayout(self._createToolbar())

        vBox.addWidget(self.tabPagePanel)
        self.setupPage(self.searchEngine)

        self.setLayout(vBox)
        self.show()

    def __del__(self):
        del self.webView
        super(Browser, self).__del__()

    def setupPage(self, url="", isDefaulf=False):
        webView = mWebView(self.tabPagePanel)

        webView.linkClicked.connect(self.onLinkClicked)
        webView.loadStarted.connect(self.onPageLoad)
        webView.loadFinished.connect(self.onPageFinished)
        webView.loadProgress.connect(self.onProgress)
        webView.urlChanged.connect(self.onChangeUrl)
        webView.titleChanged.connect(self.onTitleChange)

        webView.load(QtCore.QUrl(url))
        webView.show()

        self.tabPagePanel.addTab(webView, self.tr("Loading..."))
        if isDefaulf: self.tabPagePanel.setCurrentWidget(webView)
        return webView

    @staticmethod
    def formatUrl(url):
        """ tornando automaticamente a url válida """
        url = "http://" + url if not url.startswith("http://") else url
        url = url + "/" if not url.endswith("/") else url
        return url

    def saveSettings(self):
        # salva os dados de navegação
        historyUrl = []
        for index in range(self.tabPagePanel.count()):
            webView = self.tabPagePanel.widget(index)
            historyUrl.append(webView.getCurrentUrl())

    def closeEvent(self, event):
        self.saveSettings()

    def handleTabCloseRequest(self, index):
        # garante que pelo menos um tabela exista(tabela padrão).
        if self.tabPagePanel.count() > 1:
            webView = self.tabPagePanel.widget(index)
            self.tabPagePanel.removeTab(index)
            webView.setHtml("")

    def paintEvent(self, event):
        history = self.webView.history()
        self.btnBack.setEnabled(history.canGoBack())
        self.btnForward.setEnabled(history.canGoForward())

    def updateWebView(self, index):
        webView = self.tabPagePanel.widget(index)

        if webView == self.tabPagePanel.currentWidget():
            self.location.setEditText(webView.getCurrentUrl())
            self.location.setToolTip(webView.getCurrentUrl())
            self.webView = webView

        if not webView.isLoadingPage():
            self.btnStopRefresh.setRefreshState()
        else:
            self.btnStopRefresh.setStopState()

    def onLinkClicked(self, url):
        """ controla o fluxo de links reconhecidos como válidos """
        cUrl = QtCore.QUrl(self.webView.getCurrentUrl())

        if url.host() == cUrl.host():
            self.webView.load(url)
        else:
            self.setupPage(url.toString())

    def onPageLoad(self):
        """ chamado ao iniciar o carregamento da página """
        webView = self.sender()
        webView.onPageLoad()

        self.btnStopRefresh.setStopState()
        self.updateFavoriteStarIcon()

    def onPageFinished(self):
        webView = self.sender()
        webView.onPageFinished()

        index = self.tabPagePanel.indexOf(webView)
        self.tabPagePanel.setTabIcon(index, webView.icon())

        self.btnStopRefresh.setRefreshState()

    def onProgress(self, porcent):
        webView = self.sender()
        webView.onProgress(porcent)

        self.tabPagePanel.setTabIcon(self.tabPagePanel.indexOf(webView),
                                     QtGui.QIcon(webView.getMovieSpinPixmap()))

    def onTitleChange(self, title):
        webView = self.sender()
        index = self.tabPagePanel.indexOf(webView)
        self.tabPagePanel.setTabText(index, title if len(title) < 20 else (title[:20] + "..."))
        self.tabPagePanel.setTabToolTip(index, title)

    def onChangeUrl(self, url):
        webView = self.sender()
        webView.onChangeUrl(url)

        if self.webView == webView:
            self.location.setEditText(webView.getCurrentUrl())
            self.location.setToolTip(webView.getCurrentUrl())

    def handleLocationPageLoad(self):
        url = self.location.currentText()
        self.webView.load(QtCore.QUrl(url))

    def handleEmbed(self):
        url = self.embed.currentText()
        if hasattr(self.mainWin, "getLocation"):
            self.mainWin.getLocation().setEditText(url)

    def handleStopRefresh(self):
        if self.btnStopRefresh["state"] == "refresh":
            self.webView.reload()

        elif self.btnStopRefresh["state"] == "stop":
            self.webView.stop()

    def reload(self):
        self.webView.reload()

    def handleFavoriteSite(self):
        text, ok = QtGui.QInputDialog.getText(self, self.tr("add url as favorite"),
                                              self.tr("Enter the url below."), text=self.location.currentText())
        text = text.strip()
        if text:
            text = self.formatUrl(text)

            # adicionando ao controle de url e ao banco de dados
            if self.objects.filter(site=text).count() == 0:
                if self.location.findText(text) < 0:
                    self.location.addItem(text)

                self.addSite(text)

                # atualiza o índice, com a nova url
                self.location.setCurrentIndex(self.location.findText(text))

                # atualizando a 'start' com ativa
                self.updateFavoriteStarIcon()
            else:
                reply = QtGui.QMessageBox.question(self, self.tr("without panic :)"),
                                                   self.tr("Url already in the list. Want to add another ?"),
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

                # tentando adicionar dados novamente.
                if reply == QtGui.QMessageBox.Yes:
                    self.handleFavoriteSite()
        elif ok:
            warningBoxEmpty = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                                self.tr("Empty ?"), self.tr("Enter a url first."),
                                                QtGui.QMessageBox.NoButton, self)

            warningBoxEmpty.addButton("Retry", QtGui.QMessageBox.AcceptRole)
            warningBoxEmpty.addButton("Cancel", QtGui.QMessageBox.RejectRole)

            # tentando adicionar dados novamente.
            if warningBoxEmpty.exec_() == QtGui.QMessageBox.AcceptRole:
                self.handleFavoriteSite()

    def handleUnFavoriteSite(self):
        url = self.formatUrl(self.location.currentText())

        index = self.location.findText(url)

        if index > -1:
            # ação que leva a remoção de uma url do banco de dados e do controle de urls.
            reply = QtGui.QMessageBox.question(self, self.tr("requires confirmation"),
                                               self.tr("The url below will be removed.\n") + url,
                                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                self.location.removeItem(index)

                # removendo do bando de dados
                query = self.objects.get(site=url)
                query.delete()

                self.location.setEditText(url)
        else:
            QtGui.QMessageBox.information(self, self.tr("Not found"),
                                          self.tr("The url can not be found in the current list."))

    def updateFavoriteStarIcon(self, url=""):
        url = self.formatUrl(url if url else self.location.currentText())
        # ToDo
        # if self.objects.filter(site=url).count() > 0:
        #    self.btnFavorite.setIcon(self.starEnableIcon)
        # else:
        #    self.btnFavorite.setIcon(self.starDisableIcon)

    def handleUrlAction(self):
        url = self.formatUrl(self.location.currentText())

        # ToDo
        # if self.objects.filter(site=url).count() == 0:
        #    self.handleFavoriteSite()
        # else:
        #    self.handleUnFavoriteSite()

    def _createToolbar(self):
        self.location = QtGui.QComboBox(self)
        # adicionando a lista de site favoritos.
        self.location.addItems([])

        self.location.activated.connect(self.handleLocationPageLoad)
        # fazendo eventos de edição atualizarem a 'start' de favoritos.
        self.location.editTextChanged.connect(self.updateFavoriteStarIcon)
        self.location.setEditable(True)
        self.location.show()

        ##
        self.embed = QtGui.QComboBox(self)
        self.embed.activated.connect(self.handleEmbed)
        self.embed.show()

        ## Back button
        self.btnBack = QtGui.QPushButton(self)
        path = os.path.join("media", "btnback-blue.png")
        self.btnBack.setIcon(QtGui.QIcon(path))
        self.btnBack.setToolTip(self.tr("<b>back</b>"))
        self.btnBack.clicked.connect(lambda: self.webView.back())
        self.btnBack.show()

        ## Foward button
        self.btnForward = QtGui.QPushButton(self)
        path = os.path.join("media", "btnforward-blue.png")
        self.btnForward.setIcon(QtGui.QIcon(path))
        self.btnForward.setToolTip(self.tr("<b>forward</b>"))
        self.btnForward.clicked.connect(lambda: self.webView.forward())
        self.btnForward.show()

        ## Refresh button
        self.btnStopRefresh = StopRefreshButton(self)
        self.btnStopRefresh.clicked.connect(self.handleStopRefresh)

        ## New page button
        self.btnNewPage = QtGui.QPushButton(self)
        path = os.path.join("media", "btnpage-blue.png")
        self.btnNewPage.setIcon(QtGui.QIcon(path))
        self.btnNewPage.setToolTip(self.tr("<b>new page</b>"))
        self.btnNewPage.clicked.connect(lambda: self.setupPage(self.searchEngine, True))
        self.btnNewPage.show()

        ## Favorite button
        self.btnFavorite = QtGui.QPushButton(self)
        self.btnFavorite.setToolTip(self.tr("<b>favorite</b>"))
        self.btnFavorite.setIcon(self.starEnableIcon)
        self.btnFavorite.clicked.connect(self.handleUrlAction)

        ## Refresh button
        btnSearch = QtGui.QPushButton(self)
        path = os.path.join("media", "btnsearch-blue.png")
        btnSearch.setIcon(QtGui.QIcon(path))
        btnSearch.setToolTip(self.tr("<b>search</b>"))
        btnSearch.clicked.connect(lambda: self.webView.load(self.searchEngine))
        btnSearch.show()

        hBoxLayout = QtGui.QHBoxLayout()

        hBoxLayout.addWidget(self.btnBack)
        hBoxLayout.addWidget(self.btnForward)
        hBoxLayout.addWidget(self.btnStopRefresh)

        hBoxLayout.addWidget(self.location, 1)
        hBoxLayout.addWidget(self.btnFavorite)
        hBoxLayout.addWidget(self.btnNewPage)
        hBoxLayout.addWidget(self.embed, 1)
        hBoxLayout.addWidget(btnSearch)
        return hBoxLayout


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = Browser()
    sys.exit(app.exec_())
