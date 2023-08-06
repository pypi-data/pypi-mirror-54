import asyncio
from datetime import datetime

from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidgetAction
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QToolTip

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import QWebEnginePage

from PyQt5.QtCore import QRect
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QMimeData
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QPoint

from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QKeySequence

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from galacteek.ipfs.stat import StatInfo
from galacteek.ipfs.wrappers import ipfsOp
from galacteek.ipfs.cidhelpers import IPFSPath
from galacteek import ensure
from galacteek.core import parseDate
from galacteek.core.asynclib import asyncify
from galacteek.dweb.markdown import markitdown

from .helpers import getIcon
from .helpers import getIconFromIpfs
from .helpers import disconnectSig
from .helpers import sizeFormat
from .helpers import messageBox
from .i18n import iCancel
from .i18n import iUnknown
from .i18n import iLocalHashmarksCount
from .i18n import iSearchHashmarks
from .i18n import iSearchHashmarksAllAcross
from .i18n import iSearchUseShiftReturn
from .i18n import iHashmarkInfoToolTip


class GalacteekTab(QWidget):
    def __init__(self, gWindow, **kw):
        super(GalacteekTab, self).__init__(gWindow)
        self.vLayout = QVBoxLayout(self)
        self.setLayout(self.vLayout)

        self.gWindow = gWindow
        self.setAttribute(Qt.WA_DeleteOnClose)

    def tabIndex(self, w=None):
        return self.gWindow.tabWidget.indexOf(w if w else self)

    def setTabName(self, name, widget=None):
        idx = self.tabIndex(w=widget)
        if idx >= 0:
            self.gWindow.tabWidget.setTabText(idx, name)

    def addToLayout(self, widget):
        self.vLayout.addWidget(widget)

    def onClose(self):
        return True

    @ipfsOp
    async def initialize(self, op):
        pass

    @property
    def app(self):
        return self.gWindow.app

    @property
    def loop(self):
        return self.app.loop

    @property
    def profile(self):
        return self.app.ipfsCtx.currentProfile


class HorizontalLine(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet('''
            QFrame {
                background-color: #4a9ea1;
            }
        ''')


class URLDragAndDropProcessor:
    fileDropped = pyqtSignal(QUrl)
    ipfsObjectDropped = pyqtSignal(IPFSPath)

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()

        if mimeData.hasUrls() or mimeData.hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        mimeData = event.mimeData()

        if mimeData is None:
            return

        if mimeData.hasUrls():
            for url in mimeData.urls():
                if not url.isValid():
                    continue

                if url.scheme() == 'file' and url.isValid():
                    self.fileDropped.emit(url)
                else:
                    path = IPFSPath(url.toString(), autoCidConv=True)
                    if path.valid:
                        self.ipfsObjectDropped.emit(path)
        elif mimeData.hasText():
            text = mimeData.text()
            path = IPFSPath(text, autoCidConv=True)

            if path.valid:
                self.ipfsObjectDropped.emit(path)

        event.acceptProposedAction()


class CheckableToolButton(QToolButton):
    def __init__(self, toggled=None, icon=None, parent=None):
        super(CheckableToolButton, self).__init__(parent)
        self.setCheckable(True)
        self.setAutoRaise(True)

        if toggled:
            self.toggled.connect(toggled)

        if icon:
            self.setIcon(icon)


class IPFSPathClipboardButton(QToolButton):
    def __init__(self, ipfsPath, parent=None):
        super(IPFSPathClipboardButton, self).__init__(parent)

        self.setEnabled(False)
        self.setIcon(getIcon('clipboard.png'))
        self.app = QApplication.instance()
        self.path = ipfsPath
        self.clicked.connect(self.onClicked)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if isinstance(path, IPFSPath) and path.valid:
            self.setEnabled(True)
            self.setToolTip('Copy to clipboard: {}'.format(str(path)))
            self._path = path

    def onClicked(self):
        if isinstance(self.path, IPFSPath) and self.path.valid:
            self.app.setClipboardText(str(self.path))


class IPFSUrlLabel(QLabel):
    def __init__(self, ipfsPath, invalidPathLabel='Invalid path', parent=None):
        super(IPFSUrlLabel, self).__init__(parent)
        self.app = QApplication.instance()

        self.invalidPathMessage = invalidPathLabel
        self.path = ipfsPath
        self.linkActivated.connect(self.onLinkClicked)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, val):
        self._path = val

        if self.path and self.path.valid:
            self.url = QUrl(self.path.ipfsUrl)
            self.setText('<a href="{url}">{url}</a>'.format(
                url=self.url.toString()))
        else:
            self.url = None
            self.setText(self.invalidPathMessage)

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()

        if mimeData.hasUrls() or mimeData.hasText():
            event.acceptProposedAction()

    def mimeData(self, indexes):
        mimedata = QMimeData()
        mimedata.setUrls([self.url])
        return mimedata

    def onLinkClicked(self, urlString):
        ensure(self.app.resourceOpener.open(self.path))


class LabelWithURLOpener(QLabel):
    """
    QLabel which opens http/https URLs in a tab.
    Used by the 'About' dialog
    """

    def __init__(self, text, parent=None):
        super(LabelWithURLOpener, self).__init__(text, parent)
        self.app = QApplication.instance()
        self.linkActivated.connect(self.onLinkClicked)

    def onLinkClicked(self, urlString):
        url = QUrl(urlString)
        if url.isValid() and url.scheme() in ['http', 'https']:
            tab = self.app.mainWindow.addBrowserTab()
            tab.enterUrl(url)


class PopupToolButton(QToolButton, URLDragAndDropProcessor):
    def __init__(self, icon=None, parent=None, menu=None,
                 mode=QToolButton.MenuButtonPopup, acceptDrops=False,
                 menuSizeHint=None, toolTipsVisible=True):
        super(PopupToolButton, self).__init__(parent)

        self.menu = menu if menu else QMenu(self)
        self.menu.setToolTipsVisible(toolTipsVisible)
        self.setPopupMode(mode)
        self.setMenu(self.menu)
        self.setAcceptDrops(acceptDrops)

        if icon:
            self.setIcon(icon)


class IPFSObjectToolButton(QToolButton):
    """
    Used in the quickaccess toolbar
    """
    deleteRequest = pyqtSignal()

    def __init__(self, ipfsPath, icon=None, parent=None):
        super(IPFSObjectToolButton, self).__init__(parent=parent)
        if icon:
            self.setIcon(icon)

    def mousePressEvent(self, event):
        button = event.button()

        if button == Qt.RightButton:
            menu = QMenu(self)
            menu.addAction('Remove', lambda: self.deleteRequest.emit())
            menu.exec(self.mapToGlobal(event.pos()))

        super().mousePressEvent(event)


class HashmarkToolButton(QToolButton):
    """
    Used in the quickaccess toolbar
    """
    deleteRequest = pyqtSignal()

    def __init__(self, mark, icon=None, parent=None):
        super(HashmarkToolButton, self).__init__(parent=parent)
        if icon:
            self.setIcon(icon)

        self._hashmark = mark

    @property
    def hashmark(self):
        return self._hashmark

    def mousePressEvent(self, event):
        button = event.button()

        if button == Qt.RightButton:
            menu = QMenu(self)
            menu.addAction('Remove', lambda: self.deleteRequest.emit())
            menu.exec(self.mapToGlobal(event.pos()))

        super().mousePressEvent(event)


class _HashmarksCommon:
    def makeAction(self, path, mark, loadIcon=True):
        tLenMax = 64
        title = mark['metadata'].get('title')
        description = mark['metadata'].get('description')
        datecreated = mark.get('datecreated')
        icon = mark.get('icon')

        if title and len(title) > tLenMax:
            title = '{0} ...'.format(title[0:tLenMax])

        dt = parseDate(datecreated)
        if dt:
            dateHuman = dt.isoformat(' ', timespec='minutes')
        else:
            dateHuman = iUnknown()

        action = QAction(title, self)
        action.setToolTip(
            iHashmarkInfoToolTip(path, title, description, dateHuman))

        action.setData({
            'path': path,
            'mark': mark,
            'iconcid': icon
        })

        if not icon or not loadIcon:
            # Default icon
            action.setIcon(getIcon('ipfs-logo-128-white-outline.png'))
        else:
            ensure(self.loadMarkIcon(action, icon))

        return action

    @ipfsOp
    async def loadMarkIcon(self, ipfsop, action, iconCid):
        data = action.data()

        if isinstance(data, dict) and 'iconloaded' in data:
            return

        icon = await getIconFromIpfs(ipfsop, iconCid)

        if icon:
            await ipfsop.sleep()

            action.setIcon(icon)
            data['iconloaded'] = True
            action.setData(data)


class HashmarkMgrButton(PopupToolButton, _HashmarksCommon):
    hashmarkClicked = pyqtSignal(str, str)

    def __init__(self, marks, iconFile='hashmarks.png',
                 maxItemsPerCategory=128, parent=None):
        super(HashmarkMgrButton, self).__init__(parent=parent,
                                                mode=QToolButton.InstantPopup)

        self.setObjectName('hashmarksMgrButton')
        self.menu.setObjectName('hashmarksMgrMenu')
        self.menu.setToolTipsVisible(True)
        self.hCount = 0
        self.marks = marks
        self.cMenus = {}
        self.maxItemsPerCategory = maxItemsPerCategory
        self.setIcon(getIcon(iconFile))

        disconnectSig(self.marks.changed, self.onChanged)

        self.marks.changed.connect(self.onChanged)
        self.marks.markAdded.connect(self.onMarkAdded)
        self.marks.markDeleted.connect(self.onMarkDeleted)

    def onMarkAdded(self):
        ensure(self.updateIcons())

    def onMarkDeleted(self, category, path):
        if category in self.cMenus:
            menu = self.cMenus[category]

            for action in menu.actions():
                data = action.data()
                if data and data['path'] == path:
                    menu.removeAction(action)

            if menu.isEmpty():
                menu.hide()

    def onChanged(self):
        self.updateMenu()

    async def updateIcons(self):
        for mName, menu in self.cMenus.items():
            await asyncio.sleep(0)

            for action in menu.actions():
                data = action.data()

                if 'iconloaded' not in data and data['iconcid']:
                    ensure(self.loadMarkIcon(action, data['iconcid']))

    def updateMenu(self):
        self.hCount = 0
        categories = self.marks.getCategories()

        for category in categories:
            marks = self.marks.getCategoryMarks(category)
            mItems = marks.items()

            if len(mItems) not in range(1, self.maxItemsPerCategory):
                continue

            if category not in self.cMenus:
                self.cMenus[category] = QMenu(category)
                self.cMenus[category].setToolTipsVisible(True)
                self.cMenus[category].triggered.connect(self.linkActivated)
                self.cMenus[category].setObjectName('hashmarksMgrMenu')
                self.menu.addMenu(self.cMenus[category])

            menu = self.cMenus[category]
            menu.setIcon(getIcon('stroke-cube.png'))

            def exists(path):
                for action in menu.actions():
                    if action.data()['path'] == path:
                        return action

            if len(mItems) in range(1, self.maxItemsPerCategory):
                for path, mark in mItems:
                    self.hCount += 1

                    if exists(path):
                        continue

                    menu.addAction(self.makeAction(path, mark))
            else:
                menu.hide()

        self.setToolTip(iLocalHashmarksCount(self.hCount))

    def linkActivated(self, action):
        data = action.data()
        path, mark = data['path'], data['mark']

        if mark:
            if 'metadata' not in mark:
                return
            self.hashmarkClicked.emit(
                path,
                mark['metadata']['title']
            )


class HashmarksSearchWidgetAction(QWidgetAction):
    pass


class HashmarksSearchLine(QLineEdit):
    """
    The hashmarks search line edit.

    Run the search when Shift + Return is pressed.
    """
    searchRequest = pyqtSignal(str)
    returnNoModifier = pyqtSignal()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def keyPressEvent(self, event):
        if event.type() == QEvent.KeyPress:
            modifiers = event.modifiers()
            key = event.key()

            if modifiers & Qt.ShiftModifier:
                if key == Qt.Key_Return:
                    searchText = self.text().strip()
                    if searchText:
                        self.searchRequest.emit(searchText)

                    return
            else:
                if event.key() == Qt.Key_Return:
                    self.returnNoModifier.emit()
                    return

        return super().keyPressEvent(event)


class HashmarksSearcher(PopupToolButton, _HashmarksCommon):
    hashmarkClicked = pyqtSignal(str, str)

    def __init__(self, iconFile='hashmarks-library.png', parent=None,
                 mode=QToolButton.InstantPopup):
        super(HashmarksSearcher, self).__init__(parent=parent, mode=mode)

        self.app = QApplication.instance()

        self._catalog = {}
        self._sMenus = []
        self.setObjectName('hashmarksSearcher')

        self.setIcon(getIcon(iconFile))
        self.setShortcut(QKeySequence('Ctrl+Alt+h'))

        self.menu.setTitle(iSearchHashmarks())
        self.menu.setIcon(getIcon(iconFile))
        self.menu.setObjectName('hashmarksSearchMenu')
        self.menu.setToolTipsVisible(True)
        self.menu.aboutToShow.connect(self.aboutToShowMenu)
        self.configureMenu()

    @property
    def searchesCount(self):
        return len(self.menu.actions()) - len(self.protectedActions)

    @property
    def protectedActions(self):
        return [self.searchWAction, self.clearAction]

    def isProtectedAction(self, action):
        for pAction in self.protectedActions:
            if action is pAction:
                return True
        return False

    def aboutToShowMenu(self):
        self.searchLine.setFocus(Qt.OtherFocusReason)

    def configureMenu(self):
        self.clearAction = QAction(
            getIcon('clear-all.png'),
            'Clear searches',
            self.menu,
            triggered=self.onClearSearches
        )
        self.clearAction.setEnabled(False)
        self.searchLine = HashmarksSearchLine(self.menu)
        self.searchLine.setObjectName('hLibrarySearch')

        mediumSize = self.fontMetrics().size(0, '*' * (40))
        self.searchLine.setMinimumSize(QSize(mediumSize.width(), 32))
        self.searchLine.setFocusPolicy(Qt.StrongFocus)

        self.searchLine.returnNoModifier.connect(self.onReturnNoShift)
        self.searchLine.searchRequest.connect(self.onSearch)
        self.searchLine.setToolTip(iSearchHashmarksAllAcross())

        self.searchLine.setValidator(
            QRegExpValidator(QRegExp(r"[\w\s@\+\-_./?'\"!#]+")))
        self.searchLine.setMaxLength(96)
        self.searchLine.setClearButtonEnabled(True)

        self.searchWAction = HashmarksSearchWidgetAction(self.menu)
        self.searchWAction.setDefaultWidget(self.searchLine)
        self.menu.addAction(self.searchWAction)
        self.menu.setDefaultAction(self.searchWAction)
        self.menu.addAction(self.clearAction)

    def onReturnNoShift(self):
        QToolTip.showText(self.searchLine.mapToGlobal(
            QPoint(30, self.searchLine.height())),
            iSearchUseShiftReturn(),
            self.searchLine, QRect(0, 0, 0, 0), 1800)

    def onSearch(self, text):
        for action in self.menu.actions():
            if self.isProtectedAction(action):
                continue
            if action.text() == text:
                self.menu.removeAction(action)

        ensure(self.searchInCatalog(text))

    @asyncify
    async def searchInCatalog(self, text):
        resultsMenu = QMenu(text, self.menu)
        resultsMenu.setToolTipsVisible(True)
        resultsMenu.setObjectName('hashmarksSearchMenu')
        resultsMenu.triggered.connect(
            lambda action: self.linkActivated(
                action, closeMenu=True))
        resultsMenu.menuAction().setData({
            'query': text,
            'datecreated': datetime.now()
        })

        sources = [marks for sender, marks in self._catalog.items()]
        sources.append(self.app.marksLocal)
        showMax = 128
        added = 0

        for marks in sources:
            await asyncio.sleep(0)

            async for hashmark in marks.searchAllByMetadata({
                'path': text,
                'title': text,
                'description': text,
                'comment': text
            }):

                await asyncio.sleep(0)
                resultsMenu.addAction(self.makeAction(
                    hashmark.path, hashmark.markData))

                if added > showMax:
                    break

                added += 1

        if len(resultsMenu.actions()) > 0:
            self.menu.addMenu(resultsMenu)
            resultsMenu.setIcon(getIcon('search-engine.png'))

        self.clearAction.setEnabled(self.searchesCount > 0)
        self.searchLine.clear()

    def onClearSearches(self):
        for action in self.menu.actions():
            if not self.isProtectedAction(action):
                self.menu.removeAction(action)

        self.clearAction.setEnabled(self.searchesCount > 0)

    def register(self, nodeId, ipfsMarks):
        if nodeId in self._catalog.keys():
            del self._catalog[nodeId]

        self._catalog[nodeId] = ipfsMarks

    def linkActivated(self, action, closeMenu=False):
        data = action.data()
        path, mark = data['path'], data['mark']

        if mark:
            if 'metadata' not in mark:
                return

            self.hashmarkClicked.emit(
                path,
                mark['metadata']['title']
            )

            self.searchLine.clear()
            if closeMenu:
                self.menu.hide()


class ImageWidget(QLabel):
    """
    Displays an image stored in IPFS into a QLabel
    """

    def __init__(self, scaleWidth=64, parent=None):
        super(ImageWidget, self).__init__(parent)

        self._imgPath = None
        self._scaleWidth = scaleWidth

    @property
    def imgPath(self):
        return self._imgPath

    @ipfsOp
    async def load(self, ipfsop, path):
        try:
            imgData = await ipfsop.waitFor(
                ipfsop.client.cat(path), 8
            )

            if not imgData:
                raise Exception('Failed to load image')

            img1 = QImage()
            img1.loadFromData(imgData)
            img = img1.scaledToWidth(self._scaleWidth)

            self.setPixmap(QPixmap.fromImage(img))
            self._imgPath = path
            return True
        except Exception:
            return False


class DownloadProgressButton(PopupToolButton):
    downloadProgress = pyqtSignal(int)
    downloadFinished = pyqtSignal()
    cancelled = pyqtSignal()

    def __init__(self, path, stat, parent=None):
        super(DownloadProgressButton, self).__init__(
            icon=getIcon('download.png'),
            parent=parent, mode=QToolButton.InstantPopup)
        self.downloadProgress.connect(self.onProgress)
        self.downloadFinished.connect(self.onFinished)
        self.path = path
        self.stat = stat
        self.readBytes = 0
        self.task = None

        self.menu.addAction(iCancel(), self.onCancel)

    def onCancel(self):
        if self.task:
            try:
                self.task.cancel()
            except:
                pass

            self.cancelled.emit()

    def onProgress(self, read):
        statInfo = StatInfo(self.stat)

        self.readBytes = read
        size = sizeFormat(statInfo.totalSize) if statInfo.valid else \
            iUnknown()

        self.setToolTip('{path} (size: {size}): downloaded {dl}'.format(
            path=self.path,
            size=size,
            dl=sizeFormat(self.readBytes))
        )

    def onFinished(self):
        self.setToolTip('{path}: download finished'.format(path=self.path))


class IconSelector(QComboBox):
    """
    A simple icon selector. The selected icon is injected in the
    repository and a signal with its CID is emitted
    """
    iconSelected = pyqtSignal(str)
    emptyIconSelected = pyqtSignal()

    iconsList = [
        ':/share/icons/distributed.png',
        ':/share/icons/atom.png',
        ':/share/icons/atom-rpg.png',
        ':/share/icons/cerebro.png',
        ':/share/icons/ipfs-cube-64.png',
        ':/share/icons/ipfs-logo-128-white.png',
        ':/share/icons/code-fork.png',
        ':/share/icons/cube-blue.png',
        ':/share/icons/cube-orange.png',
        ':/share/icons/cubehouse.png',
        ':/share/icons/fragments.png',
        ':/share/icons/go-home.png',
        ':/share/icons/hotspot.png',
        ':/share/icons/ipld-logo.png',
        ':/share/icons/pyramid-aqua.png',
        ':/share/icons/pyramid-stack.png',
        ':/share/icons/multimedia.png',
        ':/share/icons/folder-documents.png',
        ':/share/icons/folder-pictures.png',
        ':/share/icons/orbitdb.png',
        ':/share/icons/pyramid-hierarchy.png',
        ':/share/icons/sweethome.png',
        ':/share/icons/stroke-code.png',
        ':/share/icons/web-devel.png',
        ':/share/icons/mimetypes/image-x-generic.png',
        ':/share/icons/mimetypes/application-pdf.png',
        ':/share/icons/mimetypes/application-epub+zip.png',
        ':/share/icons/mimetypes/application-x-directory.png',
        ':/share/icons/mimetypes/text-html.png'
    ]

    def __init__(self, parent=None, offline=False, allowEmpty=False):
        super(IconSelector, self).__init__(parent)

        self.app = QApplication.instance()
        self.allowEmpty = allowEmpty
        self.offline = offline
        self.iconCid = None

        if self.app.system == 'Linux':
            self.setIconSize(QSize(64, 64))

        if allowEmpty is True:
            self.addItem('No icon')

        for iconP in self.iconsList:
            icon = getIcon(iconP)
            if icon:
                self.addItem(icon, '', QVariant(iconP))

        self.view = QListView(self)
        self.setView(self.view)
        self.currentIndexChanged.connect(self.onIndexChanged)

        if allowEmpty is False:
            self.injectCurrent()

    def injectCurrent(self):
        self.injectIconFromIndex(self.currentIndex())

    def injectIconFromIndex(self, idx):
        iconPath = self.itemData(idx)
        if iconPath:
            ensure(self.injectQrcIcon(iconPath))

    def onIndexChanged(self, idx):
        if self.allowEmpty and idx == 0:
            self.emptyIconSelected.emit()
        else:
            self.injectIconFromIndex(idx)

    @ipfsOp
    async def injectQrcIcon(self, op, iconPath):
        _file = QFile(iconPath)
        if _file.exists():
            if not _file.open(QIODevice.ReadOnly):
                return False

            data = _file.readAll().data()

            entry = await op.addBytes(data, offline=self.offline)
            if entry:
                self.iconCid = entry['Hash']
                self.iconSelected.emit(self.iconCid)
                self.setToolTip(self.iconCid)
                return True


class IPFSWebView(QWebEngineView):
    def __init__(self, webProfile=None, parent=None):
        super(IPFSWebView, self).__init__(parent=parent)

        self.app = QApplication.instance()
        self.webProfile = webProfile if webProfile else \
            self.app.webProfiles['ipfs']
        self.setPage(QWebEnginePage(self.webProfile, self))

        self.setMinimumSize(QSize(
            self.app.desktopGeometry.width() / 8,
            self.app.desktopGeometry.height() / 8
        ))


class MarkdownView(IPFSWebView):
    pass


class MarkdownInputWidget(QWidget):
    """
    General purpose markdown input editor, with (almost) live
    preview in a qtwebengine view

    It supports the 'dweb' URL scheme, so when you type something
    like ![img](dweb:/pathtoimage) the image should appear in
    the preview widget
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = QApplication.instance()

        self.markdownDocButton = QPushButton(
            'Have you completely lost your Markdown ?')
        self.markdownDocButton.setMaximumWidth(600)

        self.markdownDocButton.clicked.connect(self.onMarkdownHelp)
        helpLayout = QHBoxLayout()
        labelsLayout = QHBoxLayout()
        labelsLayout.addWidget(QLabel('Markdown input'))
        labelsLayout.addWidget(QLabel('Preview'))

        helpLayout.addWidget(self.markdownDocButton)
        helpLayout.addItem(
            QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.textEditUser = QTextEdit(self)
        self.textEditUser.textChanged.connect(self.onEdited)
        self.textEditMarkdown = MarkdownView(parent=self)

        self.updateTimeoutMs = 500
        self.updateTimer = QTimer()
        self.updateTimer.timeout.connect(self.onTimerOut)

        mainLayout = QVBoxLayout()
        editLayout = QHBoxLayout()
        editLayout.addWidget(self.textEditUser)
        editLayout.addWidget(self.textEditMarkdown)

        mainLayout.addLayout(labelsLayout)
        mainLayout.addLayout(editLayout)
        mainLayout.addLayout(helpLayout)

        self.setLayout(mainLayout)
        self.setMinSize()

    def onMarkdownHelp(self):
        ref = self.app.ipfsCtx.resources.get('markdown-reference')
        if ref:
            self.app.mainWindow.addBrowserTab().browseIpfsHash(
                ref['Hash']
            )

    def setMinSize(self):
        self.textEditUser.setMinimumSize(QSize(
            self.app.desktopGeometry.width() / 3,
            self.app.desktopGeometry.height() / 2)
        )
        self.textEditMarkdown.setMinimumSize(QSize(
            self.app.desktopGeometry.width() / 3,
            self.app.desktopGeometry.height() / 2)
        )

    def markdownText(self):
        return self.textEditUser.toPlainText()

    def onEdited(self):
        if self.updateTimer.isActive():
            self.updateTimer.stop()

        self.updateTimer.start(self.updateTimeoutMs)

    def onTimerOut(self):
        textData = self.textEditUser.toPlainText()
        try:
            html = markitdown(textData)
            self.textEditMarkdown.setHtml(html)
        except Exception:
            pass


class AtomFeedsToolbarButton(QToolButton):
    subscribeResult = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(AtomFeedsToolbarButton, self).__init__(parent=parent)
        self.app = QApplication.instance()
        self.model = self.app.modelAtomFeeds
        self.model.root.tracker.unreadCountChanged.connect(
            self.unreadEntriesCountChanged)
        self.setIcon(getIcon('atom-feed.png'))
        self.subscribeResult.connect(self.onSubResult)

        self.setToolTip('Atom Feeds reader')

    def unreadEntriesCountChanged(self, count):
        self.setToolTip('Atom Feeds reader: {count} unread entries'.format(
            count=count))

    def onSubResult(self, url, result):
        if result == 1:
            messageBox('This Atom feed is already registered', title=url)
        elif result == 2:
            messageBox('Error while subscribing to Atom feed', title=url)
        elif result == 3:
            messageBox('Subscribe OK!', title=url)

    async def atomFeedSubscribe(self, url):
        from galacteek.dweb.atom import AtomFeedExistsError
        try:
            await self.app.sqliteDb.feeds.follow(url)
        except AtomFeedExistsError:
            self.subscribeResult.emit(url, 1)
        except Exception:
            self.subscribeResult.emit(url, 2)
        else:
            self.subscribeResult.emit(url, 3)


class PageSourceWidget(QTextBrowser):
    def __init__(self, parent):
        super(PageSourceWidget, self).__init__(parent)

        self.app = QApplication.instance()
        self.setAcceptRichText(True)
        self.setLineWrapMode(QTextEdit.WidgetWidth)

    async def showSource(self, sourceText):
        formatter = HtmlFormatter()
        cssDefs = formatter.get_style_defs()

        lexer = get_lexer_by_name('html')

        self.document().setPlainText('Loading ...')
        try:
            high = await self.app.loop.run_in_executor(
                self.app.executor, highlight,
                sourceText, lexer, formatter)

            self.document().setDefaultStyleSheet(cssDefs)
            self.document().setHtml(high)
        except:
            self.document().setPlainText('Could not load source')

        self.moveCursor(QTextCursor.Start)


class AnimatedButton(QPushButton):
    """
    Animated button.
    """

    def __init__(self, clip, ignoreFrameEvery=1, parent=None):
        super().__init__(parent)

        self.clip = clip
        self.clip.finished.connect(self.clip.start)
        self.clip.frameChanged.connect(self.onFrameChanged)
        self.ignoreFrameEvery = ignoreFrameEvery

    def startClip(self):
        if not self.clip.playing():
            self.clip.start()

    def onFrameChanged(self, fNum):
        if divmod(fNum, self.ignoreFrameEvery)[1] == 0:
            self.setIcon(self.clip.createIcon())


class AnimatedLabel(QLabel):
    """
    Animated label.
    """

    animationClicked = pyqtSignal()

    def __init__(self, clip, loop=True, parent=None):
        super().__init__(parent)

        self.clip = clip

        if self.clip.isValid():
            self.setMovie(self.clip)

        if loop:
            self.clip.finished.connect(self.clip.start)

    def mousePressEvent(self, event):
        self.animationClicked.emit()

    def startClip(self):
        if not self.clip.playing():
            self.clip.start()
