from contextlib import contextmanager
from coords.juyi import *
import time as TM
from utils.util import Util


class Zhanzheng:
    util: Util = None
    logger = None
    config = {}

    def __init__(self, util, config):
        self.util = util
        self.logger = util.logger
        self.config = config

    def juyi(self, time=5):
        """
        聚义

        参数:
        time: 聚义次数, 默认5次
        """
        self.logger.info(f"聚义开始, 预计次数: {time}")
        print(f"聚义开始, 预计次数: {time}")
        startTime = TM.time()
        realTime = 0

        option = self.config.get("聚义", {})
        position = option.get("position", [])
        count = option.get("time", time)

        if len(position) != 2:
            self.logger.error("聚义坐标配置错误, 请检查配置文件")
            return

        position = ("聚义攻打位置", *self._calculate_juyi_position(position))
        print("option:", option)
        print("position:", position)

        with self._juyi():
            times = (x for x in range(count))

            for i in times:
                self.util.click(position)
                TM.sleep(1.5)
                self.util.click(掠夺)
                TM.sleep(1.5)
                self.util.click(确定)
                TM.sleep(4)
                self.util.click(战斗结束)
                TM.sleep(3)
                self.util.click(关闭)
                TM.sleep(2)

                realTime += 1
                print(f"当前已聚义: {realTime} 次", end="\r")

        self.logger.info(
            f"聚义结束, 耗时: {round(TM.time() - startTime, 2)}s, 实际次数: {realTime}"
        )
        print(
            f"聚义结束, 耗时: {round(TM.time() - startTime, 2)}s, 实际次数: {realTime}"
        )

    @contextmanager
    def _juyi(self):
        """聚义上下文管理器"""

        # 打开聚义

        try:
            self.logger.info("打开聚义")
            yield
        except Exception as e:
            self.logger.error(f"聚义过程中出现错误: {str(e)}")

        # 关闭聚义
        self.logger.info("关闭聚义")

    def _calculate_juyi_position(self, arr):
        """计算聚义位置"""
        [x, y] = arr
        y = y - 1

        diff = 254 - 133
        if x == 1:
            # 254-133=121
            position = (133 + diff * y, 157)
        elif x == 2:
            # 214-94=120
            position = (93 + diff * y, 295)
        else:
            position = (133 + diff * y, 440)

        return position
