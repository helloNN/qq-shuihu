import logging
from .util import Util
from future.beibao import Beibao

logging.basicConfig(
    filename="game.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)


class Game:
    """窗口句柄管理类"""

    logger = logging.getLogger(__name__)
    hwnd = None
    coordDiff = (0, 0)  # 位置偏移
    util = None
    beibao: Beibao = None

    def __init__(self, hwnd: int = None):
        """
        hwnd: 窗口句柄
        """
        self.hwnd = hwnd

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
        print("计算窗口位置")

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
