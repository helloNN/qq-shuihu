from utils import Util
from contextlib import contextmanager
from coords.liehun import 一键猎魂, 一键合成
import time as TM


class Beibao:
    hwnd = None
    logger = None

    def __init__(self, logger, hwnd):
        self.logger = logger
        self.hwnd = hwnd

    def set_hwnd(self, hwnd: int):
        self.hwnd = hwnd

    def liehun(self, time=20):
        """
        猎魂

        参数:
        time: 猎魂次数, 默认20次
        """

        if self.hwnd is None:
            self.logger.error(f"使用猎魂功能前，请先设置窗口句柄")
            return

        self.logger.info(f"猎魂开始, 预计次数: {time}")
        startTime = TM.time()
        realTime = 0

        with self._liehun():
            times = (x for x in range(time))

            for i in times:
                Util.bg_click(
                    {
                        "hwnd": self.hwnd,
                        "x": 一键猎魂[1],
                        "y": 一键猎魂[2],
                        "logger": self.logger,
                    }
                )
                time.sleep(3)
                Util.bg_click(
                    {
                        "hwnd": self.hwnd,
                        "x": 一键合成[1],
                        "y": 一键合成[2],
                        "logger": self.logger,
                    }
                )
                realTime += 1
                time.sleep(1)

        self.logger.info(
            f"猎魂结束, 耗时: {TM.time() - startTime}, 实际次数: {realTime}"
        )

    @contextmanager
    def _liehun(self):
        """猎魂上下文管理器"""

        # 打开背包

        try:
            yield
        except Exception as e:
            self.logger.error(f"猎魂过程中出现错误: {str(e)}")

        # 关闭背包
