from multiprocessing.synchronize import Lock, Event
from logging import Logger

from utils.util import Util


class Base:
    def __init__(self, hwnd: int, util: Util, config, qq, lock: Lock, event: Event):
        """
        功能模块基础类

        :param hwnd: 窗口句柄
        :param util: 工具类
        :param config: qq配置
        :param qq: qq号
        :param lock: 线程锁
        """
        self.hwnd = hwnd
        self.util: Util = util
        self.logger: Logger = util.logger

        self.config = config
        self.qq = qq
        self.lock = lock
        self.event = event
