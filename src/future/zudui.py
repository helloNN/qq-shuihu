from contextlib import contextmanager
from coords.zudui import *
import time as TM
from utils.util import Util


class ZuDui:
    util: Util = None
    logger = None
    config = {}
    qq = ""

    def __init__(self, util, config, qq):
        self.util = util
        self.logger = util.logger
        self.config = config
        self.qq = qq

    def shenKun(self, order_num, times: int = 1000):
        """
        神困副本
        :param order_num
        :param times 攻打的次数, 默认1000次
        """

        role = self.config.get("role", "master")
        队伍ID = self.config.get("队伍ID", 2956253289)

        for i in range(1, times + 1):
            if role == "master":
                self.util.click(神降罗汉山)
                TM.sleep(0.5)
                self.util.click(创建组队副本)
                TM.sleep(0.5)
                self.util.click(难度)
                TM.sleep(0.2)
                self.util.click(("困难", 463, 383))
                TM.sleep(0.2)
                self.util.click(私有组队)
                TM.sleep(0.2)
                self.util.click(创建)
                TM.sleep(0.5)
                self.util.click(人满自动开)
            else:
                # 等待创建组队的创建完毕
                TM.sleep(3)

                self.util.click(加入指定队伍)
                TM.sleep(0.5 + order_num * 1.1)
                self.util.type_content(输入队伍ID_输入框, 队伍ID)
                TM.sleep(0.2)
                self.util.click(加入队伍)

            self.logger.info(f"神困副本当前已开: {i}次 | 预计次数: {times}次")
            print(
                f"神困副本当前已开: {i}次 | 预计次数: {times}次 | 等待7分钟", end="\r"
            )

            TM.sleep(7 * 60)
            self.util.click(通关成功_确定)
            TM.sleep(0.3)
            self.util.click(副本通关奖励)
            TM.sleep(0.5)
            self.util.click(消耗罗汉珠_确定)
            TM.sleep(0.5)
