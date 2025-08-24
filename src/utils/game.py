import logging
from .util import Util
from future.beibao import Beibao

logging.basicConfig(
    filename="logs/game.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)


class Game:
    """游戏管理类"""

    hwnd = None
    name = ""
    logger = None
    coordDiff = (0, 0)  # 位置偏移
    util = None
    beibao: Beibao = None

    def __init__(self, hwnd: int = None, name=""):
        """
        hwnd: 窗口句柄
        """
        self.hwnd = hwnd
        self.name = name
        self.logger = logging.getLogger(f"Game-{self.name or __name__}")
        if name:
            # 多任务则自定义日志
            self._cutomLogger()

    def _cutomLogger(self):
        """自定义日志"""
        log_filename = f"logs/{self.name}.log"
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

        self.logger.info(f"{self.name} | 日志游戏实例初始化")

    def _mountFuture(self):
        util = Util(self.hwnd, self.coordDiff, self.logger)
        self.util = util

        # 挂载背包功能
        self.beibao = Beibao(util)

    def set_hwnd(self, hwnd: int):
        """设置窗口句柄"""
        self.hwnd = hwnd

    def count_position(self, app):
        """计算窗口位置"""
        print(f"{self.name + ':' if self.name else ''}计算窗口位置")

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
        self.logger.info(f"flash窗口: {flashAreaRect}")

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
