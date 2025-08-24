from dataclasses import dataclass
from typing import List, Tuple, Union
import win32gui  # 获取窗口信息
import win32process  # 获取进程信息
import psutil  # 使用psutil获取进程信息

import pygetwindow as gw  # 用于获取窗口信息


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
            print(f"Error getting window info for hwnd {hwnd}: {e}")
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
                print(f"Error processing child window {hwnd}: {e}")
            return True  # 继续枚举

        try:
            win32gui.EnumChildWindows(
                hwnd, lambda h, _: enum_child_callback(h, current_depth + 1), 0
            )
            return all_child_windows
        except Exception as e:
            print(f"Error enumerating child windows for hwnd {hwnd}: {e}")
            return []

    @classmethod
    def bring_window_to_front(self, hwnd: int) -> bool:
        """将窗口置于前台"""
        try:
            window = self.get_hwndInfo(hwnd)
            print(window)
            # 尝试通过标题找到pygetwindow对象
            windows = gw.getWindowsWithTitle(window.title)
            print(windows)
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
            print(f"将窗口置于前台[失败]: {e}")
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
            print(f"find_hwndByTitle_p_child:\t未找到父窗口({pTitle})")
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
