import win32api
import win32con
import time
from logging import Logger


class Util:
    hwnd = None
    offset = (0, 0)
    logger: Logger = None

    def __init__(self, hwnd, offset, logger: Logger):
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

    def type_content(self, coord, content):
        Util.flash_input_wm_char(
            {
                "hwnd": self.hwnd,
                "name": coord[0],
                "coord": (coord[1] + self.offset[0], coord[2] + self.offset[1]),
                "logger": self.logger,
            },
            content,
        )

    @staticmethod
    def getPosition(rect):
        return (rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)

    @staticmethod
    def bg_click(info: dict):
        """
        后台左键单机
        """
        # print("info:", info)
        info["logger"].info(
            f"{info['hwnd']} | 后台点击: {info['name']} {info['coord']})"
        )

        (x, y) = info["coord"]
        long_position = win32api.MAKELONG(x, y)
        win32api.SendMessage(info["hwnd"], win32con.WM_LBUTTONDOWN, 0, long_position)
        time.sleep(0.05)
        win32api.SendMessage(info["hwnd"], win32con.WM_LBUTTONUP, 0, long_position)

    @classmethod
    def bg_input_number(cls, info: dict, number):
        """
        后台向指定窗口的指定位置输入数字
        :param info: 字典，包含 hwnd(窗口句柄)、coord(窗口内相对坐标(x,y))、logger(日志对象)、name(标识名)
        :param number: 要输入的数字（int/str）
        """
        try:
            # 1. 先后台点击目标位置，获取输入焦点
            cls.bg_click(info)
            time.sleep(0.1)  # 等待焦点生效

            # 2. 转换数字为字符串，逐字符发送键盘输入消息
            number_str = str(number)
            print(f"{info['hwnd']} | 后台输入数字: {number_str}")

            for char in number_str:
                # 获取字符对应的虚拟键码
                vk_code = win32api.VkKeyScan(char) & 0xFF  # 只取低8位（虚拟键码）
                # 发送键盘按下消息
                win32api.SendMessage(info["hwnd"], win32con.WM_KEYDOWN, vk_code, 0)
                time.sleep(0.1)  # 模拟真实输入的间隔
                # 发送键盘抬起消息
                win32api.SendMessage(info["hwnd"], win32con.WM_KEYUP, vk_code, 0)
                time.sleep(0.1)

            print(f"{info['hwnd']} | 数字输入完成: {number_str}")
        except Exception as e:
            info["logger"].error(f"后台输入数字失败: {e}")
            raise

    @classmethod
    def flash_input_wm_char(cls, info: dict, number):
        """
        原生WM_CHAR消息向Flash窗口输入数字（适配性远优于WM_KEYDOWN）
        """
        try:
            # 1. 后台点击获取焦点
            cls.bg_click(info)
            time.sleep(0.1)

            # 2. 转换数字为字符串，发送WM_CHAR消息
            number_str = str(number)
            info["logger"].info(f"{info['hwnd']} | 后台输入内容: {number_str}")
            print(f"{info['hwnd']} | 后台输入内容: {number_str}")

            for char in number_str:
                # 获取字符的ASCII码（WM_CHAR使用ASCII码，而非虚拟键码）
                char_ascii = ord(char)
                # 发送字符输入消息（核心：WM_CHAR）
                win32api.SendMessage(info["hwnd"], win32con.WM_CHAR, char_ascii, 0)
                time.sleep(0.03)  # Flash响应较慢，增加间隔

            info["logger"].info(f"{info['hwnd']} | 后台输入内容完毕: {number_str}")
            print(f"{info['hwnd']} | 后台输入内容完毕: {number_str}")
        except Exception as e:
            info["logger"].error(f"WM_CHAR输入失败: {e}")
            raise
