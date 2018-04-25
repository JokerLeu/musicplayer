from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
"""处理时间，处理成00:00:00的格式。"""


# 个位数x变成两位数0x
def deal_time(x):
    x = str(x)
    if len(x) == 1:
        x = '0' + x

    return x


# 秒转换成分秒 mm:ss
def itv2time(iItv):
    iItv = int(iItv)  # 字符串转换成int

    # 地板除求小时整数。
    h = iItv//3600  # 小时
    # 求余数。
    h_remainder = iItv % 3600

    # 地板除求分钟整数。
    m = h_remainder // 60  # 分钟
    # 求余数 为秒。
    s = h_remainder % 60  # 秒

    return ":".join(map(deal_time,(m,s)))  # 返回mm:ss


# 搜索框（QT单行输入框）
class SearchLineEdit(QLineEdit):
    """创建一个可自定义图片的输入框。"""
    def __init__(self, parent=None):
        super(SearchLineEdit, self).__init__()
        self.setObjectName("SearchLine")  # 名称
        self.parent = parent
        self.setMinimumSize(218, 20)  # 最小尺寸
        with open('QSS/searchLine.qss', 'r') as f:  # 打开样式文件
            self.setStyleSheet(f.read())  # 设置样式

        self.button = QPushButton(self)  # 实例化QT按钮
        self.button.setMaximumSize(13, 13)  # 最大尺寸
        self.button.setCursor(QCursor(Qt.PointingHandCursor))

        self.setTextMargins(3, 0, 19, 0)  # 文字边缘（上左下右）

        self.spaceItem = QSpacerItem(150, 10, QSizePolicy.Expanding)  # QT尺寸策略，扩展

        self.mainLayout = QHBoxLayout()  # 主布局实例化水平布局
        self.mainLayout.addSpacerItem(self.spaceItem)  # 添加间隔项，将输入和按钮水平排列
        # self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.button)  # 添加按钮
        self.mainLayout.addSpacing(10)  # 添加间距
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # 边缘
        self.setLayout(self.mainLayout)  # 设置布局：主布局

    # 设置按钮槽
    def setButtonSlot(self, funcName):
        self.button.clicked.connect(funcName)  # 触发槽 函数



if __name__ == '__main__':
    # import sys

    # app = QApplication(sys.argv)

    # main = SearchLineEdit()

    # main.show()

    # sys.exit(app.exec_())
    print(itv2time(12.34))