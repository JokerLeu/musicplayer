# 下载页面布置类
__author__ = 'cyrbuzz'

from base import (ScrollArea, QLabel, QFrame, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget,
                  QAbstractItemView)


# 下载框架类（滚动区域）
class DownloadFrame(ScrollArea):

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setObjectName('downloadMusic')
        with open('QSS/downloadFrame.qss', 'r', encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.mainLayout = QVBoxLayout(self)

        self.setHeader()
        self.setMusicTable()

    # 设置头部信息方法
    def setHeader(self):
        # self.titleLabel = QLabel("我的下载")

        self.spaceLine = QFrame(self)
        self.spaceLine.setObjectName("spaceLine")
        self.spaceLine.setFrameShape(QFrame.HLine)
        self.spaceLine.setFrameShadow(QFrame.Plain)
        self.spaceLine.setLineWidth(2)
        
        self.currentStorageFolderLabel = QLabel("当前存储目录: ")
        
        self.currentStorageFolder = QLabel()

        self.selectButton = QPushButton("选择目录")
        self.selectButton.setObjectName('selectButton')

        self.topShowLayout = QHBoxLayout()
        self.topShowLayout.addSpacing(20)
        # self.topShowLayout.addWidget(self.titleLabel)
        self.topShowLayout.addWidget(self.currentStorageFolderLabel)
        self.topShowLayout.addWidget(self.currentStorageFolder)
        self.topShowLayout.addWidget(self.selectButton)
        self.topShowLayout.addStretch(1)

        self.mainLayout.addLayout(self.topShowLayout)
        self.mainLayout.addWidget(self.spaceLine)

    # 设置音乐列表方法
    def setMusicTable(self):
        self.singsTable = QTableWidget()  # 歌曲列表，实例化表格部件
        self.singsTable.setObjectName('singsTable')  # 名字
        self.singsTable.setMinimumWidth(self.width())  # 最小宽度
        self.singsTable.setColumnCount(3)  # 列
        self.singsTable.setHorizontalHeaderLabels(['音乐标题', '歌手', '时长'])  # 列头名称

        self.singsTable.setColumnWidth(0, self.width()/3*1.25)  # 宽度
        self.singsTable.setColumnWidth(1, self.width()/3*1.25)
        self.singsTable.setColumnWidth(2, self.width()/3*0.5)
        self.singsTable.horizontalHeader().setStretchLastSection(True)  # 表格宽度自适应调整，铺开
        self.singsTable.verticalHeader().setVisible(False)  # 数值头部显示
        self.singsTable.setShowGrid(False)  # 网格可见性
        self.singsTable.setAlternatingRowColors(True)  # 表格颜色交替

        self.singsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 编辑出发，否
        self.singsTable.setSelectionBehavior(QAbstractItemView.SelectRows)  # 被选择后的行为，选择整行

        self.mainLayout.addWidget(self.singsTable)  # 添加到主布局