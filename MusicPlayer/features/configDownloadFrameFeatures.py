__author__ = 'cyrbuzz'

import os
import re
import glob
import pickle
import os.path
import logging
try:
    import eyed3
except ImportError:
    print('eyed3没有成功加载或安装，当再次打开时下载的音乐会加载不到！')

from apiRequestsBase import HttpRequest
from asyncBase import aAsync, toTask
from base import QFileDialog, QObject, QTableWidgetItem, checkFolder
from addition import itv2time

import logger

logger = logging.getLogger(__name__)

myRequests = HttpRequest()  # 实例化HTTP请求


# 获取全部文件方法，返回结果列表
def getAllFolder(topFolder):
    result = []  # 定义结果列表

    # 查找文件方法
    def findFolder(topFolder):
        folders = [os.path.join(topFolder, i) for i in os.listdir(topFolder) if not os.path.isfile(os.path.join(topFolder, i))]
        if not folders:
            return 
        else:
            result.extend(folders)
            for i in folders:
                findFolder(i)
    # 执行查找文件
    findFolder(topFolder)

    return result


# 覆盖特殊符号方法
def replace_forbidden_sym(string):

    return re.sub(r'[\\/:*?"<>|]{1}', ' ', string)

# 配置下载框架类
class ConfigDownloadFrame(QObject):
    myDownloadFrameCookiesFolder = 'cookies/downloadInfo/downloadFolder.cks'  # 下载框架缓存
    allCookiesFolder = [myDownloadFrameCookiesFolder]  # 定义所有缓存文件列表

    def __init__(self, downloadFrame):
        super(ConfigDownloadFrame, self).__init__()
        self.downloadFrame = downloadFrame
        self.showTable = self.downloadFrame.singsTable  # 显示的表格：歌曲列表

        self.musicList = []  # 音乐列表
        self.folder = []  # 文件夹列表
        self.myDownloadFolder = os.path.join(os.getcwd(), 'downloads')  # 默认下载路径

        self._setDownloadFolder(self.myDownloadFolder)  # 设置下载路径

        self.bindConnect()  # 绑定连接

        self.loadCookies()

    # 绑定连接方法
    def bindConnect(self):
        self.downloadFrame.selectButton.clicked.connect(self.selectFolder)  # 下载框架，选按钮，点击，连接（选择文件方法）
        self.downloadFrame.singsTable.itemDoubleClicked.connect(self.itemDoubleClickedEvent)  # 下载框架，歌曲列表，单项双击，连接（单项双击事件）

    def getDownloadSignal(self):
        #
        window = self.downloadFrame.parent
        try:
            window.searchArea.config.download.connect(self.downloadSong)
            window.detailSings.config.download.connect(self.downloadSong)
        except Exception as e:
            logger.error("下载时遇到未知错误", exc_info=True)


    def _setDownloadFolder(self, folderName):
        logger.info("下载目标变更{}".format(folderName))
        self.fromPathLoadSong(folderName)
        self.myDownloadFolder = folderName
        self.downloadFrame.currentStorageFolder.setText(folderName)

    @toTask
    def downloadSong(self, musicInfo):
        logger.info("正在下载的音乐的信息: {}".format(musicInfo))

        url = musicInfo.get('url')
        allMusicName = re.search(r'.*\.[a-zA-Z0-9]+', url[url.rfind('/')+1:]).group(0)  # 歌曲链接
        if allMusicName:  # 存在歌曲链接
            musicSuffix = allMusicName[allMusicName.rfind('.')+1:]  # 后缀
            musicName = '{name}.{suf}'.format(name=musicInfo.get('name') + ' - ' + musicInfo.get('author'), suf=musicSuffix)  # 重命名成name -  author.suf
        else:
            # TODO MD5。
            musicName = "random_name.mp3"

        musicName = replace_forbidden_sym(musicName)  # 返回去掉特殊符号的歌曲名

        self.downloadFrame.parent.systemTray.showMessage("~~~", '{musicName} 加入下载队列'.format(musicName=musicName))
        # TODO
        # Streaming.
        future = aAsync(myRequests.httpRequest, url, 'GET')  # 一次异步（http请求，链接，方法）
        data = yield from future

        localPath = '{myDownloadFolder}/{musicName}'.format(myDownloadFolder=self.myDownloadFolder, musicName=musicName)
        with open(localPath, 'wb') as f:
            f.write(data.content)

        musicInfo['url'] = localPath

        # 从托盘栏给出提示。
        self.downloadFrame.parent.systemTray.showMessage("~~~", '{musicName} 下载完成'.format(musicName=musicName))
        # 将音乐信息加到musicList中。
        self.musicList.append(musicInfo)  # 添加音乐到列表
        self.updateDownloadShowTable(musicInfo)  # 更新下载列表

    # 更新下载列表方法
    def updateDownloadShowTable(self, musicInfo):
        showInfo = [musicInfo.get("name"), musicInfo.get("author"), musicInfo.get("time")]  # 解析信息到列表
        # 这里写"我的下载"的实例对象。
        # 首先获取出当前总共多少行。
        rowCount = self.showTable.rowCount()  # 行数
        self.showTable.setRowCount(rowCount+1)  # 显示的行数：总数+1
        #  然后直接添加过去就好啦。
        for i in range(3):  # 轮询3项
            self.showTable.setItem(rowCount, i, QTableWidgetItem(showInfo[i]))  # 设置项（行，列，值）

    # 从路径加载音乐的方法
    def fromPathLoadSong(self, selectFolder):
        if not os.path.isdir(selectFolder):  # 如果没有此路径则：
            os.mkdir(selectFolder)  # 创建路径
            return 
        mediaFiles = glob.glob(selectFolder+'/*.mp3')  # 此目录下所有mp3文件
        allFolder = getAllFolder(selectFolder)  # 此目录下所有文件夹列表
        for i in allFolder:  # 枚举所有文件夹
            mediaFiles.extend(glob.glob(i+'/*.mp3'))  # 添加mp3到文件列表

        length = len(mediaFiles)  # 长度为mp3文件个数
        
        self.downloadFrame.singsTable.clearContents()  # 下载框架，歌曲列表，清空内容
        self.downloadFrame.singsTable.setRowCount(length)  # 下载框架，歌曲列表，设置行数（从列表长度获取）
        self.musicList = []  # 创建音乐列表
        
        for i in enumerate(mediaFiles):  # 枚举搜索到的音乐列表
            music = eyed3.load(i[1])  # eyed3加载音乐文件

            if not music:  # 如果列表里没有音乐
                self.singsTable.removeRow(i[0])  #
                continue

            try:
                name = music.tag.title  # 解析歌曲名
                author = music.tag.artist  # 解析作者

                if not name:  # 无歌曲名
                    filePath = i[1].replace(selectFolder, '')  # 文件路径替换成空
                    name = filePath[1:][:-4]  # 歌曲名=去掉第一位，去掉后缀
                if not author:  # 无作者
                    author = ''  # 作者为空
            except:
                try:
                    # TODO
                    # if more folders exist.
                    filePath = i[1].replace(selectFolder, '')
                    name = filePath[1:][:-4]
                except Exception as e:
                    name = i[1]
                    author = ''
            try:
                time = itv2time(music.info.time_secs)  # 解析时长
            except:
                time = '00:00'

            # 音乐列表字典
            self.musicList.append({'name': name,'author': author, 'time': time, 'url': i[1], 'music_img': 'None'})
            #
            self.downloadFrame.singsTable.setItem(i[0], 0, QTableWidgetItem(name))  # 下载框架，歌曲表格，设置项（歌曲名）
            self.downloadFrame.singsTable.setItem(i[0], 1, QTableWidgetItem(author))  # （作者）
            self.downloadFrame.singsTable.setItem(i[0], 2, QTableWidgetItem(time))  # （时长）


    # 选择一个文件夹方法
    def selectFolder(self):
        folder = QFileDialog()  # 文件夹实例化QT文件夹对话
        selectFolder = folder.getExistingDirectory()  # 选择文件夹，获取现有目录
        if not selectFolder:
            pass
        else:
            self.folder.append(selectFolder)  # 文件夹列表，添加已选择的文件夹
            self._setDownloadFolder(selectFolder)  # 设置下载文件夹
            self.fromPathLoadSong(selectFolder)  # 从路径加载音乐

    # 保存缓存文件@检查文件（所有缓存文件列表）
    @checkFolder(allCookiesFolder)
    def saveCookies(self):
        with open(self.myDownloadFrameCookiesFolder, 'wb') as f:
            pickle.dump(self.myDownloadFolder, f)

    # 加载缓存文件@检查文件（所有缓存文件列表）
    @checkFolder(allCookiesFolder)
    def loadCookies(self):
        with open(self.myDownloadFrameCookiesFolder, 'rb') as f:
            self.myDownloadFolder = pickle.load(f)

        self._setDownloadFolder(self.myDownloadFolder)

    # 双击事件处理方法
    def itemDoubleClickedEvent(self):
        currentRow = self.downloadFrame.singsTable.currentRow()  # 特定行数据
        data = self.musicList[currentRow]  # 行中的数据列表

        self.downloadFrame.parent.playWidgets.setPlayerAndPlayList(data)  # 设置播放列表，播放列表音乐
