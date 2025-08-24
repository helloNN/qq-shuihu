import win32api
import win32con
import time


class Util:
    @staticmethod
    def getPosition(rect):
        return (rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)

    @staticmethod
    def bg_click(info: dict):
        """
        后台左键单机\n
        x: x坐标\n
        y: y坐标\n
        """

        info["logger"].info(f"[{info['hwnd']}] 后台点击: ({info['x']},{info['y']})")

        long_position = win32api.MAKELONG(info["x"], info["y"])
        win32api.SendMessage(info["hwnd"], win32con.WM_LBUTTONDOWN, 0, long_position)
        time.sleep(0.05)
        win32api.SendMessage(info["hwnd"], win32con.WM_LBUTTONUP, 0, long_position)
