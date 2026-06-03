import time as TM
from datetime import datetime

from coords.zudui import *
from .futureBase import Base


class ZuDui(Base):
    def shenKun(self, select_index: int = 2, times: int = 100):
        """神困副本

        :param select_index: 副本的索引, 默认2, 神将罗汉山
        :param times: 攻打的次数, 默认1000次
        """

        role = self.config.get("role", "master")
        队伍ID = self.config.get("队伍ID", 2956253289)

        if select_index == 0:
            副本 = 激战东平府
        elif select_index == 1:
            副本 = 鏖战东昌府
        else:
            副本 = 神降罗汉山

        for i in range(1, times + 1):
            if role == "master":
                self.util.click(副本)
                TM.sleep(0.5)
                self.util.click(创建组队副本)
                TM.sleep(0.5)
                self.util.click(难度)
                TM.sleep(0.3)
                self.util.click(("困难", 463, 383))
                TM.sleep(0.5)
                self.util.click(私有组队)
                TM.sleep(0.5)
                self.util.click(创建)
                TM.sleep(0.5)
                self.util.click(人满自动开)
                TM.sleep(0.2)
                self.util.click(("空白位置", 650, 377))
                print(
                    f"master[{self.qq}]创建组队完毕, {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, 预计等待7分钟20秒"
                )
            else:
                TM.sleep(4)

                self.lock.acquire()  # 进行抢锁，抢到的线程才执行
                self.util.click(加入指定队伍)
                TM.sleep(0.5)

                self.util.type_content(输入队伍ID_输入框, 队伍ID)
                TM.sleep(0.5)

                self.util.click(加入队伍)
                TM.sleep(0.3)
                self.lock.release()  # 释放锁，其它线程可以执行了

            self.logger.info(f"神困副本当前已开: {i}次, 预计次数: {times}次")
            print(f"神困副本当前已开: {i}次, 预计次数: {times}次", end="\r")

            # 用于解决: 组队的人点击过快
            loop = i // 5
            TM.sleep(7 * 60 + 10 + loop * 20)

            self.util.click(通关成功_确定)
            TM.sleep(0.3)
            self.util.click(通关成功_确定)
            TM.sleep(0.3)

            self.util.click(副本通关奖励)
            TM.sleep(0.5)
            self.util.click(副本通关奖励)
            TM.sleep(0.5)

            self.util.click(消耗罗汉珠_确定)
            TM.sleep(0.5)
            self.util.click(消耗罗汉珠_确定)
            TM.sleep(0.5)
