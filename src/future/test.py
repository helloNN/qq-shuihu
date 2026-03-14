from contextlib import contextmanager
import time as TM
from utils.util import Util


class Test:
    util: Util = None
    logger = None
    config = {}
    qq = ""

    def __init__(self, util, config, qq):
        self.util = util
        self.logger = util.logger
        self.config = config
        self.qq = qq

    def test_write(self, coord, content):
        """
        测试输入框输入内容
        :param coord: 普通坐标
        :param content 输入的内容
        """
        self.util.type_content(coord, content)
