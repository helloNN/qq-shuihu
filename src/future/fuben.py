from contextlib import contextmanager
from coords.zhengzhan import *
import time as TM
from utils.util import Util


class Fuben:
    util: Util = None
    logger = None
    config = {}
    qq = ""

    def __init__(self, util, config, qq):
        self.util = util
        self.logger = util.logger
        self.config = config
        self.qq = qq

    def zhengzhan(self, time=5):
        """
        征战

        参数:
        time: 征战次数, 默认5次
        """
        self.logger.info(f"征战开始, 预计次数: {time}")
        print(f"征战开始, 预计次数: {time}")
        startTime = TM.time()
        realTime = 0

        with self._zhengzhan():
            times = (x for x in range(time))
            self.util.click(攻击)
            TM.sleep(2)

            for i in times:
                self.util.click(战斗结束)
                TM.sleep(2.5)

                self.util.click(再战)
                realTime += 1
                print(f"当前已征战: {realTime} 次", end="\r")
                TM.sleep(1)

        self.logger.info(
            f"征战结束, 耗时: {round(TM.time() - startTime, 2)}s, 实际次数: {realTime}"
        )
        print(
            f"征战结束, 耗时: {round(TM.time() - startTime, 2)}s, 实际次数: {realTime}"
        )

    @contextmanager
    def _zhengzhan(self):
        """征战上下文管理器"""

        # 打开征战

        try:
            self.logger.info("打开征战")
            yield
        except Exception as e:
            self.logger.error(f"征战过程中出现错误: {str(e)}")

        # 关闭征战
        self.logger.info("关闭征战")
