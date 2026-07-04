import win32api
import win32con
import win32clipboard

import time
from logging import Logger


class Util:
    hwnd = None
    offset = (0, 0)
    logger: Logger = None

    def __init__(self, hwnd, offset, logger: Logger, printClick=False):
        self.hwnd = hwnd
        self.offset = offset
        self.logger = logger
        self.printClick = printClick

    def click(self, coord):
        Util.bg_click(
            {
                "hwnd": self.hwnd,
                "name": coord[0],
                "coord": (coord[1] + self.offset[0], coord[2] + self.offset[1]),
                "logger": self.logger,
            },
            self.printClick,
        )

    def type_content(self, coord, content):
        Util.flash_input_set(
            {
                "hwnd": self.hwnd,
                "name": coord[0],
                "coord": (coord[1] + self.offset[0], coord[2] + self.offset[1]),
                "logger": self.logger,
            },
            content,
        )

    def get_content(self, coord):
        return Util.flash_input_get(
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
    def bg_click(info: dict, printClick=False):
        """
        后台左键单机
        """
        x, y = info["coord"]
        long_position = win32api.MAKELONG(x, y)
        win32api.SendMessage(info["hwnd"], win32con.WM_LBUTTONDOWN, 0, long_position)
        time.sleep(0.05)
        win32api.SendMessage(info["hwnd"], win32con.WM_LBUTTONUP, 0, long_position)

        info["logger"].info(
            f"{info['hwnd']} | 后台点击: {info['name']} {info['coord']})"
        )
        if printClick:
            print(f"后台点击: {info['name']} {info['coord']})")

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
    def flash_input_set(cls, info: dict, number):
        """
        原生WM_CHAR消息向Flash窗口输入数字（适配性远优于WM_KEYDOWN）
        """
        try:
            # 1. 后台点击获取焦点
            cls.bg_click(info, False)
            time.sleep(0.2)

            # 2. 转换数字为字符串，发送WM_CHAR消息
            number_str = str(number)
            info["logger"].info(f"{info['hwnd']} | 后台输入内容: {number_str}")
            # print(f"{info['hwnd']} | 后台输入内容: {number_str}")

            for char in number_str:
                # 获取字符的ASCII码（WM_CHAR使用ASCII码，而非虚拟键码）
                char_ascii = ord(char)
                # 发送字符输入消息（核心：WM_CHAR）
                win32api.SendMessage(info["hwnd"], win32con.WM_CHAR, char_ascii, 0)
                time.sleep(0.05)  # Flash响应较慢，增加间隔

            info["logger"].info(f"{info['hwnd']} | 后台输入内容完毕: {number_str}")
            # print(f"{info['hwnd']} | 后台输入内容完毕: {number_str}")
        except Exception as e:
            info["logger"].error(f"WM_CHAR输入失败: {e}")
            raise

    @classmethod
    def flash_input_get(cls, info: dict) -> str:
        """
        【终极版】后台消息模拟 Ctrl+A → Ctrl+C 读取 Flash 输入框内容
        无前台按键、无剪贴板报错、不抢窗口、不干扰用户
        """
        # 1. 后台点击获取焦点
        cls.bg_click(info)
        time.sleep(0.2)

        hwnd = info["hwnd"]

        # 2. 系统级模拟 Ctrl+A（和手动一模一样！）

        # 3. 系统级模拟 Ctrl+C

        # 4.获取剪切板内容
        text = Util.get_ctrl_c()
        print(f"剪贴板内容: {text}")

    @staticmethod
    def get_ctrl_c():
        """获取剪切板内容
        :return None:
        """
        text = ""
        for _ in range(5):
            try:
                # 正确打开剪贴板方式（无None参数）
                win32clipboard.OpenClipboard()
                try:
                    text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                except:
                    text = ""
                win32clipboard.CloseClipboard()
                break
            except Exception as e:
                time.sleep(0.1)

        final_text = str(text).strip()
        return final_text
