from dataclasses import dataclass
from typing import List, Tuple, Union
import win32gui
import win32process
import psutil  # 使用psutil获取进程信息
import logging
import pygetwindow as gw  # 用于获取窗口信息
import pyautogui  # 用于前台点击


@dataclass
class WindowInfo:
    """窗口信息类"""

    hwnd: Union[int, str]  # 窗口句柄或标识符
    title: str
    class_name: str
    pid: int
    process_name: str
    rect: Tuple[int, int, int, int]  # (left, top, right, bottom)
    is_visible: bool
    is_minimized: bool
    is_maximized: bool = False


class Hwnd:
    """窗口句柄管理类"""

    name = "Hwnd"
    desc = "窗口句柄管理类"

    # 静态方法
    @classmethod
    def get_hwndInfo(self, hwnd: int):
        """获取窗口信息"""
        try:
            length = win32gui.GetWindowTextLength(hwnd)
            title = win32gui.GetWindowText(hwnd) if length > 0 else ""
            class_name = win32gui.GetClassName(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process_name = (
                psutil.Process(pid).name() if psutil.pid_exists(pid) else "Unknown"
            )
            rect = win32gui.GetWindowRect(hwnd)
            is_visible = win32gui.IsWindowVisible(hwnd)
            is_minimized = win32gui.IsIconic(hwnd)

            return WindowInfo(
                hwnd=hwnd,
                title=title,
                class_name=class_name,
                pid=pid,
                process_name=process_name,
                rect=rect,
                is_visible=is_visible,
                is_minimized=is_minimized,
            )
        except Exception as e:
            logging.error(f"Error getting window info for hwnd {hwnd}: {e}")
            return None

    @classmethod
    def find_childHwnds(
        cls, hwnd: int, include_hidden: bool = False, max_depth: int = 20
    ) -> List[WindowInfo]:
        """
        查找指定窗口的所有子窗口

        参数:
            hwnd: 父窗口句柄
            include_hidden: 是否包含隐藏窗口，默认为False
            max_depth: 递归查找的最大深度，默认为20层

        返回:
            包含所有子窗口信息的WindowInfo列表
        """
        all_child_windows = []
        current_depth = 0

        def enum_child_callback(hwnd: int, depth: int) -> bool:
            nonlocal current_depth
            current_depth = depth

            try:
                window_info = cls.get_hwndInfo(hwnd)
                if window_info and (include_hidden or window_info.is_visible):
                    all_child_windows.append(window_info)

                if depth < max_depth:
                    win32gui.EnumChildWindows(
                        hwnd, lambda h, _: enum_child_callback(h, depth + 1), 0
                    )

            except Exception as e:
                logging.error(f"Error processing child window {hwnd}: {e}")
            return True  # 继续枚举

        try:
            win32gui.EnumChildWindows(
                hwnd, lambda h, _: enum_child_callback(h, current_depth + 1), 0
            )
            return all_child_windows
        except Exception as e:
            logging.error(f"Error enumerating child windows for hwnd {hwnd}: {e}")
            return []

    @classmethod
    def bring_window_to_front(self, hwnd: int) -> bool:
        """将窗口置于前台"""
        try:
            window = self.get_hwndInfo(hwnd)

            # 尝试通过标题找到pygetwindow对象
            windows = gw.getWindowsWithTitle(window.title)
            if not windows:
                return False

            target_window = windows[0]

            # 如果窗口最小化，先恢复
            if target_window.isMinimized:
                target_window.restore()

            # 激活窗口
            target_window.activate()
            return True

        except Exception as e:
            self.logger.error(f"将窗口置于前台[失败]: {e}")
            return False

    @classmethod
    def find_hwndByTitle_p_child(self, pTitle: str, childTitle=str) -> Union[int, None]:
        """
        根据父窗口标题和子窗口标题获取窗口信息

        参数:
            pTitle: 父窗口标题
            childTitle: 子窗口标题

        返回:
            WindowInfo对象或None
        """
        targetHwnd = None

        p_hwnd = win32gui.FindWindow(None, pTitle)
        if not p_hwnd:
            logging.error(f"find_hwndByTitle_p_child:\t未找到父窗口({pTitle})")
            return None

        def fn(hwnd, _):
            nonlocal targetHwnd
            title = win32gui.GetWindowText(hwnd)
            if title == childTitle:
                targetHwnd = hwnd
                return
            else:
                return

        win32gui.EnumChildWindows(p_hwnd, fn, None)

        return targetHwnd


class Automation(Hwnd):
    name = "automation"
    desc = "自动化操作类"
    clickMode = "FE"  # 默认前台点击
    hwnd = None

    def __init__(self):
        self.clickMode = "FE"

    def set_clickMode(self, mode: str):
        """
        设置点击模式
        参数:
            mode: 'FE' 前台点击, 'BG' 后台点击
        """
        if mode in ["FE", "BG"]:
            self.clickMode = mode
        else:
            raise ValueError("Invalid click mode. Use 'FE' or 'BG'.")

    def _FE_click(self, x: int, y: int, button: str) -> bool:
        """前台点击"""
        try:
            # 获取窗口信息
            window_info = self.bring_window_to_front(self.hwnd)
            if not window_info:
                self.logger.error(f"无法获取窗口信息, 所以: 前台点击失败({self.hwnd}) ")
                return False

            print(window_info.rect)
            # 计算屏幕坐标
            screen_x = window_info.rect[0] + x
            screen_y = window_info.rect[1] + y

            # 使用pyautogui进行点击
            mouse_button = self._get_button(button)
            pyautogui.click(screen_x, screen_y, button=mouse_button)

            return True

        except Exception as e:
            self.logger.error(f"FE click failed: {e}")
            return False

    def _BG_click(self, x: int, y: int, button: str) -> bool:
        """后台点击"""
        try:
            # 对于跨平台兼容性，后台点击实际上还是需要前台操作
            # 但我们可以先保存当前鼠标位置，点击后恢复
            current_pos = pyautogui.position()

            # 获取窗口信息
            window = self.get_hwndInfo(self.hwnd)

            # 计算屏幕坐标
            screen_x = window.rect[0] + x
            screen_y = window.rect[1] + y

            # 执行点击
            mouse_button = self._get_button(button)
            pyautogui.click(screen_x, screen_y, button=mouse_button)

            # 恢复鼠标位置
            pyautogui.moveTo(current_pos.x, current_pos.y)

            return True

        except Exception as e:
            self.logger.error(f"BG click failed: {e}")
            return False

    def _get_button(self, button: str) -> str:
        """获取pyautogui的按钮名称"""
        button_map = {"left": "left", "right": "right", "middle": "middle"}
        return button_map.get(button.lower(), "left")

    def click(self, x: int, y: int, button: str = "left") -> bool:
        """
        点击指定窗口的坐标

        Args:
            x: X坐标（相对于窗口）
            y: Y坐标（相对于窗口）
            button: 鼠标按钮 ("left", "right", "middle")

        Returns:
            bool: 是否成功
        """
        try:
            if self.clickMode == "FE":
                return self._FE_click(x, y, button)
            else:
                return self._BG_click(x, y, button)
        except Exception as e:
            self.logger.error(f"点击失败: {e}")
            return False

    def hello(self):
        print("Hello from Automation")


class GameHwnd(Automation):
    """窗口句柄管理类"""

    logger = logging.getLogger(__name__)

    def __init__(self, hwnd: int):
        """
        hwnd: 窗口句柄
        """
        self.hwnd = hwnd

    def set_hwnd(self, hwnd: int):
        """设置窗口句柄"""
        self.hwnd = hwnd
