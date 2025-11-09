from contextlib import contextmanager
from coords.other import *
import time as TM
from utils.util import Util


class Other:
    util: Util = None
    logger = None
    config = {}
    qq = ""

    def __init__(self, util, config, qq):
        self.util = util
        self.logger = util.logger
        self.config = config
        self.qq = qq

    def xiShuXing(self, time=30):
        """
        洗属性【一次洗100次】

        参数:\n
        time: 次数, 默认 30次\n
        """
        self.logger.info(f"洗属性开始, 预计次数: {time}")
        startTime = TM.time()
        realTime = 0
        times = (x for x in range(time))

        printStr = f"{self.qq} | " if self.qq else ""

        for i in times:
            self.util.click(次数_洗属性)
            TM.sleep(1)

            self.util.click(确定_洗属性)
            realTime += 1
            print(f"{printStr}当前已洗属性: {realTime} 次 | 预计次数: {time}", end="\r")
            TM.sleep(1)

        result = f"洗属性结束, 耗时: {round(TM.time() - startTime, 2)}s, 实际次数: {realTime}"
        self.logger.info(result)
        print(result)

    def xiShuXing2(self, time=300):
        """
        洗属性【一次一次洗】

        参数:\n
        time: 次数, 默认 300次\n
        """
        self.logger.info(f"洗属性开始2, 预计次数: {time}")
        startTime = TM.time()
        realTime = 0
        times = (x for x in range(time))

        printStr = f"{self.qq} | " if self.qq else ""

        for i in times:
            self.util.click(确定_洗属性)
            realTime += 1
            print(f"{printStr}当前已洗属性: {realTime} 次 | 预计次数: {time}", end="\r")
            TM.sleep(30 if realTime % 30 == 0 else 1)

        result = f"洗属性2结束, 耗时: {round(TM.time() - startTime, 2)}s, 实际次数: {realTime}"
        self.logger.info(result)
        print(result)
