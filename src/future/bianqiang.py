from contextlib import contextmanager
from coords.liehun import 一键猎魂, 一键合成
import time as TM
from utils.util import Util


class Bianqiang:
    util: Util = None
    logger = None
    config = {}
    qq = ""

    def __init__(self, util, config, qq):
        self.util = util
        self.logger = util.logger
        self.config = config
        self.qq = qq

    def liehun(self, time=20):
        """
        猎魂

        参数:
        time: 猎魂次数, 默认20次
        """
        self.logger.info(f"猎魂开始, 预计次数: {time}")
        print(f"猎魂开始, 预计次数: {time}")
        startTime = TM.time()
        realTime = 0

        with self._liehun():
            times = (x for x in range(time))

            for i in times:
                self.util.click(一键猎魂)
                TM.sleep(2)
                self.util.click(一键合成)
                realTime += 1
                print(f"当前已猎魂: {realTime} 次", end="\r")
                TM.sleep(1)

        self.logger.info(
            f"猎魂结束, 耗时: {round(TM.time() - startTime, 2)}s, 实际次数: {realTime}"
        )
        print(
            f"猎魂结束, 耗时: {round(TM.time() - startTime, 2)}s, 实际次数: {realTime}"
        )

    @contextmanager
    def _liehun(self):
        """猎魂上下文管理器"""

        # 打开背包

        try:
            self.logger.info("打开背包")
            yield
        except Exception as e:
            self.logger.error(f"猎魂过程中出现错误: {str(e)}")

        # 关闭背包
        self.logger.info("关闭背包")
