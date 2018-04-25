"""本地音乐的界面，逻辑。"""
__author__ = 'cyrbuzz'

from base import (ScrollArea, QLabel, QFrame, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget,
                  QAbstractItemView)


# 本地音乐（滚动条区）
class NativeMusic(ScrollArea):
    """本地音乐类"""
    def __init__(self, parent):
        super(NativeMusic, self).__init__()
        self.parent = parent
        self.setObjectName('nativeMusic')  # 实例名称
        with open('QSS/nativeMusic.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())  # 设置页面样式

        self.mainLayout = QVBoxLayout(self)  # 生成主布局：QT垂直盒子布局

        self.setTopShow()
        self.musicTable()

    # 顶部布局。
    def setTopShow(self):
        self.showLabel = QLabel("本地音乐")  # 实例化本地音乐的左上角标签名
        
        self.spaceLine = QFrame(self)  # 实例化QT框架
        self.spaceLine.setObjectName("spaceLine")  # 线框名称
        self.spaceLine.setFrameShape(QFrame.HLine)  # 设置线框形状（横线）
        # self.spaceLine.setFrameShadow(QFrame.Raised)  # 设置线框阴影（凸起）
        self.spaceLine.setFrameShadow(QFrame.Plain)  # 设置线框阴影（平的）
        self.spaceLine.setLineWidth(2)  # 设置线的宽度

        self.selectButton = QPushButton("选择目录")  # 按钮
        self.selectButton.setObjectName('selectButton')  # 名字

        self.topShowLayout = QHBoxLayout()  # 水平盒子布局
        self.topShowLayout.addSpacing(20)  # 盒子左边加20空白
        self.topShowLayout.addWidget(self.showLabel)  # 添加左上角标签名
        self.topShowLayout.addWidget(self.selectButton)  # 添加线框
        self.topShowLayout.addStretch(1)  # 伸缩值???

        self.mainLayout.addLayout(self.topShowLayout)  # 主布局添加水平盒子布局
        self.mainLayout.addWidget(self.spaceLine)  # 主布局添加线框

    # 歌曲表格
    def musicTable(self):
        self.singsTable = QTableWidget()  # 实例化QT表格部件
        self.singsTable.setObjectName('singsTable')  # 名称
        self.singsTable.setMinimumWidth(self.width())  # 最小宽度为自身宽度
        self.singsTable.setColumnCount(3)  # 列数
        self.singsTable.setHorizontalHeaderLabels(['音乐标题', '歌手', '时长'])

        self.singsTable.setColumnWidth(0, self.width()/3*1.25)  # 列宽1
        self.singsTable.setColumnWidth(1, self.width()/3*1.25)  # 列宽2
        self.singsTable.setColumnWidth(2, self.width()/3*0.5)  # 列宽3
        self.singsTable.horizontalHeader().setStretchLastSection(True)  # 列头
        self.singsTable.verticalHeader().setVisible(False)  # 行头
        self.singsTable.setShowGrid(False)  # 网格可见性
        self.singsTable.setAlternatingRowColors(True)  # 交替显示行颜色

        self.singsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑触发
        self.singsTable.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中行

        self.mainLayout.addWidget(self.singsTable)  # 最终将部件在主布局中添加


# 无信息音乐
class EmptyMusic(object):

    def __init__(self):
        self.tag = EmptyMusicObject()
        self.tag.title = '未知名称'
        self.tag.artist = '未知歌手'

        self.info = EmptyMusicObject()
        self.info.time_secs = 0  # 时间为0秒


# 没有音频文件
class EmptyMusicObject(object):
    def __init__(self):
        pass

