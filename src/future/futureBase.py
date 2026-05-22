from multiprocessing.synchronize import Lock
from logging import Logger

from utils.util import Util


class Base:
    def __init__(self, util: Util, config, qq, lock: Lock):
        """
        功能模块基础类

        :param util: 工具类
        :param config: qq配置
        :param qq: qq号
        :param lock: 线程锁
        """
        self.util: Util = util
        self.logger: Logger = util.logger

        self.config = config
        self.qq = qq
        self.lock = lock
