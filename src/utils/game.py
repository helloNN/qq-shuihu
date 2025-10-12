import logging
import json
import os
from .util import Util
from future import Bianqiang, Fuben, Zhanzheng

logging.basicConfig(
    filename="logs/game.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)


class Game:
    """游戏管理类"""

    hwnd = None
    qq = ""
    logger = None
    coordDiff = (0, 0)  # 位置偏移
    util = None
    Bianqiang = None
    config = {}

    def __init__(self, hwnd: int = None, qq=""):
        """
        hwnd: 窗口句柄
        """
        self.hwnd = hwnd
        self.qq = qq
        self.logger = logging.getLogger(f"Game-{self.qq or __name__}")
        if qq:
            # 多任务则自定义日志
            self._cutomLogger()
        self.load_config()

    def _cutomLogger(self):
        """自定义日志"""
        log_filename = f"logs/{self.qq}.log"
        handler_exists = any(
            isinstance(h, logging.FileHandler) and h.baseFilename.endswith(log_filename)
            for h in self.logger.handlers
        )

        if not handler_exists:
            file_handler = logging.FileHandler(log_filename, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.propagate = False  # 不向上传播到根日志器

        self.logger.info(f"{self.qq} | 日志游戏实例初始化")

    def _mountFuture(self):
        util = Util(self.hwnd, self.coordDiff, self.logger)
        self.util = util

        # 挂载功能
        self.Bianqiang = Bianqiang(util, self.config.get("变强", {}), self.qq)
        self.Fuben = Fuben(util, self.config.get("副本", {}), self.qq)
        self.Zhanzheng = Zhanzheng(util, self.config.get("战争", {}), self.qq)

    def set_hwnd(self, hwnd: int):
        """设置窗口句柄"""
        self.hwnd = hwnd

    def count_position(self, app):
        """计算窗口位置，并挂载功能"""
        print(f"{self.qq + ':' if self.qq else ''}计算窗口位置")

        mainWindow = app.MainWindow
        mainWindowRect = mainWindow.rectangle()
        self.logger.info(f"mainWindow窗口: {mainWindowRect}")

        # 联系官方，下面那块区域
        contactArea = mainWindow.child_window(
            auto_id="windowsFormsHost", control_type="Pane"
        )
        contactAreaRect = contactArea.rectangle()
        self.logger.info(f"联系官方窗口: {contactAreaRect}")

        flashArea = mainWindow["Custom4"]
        flashAreaRect = flashArea.rectangle()
        self.logger.info(
            f"flash窗口: {flashAreaRect} | width:{flashAreaRect.right - flashAreaRect.left}、height:{flashAreaRect.bottom - flashAreaRect.top}"
        )

        self.coordDiff = (
            flashAreaRect.left - contactAreaRect.left,
            flashAreaRect.top - contactAreaRect.top,
        )

        self.logger.info(f"flash窗口到联系官方窗口位置偏移: {self.coordDiff}")
        # 挂载功能
        self._mountFuture()

    def click_lt(self, coord):
        """鼠标左键点击"""
        Util.bg_click(
            {
                "hwnd": self.hwnd,
                "x": coord[1] + self.coordDiff[0],
                "y": coord[2] + self.coordDiff[1],
                "logger": self.logger,
            }
        )

    def load_config(self):
        """加载配置文件"""

        currentDir = os.path.dirname(os.path.abspath(__file__))
        baseConfigPath = os.path.join(currentDir, "..", "config", "base.json")
        with open(baseConfigPath, "r", encoding="utf-8") as f:
            config = json.load(f)
            self.logger.info(f"加载配置文件: {baseConfigPath}")

        if self.qq:
            try:
                qqConfigPath = os.path.join(
                    currentDir, "..", "config", f"{self.qq}.json"
                )
                with open(qqConfigPath, "r", encoding="utf-8") as f:
                    qqConfig = json.load(f)
                    self.logger.info(f"加载配置文件: {qqConfigPath}")
                    # 合并配置，覆盖 base 配置
                    config = {**config, **qqConfig}
            except FileNotFoundError:
                self.logger.warning(f"未找到配置文件: {qqConfigPath}, 使用默认配置")

        self.config = config
