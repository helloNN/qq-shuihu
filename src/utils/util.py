import win32api
import win32con
import time


class Util:
    hwnd = None
    offset = (0, 0)
    logger = None

    def __init__(self, hwnd, offset, logger):
        self.hwnd = hwnd
        self.offset = offset
        self.logger = logger

    def click(self, coord):
        Util.bg_click(
            {
                "hwnd": self.hwnd,
                "name": coord[0],
                "coord": (coord[1] + self.offset[0], coord[2] + self.offset[1]),
                "logger": self.logger,
            }
        )

    @staticmethod
    def getPosition(rect):
        return (rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)

    @staticmethod
    def bg_click(info: dict):
        """
        后台左键单机
        """
        info["logger"].info(
            f"{info['hwnd']} | 后台点击: {info['name']} {info['coord']})"
        )

        (x, y) = info["coord"]
        long_position = win32api.MAKELONG(x, y)
        win32api.SendMessage(info["hwnd"], win32con.WM_LBUTTONDOWN, 0, long_position)
        time.sleep(0.05)
        win32api.SendMessage(info["hwnd"], win32con.WM_LBUTTONUP, 0, long_position)
