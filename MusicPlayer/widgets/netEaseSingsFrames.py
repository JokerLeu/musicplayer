__author__ = 'cyrbuzz'
"""网易歌曲框架
不要单独运行。"""
from singsFrameBase import SingsFrameBase, SingsSearchResultFrameBase


# 一个Tab，网易云的全部歌单（singsFrameBase的歌单框架基类）
class NetEaseSingsArea(SingsFrameBase):
    """全部歌单。"""

    def __init__(self, parent=None):
        super(NetEaseSingsArea, self).__init__(parent)


# 网易云的搜素结果（singsFrameBase的搜索结果框架基类）
class NetEaseSearchResultFrame(SingsSearchResultFrameBase):

    def __init__(self, parent):
        super(NetEaseSearchResultFrame, self).__init__(parent)
