"""
重新设计，主要用于熟悉设计模式。
多线程/漂亮界面的设计等。

以网易云音乐为模板。
# 基本没考虑网络的出错问题。
# 
"""

__author__ = 'cyrbuzz'

import os
import sys
import os.path

myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path = [os.path.join(myFolder, 'widgets'),
os.path.join(myFolder, 'networks'),
os.path.join(myFolder, 'features'),
os.path.join(myFolder, 'apis'),
os.path.join(myFolder, 'logger')
] + sys.path

os.chdir(myFolder)

import asyncio
import logging

# event loop
# https://github.com/harvimt/quamash
# an asyncio eventloop for PyQt.
from quamash import QEventLoop

# widgets
from base import (QApplication, cacheFolder, QDialog, QFrame, QHBoxLayout, HBoxLayout, QIcon, QLabel, QListWidget, QListWidgetItem,
                  QPushButton, PicLabel, QScrollArea, ScrollArea, Qt, QTabWidget, TableWidget, QVBoxLayout, VBoxLayout,
                  QWidget)
from player import PlayWidgets
from native import NativeMusic
from downloadFrame import DownloadFrame
from addition import SearchLineEdit
from systemTray import SystemTray
from loginFrames import LoginBox
from singsFrameBase import DetailSings
from netEaseSingsFrames import  NetEaseSingsArea, NetEaseSearchResultFrame
from xiamiSingsFrames import XiamiSingsArea, XiamiSearchResultFrame
from qqSingsFrames import QQSingsArea, QQSearchResultFrame

# features
from configMainFeatures import (ConfigWindow, ConfigHeader, ConfigNavigation, ConfigMainContent, ConfigSearchArea,
                                ConfigSystemTray, ConfigDetailSings)
from configNativeFeatures import ConfigNative
from configDownloadFrameFeatures import ConfigDownloadFrame
from configNeteaseFeatures import ConfigNetEase
from configXiamiFeatures import ConfigXiami
from configQQFeatures import ConfigQQ

# logger
import logger


logger.loggerConfig('logger/running_log.log')

# 覆盖原logger变量。
logger = logging.getLogger(__name__)

logger.info("当前图片缓存目录: {0}".format(os.path.join(os.getcwd(), cacheFolder)))


# 用于承载整个界面。所有窗口的父窗口，所有窗口都可以在父窗口里找到索引。
class Window(QWidget):
    """Window 承载整个界面。"""
    def __init__(self):
        super(Window, self).__init__()
        self.setObjectName('MainWindow')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('resource/format.ico'))  # 窗口图标
        self.setWindowTitle("Music")  # 窗口名称

        self.resize(1022, 670)  # 窗口大小

        self.header = Header(self)  # 初始化头部
        self.navigation = Navigation(self)  # 初始化导航栏
        self.playWidgets = PlayWidgets(self)  # 初始化播放部件
        self.detailSings = DetailSings(self)  # 初始化歌单详情页（类在singsFrameBase里）
        self.mainContent = MainContent(self)  # 初始化主窗口
        self.nativeMusic = NativeMusic(self)  # 初始化本地音乐
        self.downloadFrame = DownloadFrame(self)  # 初始化下载框架
        self.searchArea = SearchArea(self)  # 初始化搜索区

        self.mainContents = QTabWidget()
        self.mainContents.tabBar().setObjectName("mainTab")

        self.systemTray = SystemTray('resource/logo.png', self)  # 系统图标

        # 加载tab设置。
        self.setContents()
        # 添加各类网站的歌单。
        self.addAllPlaylist()
        # 设置布局小细线。
        self.setLines()
        # 设置布局。
        self.setLayouts()
        # 注册功能。
        self.configFeatures()

        with open('QSS/window.qss', 'r') as f:
            self.setStyleSheet(f.read())

    # 添加歌单列表
    def addAllPlaylist(self):
        self.indexNetEaseSings = NetEaseSingsArea(self.mainContent)  # 内部实例：网易云歌单（在主窗口）
        self.indexXiamiSings = XiamiSingsArea(self.mainContent)
        self.indexQQSings = QQSingsArea(self.mainContent)
        # self.indexQQSings1 = QQSingsArea(self.mainContent)
        self.mainContent.addTab(self.indexNetEaseSings, "网易云歌单")  # 创建标签
        self.mainContent.addTab(self.indexXiamiSings, "虾米歌单")
        self.mainContent.addTab(self.indexQQSings, "QQ歌单")
        # self.mainContent.addTab(self.indexQQSings1, "QQ歌单1")

    # 设置Tab界面布局。
    def setContents(self):
        """设置tab界面。"""
        # 将需要切换的窗口做成Tab，并隐藏tabBar，这样方便切换，并且可以做前进后退功能。
        
        self.mainContents.addTab(self.mainContent, '')  # 添加标签（主要内容）
        self.mainContents.addTab(self.detailSings, '')  # 添加标签（歌单详情页）
        self.mainContents.addTab(self.nativeMusic, '')  # 添加标签（本地音乐）
        self.mainContents.addTab(self.downloadFrame, '')  # 添加标签（下载）
        self.mainContents.addTab(self.searchArea, '')  # 添加标签（搜索）

        self.mainContents.setCurrentIndex(0)  # 设置默认标签（主页（在以上里选择））

    # 设置布局小细线。
    def setLines(self):
        """设置布局小细线。"""
        self.line1 = QFrame(self)  # 实例化线框
        self.line1.setObjectName("line1")  # 名称
        self.line1.setFrameShape(QFrame.HLine)  # 线框形状设置
        self.line1.setFrameShadow(QFrame.Plain)  # 线框阴影：平的
        self.line1.setLineWidth(2)  # 线框宽度

    # 设置布局
    def setLayouts(self):
        """设置布局"""
        self.mainLayout = QVBoxLayout()  # 主布局：实例化垂直盒子布局
        self.mainLayout.addWidget(self.header)  # 添加头部部件
        self.mainLayout.addWidget(self.line1)  # 一条横线
        
        self.contentLayout = QHBoxLayout()  # 内容布局：实例化水平盒子布局
        self.contentLayout.setStretch(0, 70)  # 设置伸展??
        self.contentLayout.setStretch(1, 570)
        
        self.contentLayout.addWidget(self.navigation)  # 添加左侧导航条
        self.contentLayout.addWidget(self.mainContents)  # 添加主内容页

        self.contentLayout.setSpacing(0)  # 设置内容布局与其他部件的间隔
        self.contentLayout.setContentsMargins(0, 0, 0, 0)  # 设置边框（左，上，右，下）

        self.mainLayout.addLayout(self.contentLayout)  # 主布局：添加内容布局
        self.mainLayout.addWidget(self.playWidgets)  # 主布局：添加部件播放器部件
        
        self.mainLayout.setStretch(0, 43)  # 设置伸展??
        self.mainLayout.setStretch(1, 0)
        self.mainLayout.setStretch(2, 576)
        self.mainLayout.setStretch(3, 50)

        self.mainLayout.setSpacing(0)  # 设置主布局与其他部件的间隔
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)  # 设置布局：主布局

    # 注册所有功能。
    def configFeatures(self):
        self.config = ConfigWindow(self)  # 实例化窗口配置
        self.header.config = ConfigHeader(self.header)  # 实例化头部配置
        self.downloadFrame.config = ConfigDownloadFrame(self.downloadFrame) # 实例化下载框架配置
        self.searchArea.config = ConfigSearchArea(self.searchArea)  # 实例化搜索区域配置
        self.navigation.config = ConfigNavigation(self.navigation)  # 实例化导航条区域配置
        self.nativeMusic.config = ConfigNative(self.nativeMusic)  # 实例化本地音乐配置
        self.mainContent.config = ConfigMainContent(self.mainContent)  # 实例化主内容区配置
        self.detailSings.config = ConfigDetailSings(self.detailSings)  # 实例化音乐详情区配置
        self.indexNetEaseSings.config = ConfigNetEase(self.indexNetEaseSings)  # 实例化网易云配置
        self.indexXiamiSings.config = ConfigXiami(self.indexXiamiSings)  # 实例化虾米配置
        self.indexQQSings.config = ConfigQQ(self.indexQQSings)  # 实例化QQ音乐配置
        self.systemTray.config = ConfigSystemTray(self.systemTray)  # 实例化系统托盘配置

        self.indexNetEaseSings.config.initThread()  # 网易云初始化线程
        self.indexXiamiSings.config.initThread()  # 初始化线程
        self.indexQQSings.config.initThread()  # 初始化线程

        # 当前耦合度过高。
        self.downloadFrame.config.getDownloadSignal()
        
        # move to center.
        screen = QApplication.desktop().availableGeometry()
        self.playWidgets.desktopLyric.resize(screen.width(), 50)
        self.playWidgets.desktopLyric.move(0, screen.height() - 100)

    # 关闭事件
    def closeEvent(self, event):
        # 主要是保存cookies.
        self.header.config.saveCookies()  # 头部保存缓存
        self.playWidgets.saveCookies()  # 播放器保存缓存
        self.downloadFrame.config.saveCookies()  # 下载保存缓存

        # 系统托盘需要先隐藏，否则退出后会残留在任务栏。
        self.systemTray.hide()  # 系统图标隐藏

    # 重调整尺寸事件
    def resizeEvent(self, event):
       self. playWidgets.currentMusic.move(0, self.height()-64-self.playWidgets.height())


# 标题栏，包括logo，搜索，登陆，最小化/关闭。
class Header(QFrame):

    def __init__(self, parent=None):
        """头部区域，包括图标/搜索/设置/登陆/最大/小化/关闭。"""

        super(Header, self).__init__()
        self.setObjectName('Header')  # 实例名称

        self.parent = parent

        self.loginBox = LoginBox(self)  # 实例化登录框

        with open('QSS/header.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())  # 样式表

        self.setButtons()  # 设置按钮。

        self.setLabels()   # 设置标签。

        self.setLineEdits()  # 设置输入框。

        self.setLines()  # 设置小细线装饰。

        self.setLayouts()  # 设置布局。

    # 布局。
    # 设置按钮方法
    def setButtons(self):
        """创建所有的按钮。"""

        # 关闭按钮
        self.closeButton = QPushButton('×', self)  # 创建关闭按钮
        self.closeButton.setObjectName("closeButton")  # 关闭按钮的名字
        self.closeButton.setMinimumSize(21, 17)  # 最小区域尺寸

        # 最小化按钮
        self.showminButton = QPushButton('_', self)
        self.showminButton.setObjectName("minButton")
        self.showminButton.setMinimumSize(21, 17)

        # 最大化按钮
        self.showmaxButton = QPushButton('□')
        self.showmaxButton.setObjectName("maxButton")
        self.showmaxButton.setMaximumSize(16, 16)

        # 登录按钮
        self.loginButton = QPushButton("未登录 ▼", self)
        self.loginButton.setObjectName("loginButton")

        # 向前按钮
        self.prevButton = QPushButton("<")
        self.prevButton.setObjectName("prevButton")
        self.prevButton.setMaximumSize(28, 22)
        self.prevButton.setMinimumSize(28, 22)

        # 向后按钮
        self.nextButton = QPushButton(">")
        self.nextButton.setObjectName("nextButton")
        self.nextButton.setMaximumSize(28, 22)
        self.nextButton.setMinimumSize(28, 22)

    # 设置标签方法
    def setLabels(self):
        """创建所需的所有标签。"""
        self.logoLabel = PicLabel(r'resource/format.png', 32, 32)  # 左上角logo

        self.descriptionLabel = QLabel(self)  # 左上角文字
        self.descriptionLabel.setText("<b>Music</b>")

        self.userPix = PicLabel(r'resource/no_music.png', 32, 32, r'resource/user_pic_mask.png')
        self.userPix.setMinimumSize(22, 22)
        self.userPix.setObjectName("userPix")

    # 设置搜索框方法
    def setLineEdits(self):
        """创建搜素框。"""
        self.searchLine = SearchLineEdit(self)
        self.searchLine.setPlaceholderText("搜索音乐, 歌手, 歌词, 用户")  # 代替文字

    # 设置装饰线方法
    def setLines(self):
        """设置装饰用小细线。"""
        self.line1 = QFrame(self)
        self.line1.setObjectName("line1")
        self.line1.setFrameShape(QFrame.VLine)
        self.line1.setFrameShadow(QFrame.Plain)
        self.line1.setMaximumSize(1, 25)

    # 设置布局
    def setLayouts(self):
        """设置布局。"""
        self.mainLayout = QHBoxLayout()  # 头部主布局：水平布局
        self.mainLayout.setSpacing(0)  # 设置部件间的间隔
        self.mainLayout.addWidget(self.logoLabel)  # 小部件：logo
        self.mainLayout.addWidget(self.descriptionLabel)  # 小部件：描述文字
        self.mainLayout.addSpacing(70)  # 间隔
        self.mainLayout.addWidget(self.prevButton)  # 向前按钮
        self.mainLayout.addWidget(self.nextButton)  # 向后按钮
        self.mainLayout.addSpacing(10)  # 间隔
        self.mainLayout.addWidget(self.searchLine)  # 搜索框
        self.mainLayout.addStretch(1)  # 伸展
        self.mainLayout.addWidget(self.userPix)  # 用户头像
        self.mainLayout.addSpacing(7)  # 间隔
        self.mainLayout.addWidget(self.loginButton)  # 登录按钮
        self.mainLayout.addSpacing(7)  # 间隔
        self.mainLayout.addWidget(self.line1)  # 细线
        self.mainLayout.addSpacing(30)  # 间隔
        self.mainLayout.addWidget(self.showminButton)  # 最小化按钮
        self.mainLayout.addWidget(self.showmaxButton)  # 最大化按钮
        self.mainLayout.addSpacing(3)  # 间隔
        self.mainLayout.addWidget(self.closeButton)  # 关闭按钮

        self.setLayout(self.mainLayout)  # 设置布局到主布局

    # 事件。
    # 鼠标点击事件
    """重写鼠标事件，实现窗口拖动。"""
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.m_drag = True
            self.parent.m_DragPosition = event.globalPos()-self.parent.pos()
            event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and Qt.LeftButton:
                self.parent.move(event.globalPos()-self.parent.m_DragPosition)
                event.accept()
        except AttributeError:
            pass

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.m_drag = False


# 导航栏类（QT滚动条区）
# 左侧的导航栏，包括发现音乐/歌单/本地音乐。
class Navigation(QScrollArea):
    def __init__(self, parent=None):
        """包括发现音乐，MV，我的音乐, 歌单等导航信息。"""
        super(Navigation, self).__init__(parent)
        self.parent = parent
        self.frame = QFrame()  # 初始化框架：QT框架
        self.setMaximumWidth(200)  # 设置最大宽度

        self.setWidget(self.frame)  # 设置部件（本框架）
        self.setWidgetResizable(True)  # 设置部件尺寸可调型
        self.frame.setMinimumWidth(200)  # 设置最小宽度

        # 定义3个事件函数，方便扩展。
        self.navigationListFunction = self.none
        self.nativeListFunction = self.none
        self.singsFunction = self.none

        with open('QSS/navigation.qss', 'r') as f:  # 打开样式表
            style = f.read()  # 读取
            self.setStyleSheet(style)  # 设置
            self.frame.setStyleSheet(style)  # 框架设置

        # 包括显示信息： 推荐 我的音乐 歌单。
        self.setLabels()  # 初始化设置标签

        # 包括详细的内容：发现音乐，FM，MV等。
        self.setListViews()  # 初始化设置列表视图

        self.setLayouts()  # 初始化设置布局

    # 布局。
    # 设置标签
    def setLabels(self):
        """定义所有的标签。"""
        self.recommendLabel = QLabel(" 推荐")
        self.recommendLabel.setObjectName("recommendLabel")
        self.recommendLabel.setMaximumHeight(27)

        self.myMusic = QLabel(" 我的音乐")
        self.myMusic.setObjectName("myMusic")
        self.myMusic.setMaximumHeight(27)
        # self.myMusic.setMaximumHeight(54)

        self.singsListLabel = QLabel(" 收藏与创建的歌单")
        self.singsListLabel.setObjectName("singsListLabel")
        self.singsListLabel.setMaximumHeight(27)

    # 设置表视图
    def setListViews(self):
        """定义承载功能的ListView"""
        self.navigationList = QListWidget()  # 实例化一个列表控件到导航列表
        self.navigationList.setMaximumHeight(110)  # 最大列表高度
        self.navigationList.setObjectName("navigationList")  # 名字
        self.navigationList.addItem(QListWidgetItem(QIcon('resource/music.png'), " 发现音乐"))
        self.navigationList.addItem(QListWidgetItem(QIcon('resource/signal.png'), " 私人FM"))
        self.navigationList.addItem(QListWidgetItem(QIcon('resource/movie.png'), " MV"))
        self.navigationList.setCurrentRow(0)  # 设置列表第一项为默认

        self.nativeList = QListWidget()  # 实例化一个列表控件到本地列表
        self.nativeList.setObjectName("nativeList")  # 名字
        self.nativeList.setMaximumHeight(80)  # 最大列表高度
        self.nativeList.addItem(QListWidgetItem(QIcon('resource/notes.png'), " 本地音乐"))
        self.nativeList.addItem(QListWidgetItem(QIcon('resource/download_icon.png'), " 我的下载"))

    # 设置导航栏布局
    def setLayouts(self):
        """定义布局。"""
        self.mainLayout = VBoxLayout(self.frame)  # 建立垂直布局
        self.mainLayout.addSpacing(10)  # 间隔
        self.mainLayout.addWidget(self.recommendLabel)  # 推荐标签
        self.mainLayout.addSpacing(3)  # 间隔
        self.mainLayout.addWidget(self.navigationList)  # 导航列表
        self.mainLayout.addSpacing(1)  # 间隔
        
        self.mainLayout.addWidget(self.myMusic)  # 我的音乐标签
        self.mainLayout.addSpacing(3)  # 间隔
        self.mainLayout.addWidget(self.nativeList)  # 本地列表
        self.mainLayout.addSpacing(1)  # 间隔

        self.mainLayout.addWidget(self.singsListLabel)  # 收藏与创建的歌单标签
        self.mainLayout.addSpacing(1)  # 间隔

        self.mainLayout.addStretch(1)  # 间隔

        self.setContentsMargins(0, 0, 0, 0)  # 整体边缘

    # just a test.
    def setSingsList(self):

        pass

    # 功能。
    def none(self):
        # 没有用的空函数。
        pass


# 主要内容区，包括最新的歌单。
class MainContent(ScrollArea):
    # 定义一个滑到了最低部的信号。
    # 方便子控件得知已经滑到了最底部，要做些加载的动作。

    def __init__(self, parent=None):
        """主内容区，包括推荐歌单等。"""
        super(MainContent, self).__init__()
        self.parent = parent
        self.setObjectName("MainContent")

        # 连接导航栏的按钮。
        # self.parent.navigation.navigationListFunction = self.navigationListFunction
        with open("QSS/mainContent.qss", 'r', encoding='utf-8') as f:  # 打开样式表
            self.style = f.read()  # 读取
            self.setStyleSheet(self.style)  # 设置样式表

        self.tab = QTabWidget()  # 实例化QT表格部件
        self.tab.setObjectName("contentsTab")  # 名字

        self.mainLayout = QVBoxLayout()  # 主内容布局：垂直布局
        self.mainLayout.setSpacing(0)  # 间隔
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # 边缘距离(左，上，右，下)
        self.mainLayout.addWidget(self.tab)  # 添加部件

        self.frame.setLayout(self.mainLayout)  # 框架，设置布局：主布局

    def addTab(self, widget, name=''):  # 添加标签（部件实例，名称）
        """添加标签"""
        self.tab.addTab(widget, name)


# 搜索后的结果显示页。
class SearchArea(ScrollArea):

    def __init__(self, parent=None):
        super(SearchArea, self).__init__(self)
        self.parent = parent
        self.setObjectName("searchArea")  # 实例名称
        with open('QSS/searchArea.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        self.mainLayout = QVBoxLayout(self.frame)  # 主布局：QT竖直布局：框架

        self.titleLabel = QLabel(self.frame)  # 标题标签：QT标签:框架

        # 搜索结果的tab。
        self.contentsTab = QTabWidget(self.frame)  # 内容表格：QT表格：框架

        # 加入布局。
        self.mainLayout.addWidget(self.titleLabel)  # 主布局，添加部件：标题标签
        self.mainLayout.addWidget(self.contentsTab)  # 主布局，添加部件：内容表格

        self.setSingsFrame()  # 搜索结果布局

    # 搜索结果布局。
    def setSingsFrame(self):
        # 单曲界面。
        self.neteaseSearchFrame = NetEaseSearchResultFrame(self)
        self.contentsTab.addTab(self.neteaseSearchFrame, "网易云")

        self.xiamiSearchFrame = XiamiSearchResultFrame(self)
        self.contentsTab.addTab(self.xiamiSearchFrame, "虾米")

        self.qqSearchFrame = QQSearchResultFrame(self)
        self.contentsTab.addTab(self.qqSearchFrame, 'QQ')

    # 搜索后的窗口文字。
    def setText(self, text):
        self.text = text
        self.titleLabel.setText("搜索<font color='#23518F'>“{0}”</font><br>".format(self.text))


def start():
    app = QApplication(sys.argv)  # 启动应用

    # 将Qt事件循环写到asyncio事件循环里。
    # QEventLoop不是Qt原生事件循环，
    # 是被asyncio重写的事件循环。
    eventLoop = QEventLoop(app)  # QT事件循环（应用）
    asyncio.set_event_loop(eventLoop)  # 异步，设置事件循环（QT事件循环）

    try:
        main = Window()

        main.show()
        # 当前音乐的显示信息。
        # 因为需要布局之后重新绘制的宽高。
        # 这个宽高会在show之后才会改变。
        # 需要获取宽，高并嵌入到父窗口里。
        main.playWidgets.currentMusic.resize(main.navigation.width(), 64)
        
        with eventLoop:
            eventLoop.run_forever()

        sys.exit(0)
    except:
        logger.error("got some error", exc_info=True)


if __name__ == '__main__':
    start()    
