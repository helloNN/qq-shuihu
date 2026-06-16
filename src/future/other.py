from coords.other import *
import time as TM
from .futureBase import Base


class Other(Base):
    def xiShuXing100(self, time=30):
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

    def xiShuXing1(self, time=3000):
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
            TM.sleep(1)

        result = f"洗属性2结束, 耗时: {round(TM.time() - startTime, 2)}s, 实际次数: {realTime}"
        self.logger.info(result)
        print(result)

    def jiShi(self, done=True):
        """
        集市
        """
        start_time = TM.time()

        集市 = self.config.get("集市")
        城市 = 集市.get("城市")
        商队 = 集市.get("商队")
        商品顺序 = 集市.get("商品顺序")
        stop = 集市.get("stop")
        if stop:
            return

        city = {1: "汴京", 2: "洛阳", 3: "扬州", 4: "苏州", 5: "临安", 6: "泉州"}

        self.logger.info(f"在{city[城市]}用第{商队}商队进行跑商第{商品顺序}个")

        self.util.click((f"{city[城市]}", 200 + 103 * (城市 - 1), 100))
        TM.sleep(0.2)
        self.util.click((f"商品{商品顺序}", 470, 230 + 40 * (商品顺序 - 1)))
        TM.sleep(0.15)
        self.util.click((f"商队{商队}", 270 + 190 * (商队 - 1), 170))
        TM.sleep(0.1)
        self.util.click((f"货品数量最大", 688, 265))

        if done:
            TM.sleep(0.1)
            self.util.click((f"开始跑商", 500, 415))

        print(
            f"{self.qq}在{city[城市]}用第{商队}商队进行跑商第{商品顺序}个, 耗时:{round(TM.time() - start_time, 2)}s"
        )

    def jingJiChang(self, time=13):
        """竞技场

        :param time: 攻打次数
        """
        for ii in range(time):
            self.util.click(立即开战)
            TM.sleep(7)

            self.util.click(战斗结束)
            TM.sleep(0.2)
            self.util.click(战斗结束)
            TM.sleep(3)

            self.util.click(关闭)
            TM.sleep(1)

            print(f"{self.qq} | 已攻打: {ii+1} 次, 预计要攻打: {time}次", end="\r")

    def youShanXunBao(self, time=100):
        """游山寻宝

        :param time: 游山次数, 默认100次
        """

        self.util.click(跳过动画)
        TM.sleep(0.3)

        for ii in range(time):
            self.util.click(徒步游山)
            TM.sleep(0.5)

            self.util.click(跳过动画)
            TM.sleep(0.3)

            print(f"{self.qq} | 已攻打: {ii+1} 次, | 预计要攻打: {time}次", end="\r")
