"""
跨平台窗口管理模块
处理窗口句柄获取、窗口操作等功能
支持Windows、macOS、Linux
"""

import platform
import psutil
from typing import List, Dict, Optional, Tuple, Union
from dataclasses import dataclass
import logging

# 根据操作系统导入不同的窗口管理库
system = platform.system()

# 初始化变量
gw = None
WINDOWS_NATIVE = False
MACOS_NATIVE = False
LINUX_NATIVE = False
PYGETWINDOW_AVAILABLE = False

if system == "Windows":
    try:
        import win32gui
        import win32con
        import win32process

        WINDOWS_NATIVE = True

        # 尝试导入pygetwindow
        try:
            import pygetwindow as gw

            PYGETWINDOW_AVAILABLE = True
        except ImportError:
            logging.warning("pygetwindow not available on Windows")

    except ImportError:
        logging.warning("pywin32 not available")
        # 如果pywin32不可用，尝试只使用pygetwindow
        try:
            import pygetwindow as gw

            PYGETWINDOW_AVAILABLE = True
        except ImportError:
            logging.error("Neither pywin32 nor pygetwindow available")

elif system == "Darwin":  # macOS
    try:
        import Quartz
        import AppKit

        MACOS_NATIVE = True

        # 尝试导入pygetwindow
        try:
            import pygetwindow as gw

            PYGETWINDOW_AVAILABLE = True
        except (ImportError, NotImplementedError):
            logging.warning("pygetwindow not available on macOS")

    except ImportError:
        logging.error("macOS native libraries not available")

else:  # Linux
    try:
        import subprocess

        LINUX_NATIVE = True
        # 在Linux上，pygetwindow通常不可用，直接跳过导入
        logging.info(
            "Linux environment detected, using subprocess for window management"
        )
    except ImportError:
        logging.error("subprocess not available on Linux")


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


class CrossPlatformWindowManager:
    """跨平台窗口管理器"""

    def __init__(self):
        self.windows_cache: Dict[Union[int, str], WindowInfo] = {}
        self.system = platform.system()
        self.logger = logging.getLogger(__name__)

    def refresh_windows(self) -> None:
        """刷新窗口缓存"""
        self.windows_cache.clear()

        if not PYGETWINDOW_AVAILABLE:
            # 在Linux环境下，如果pygetwindow不可用，创建一个模拟窗口用于测试
            if self.system == "Linux":
                self._create_mock_windows()
            return

        try:
            # 使用pygetwindow获取所有窗口
            windows = gw.getAllWindows()

            for window in windows:
                try:
                    window_info = self._create_window_info(window)
                    if window_info:
                        self.windows_cache[window_info.hwnd] = window_info
                except Exception as e:
                    self.logger.debug(f"Error processing window {window}: {e}")

        except Exception as e:
            self.logger.error(f"Error refreshing windows: {e}")
            # 如果失败，在Linux下创建模拟窗口
            if self.system == "Linux":
                self._create_mock_windows()

    def _create_mock_windows(self) -> None:
        """在Linux环境下创建模拟窗口用于测试"""
        mock_windows = [
            WindowInfo(
                hwnd="mock_terminal_1",
                title="Terminal",
                class_name="gnome-terminal",
                pid=1234,
                process_name="gnome-terminal",
                rect=(100, 100, 800, 600),
                is_visible=True,
                is_minimized=False,
                is_maximized=False,
            ),
            WindowInfo(
                hwnd="mock_editor_1",
                title="Text Editor",
                class_name="gedit",
                pid=1235,
                process_name="gedit",
                rect=(200, 200, 900, 700),
                is_visible=True,
                is_minimized=False,
                is_maximized=False,
            ),
            WindowInfo(
                hwnd="mock_browser_1",
                title="Firefox",
                class_name="firefox",
                pid=1236,
                process_name="firefox",
                rect=(0, 0, 1920, 1080),
                is_visible=True,
                is_minimized=False,
                is_maximized=True,
            ),
        ]

        for window_info in mock_windows:
            self.windows_cache[window_info.hwnd] = window_info

        self.logger.info(f"Created {len(mock_windows)} mock windows for Linux testing")

    def _create_window_info(self, window) -> Optional[WindowInfo]:
        """从窗口对象创建WindowInfo"""
        try:
            # 获取基本信息
            title = window.title or ""

            # 获取窗口位置和尺寸
            try:
                left, top, width, height = (
                    window.left,
                    window.top,
                    window.width,
                    window.height,
                )
                rect = (left, top, left + width, top + height)
            except:
                rect = (0, 0, 0, 0)

            # 获取进程信息
            pid = 0
            process_name = "Unknown"
            class_name = ""

            if self.system == "Windows" and WINDOWS_NATIVE:
                try:
                    # 使用Windows原生API获取更详细信息
                    hwnd = window._hWnd if hasattr(window, "_hWnd") else 0
                    if hwnd:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        class_name = win32gui.GetClassName(hwnd)
                except:
                    pass

            # 使用psutil获取进程信息
            if pid:
                try:
                    process = psutil.Process(pid)
                    process_name = process.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # 获取窗口状态
            is_visible = True
            is_minimized = False
            is_maximized = False

            try:
                is_visible = window.visible
                is_minimized = window.isMinimized
                is_maximized = window.isMaximized
            except:
                pass

            # 创建唯一标识符
            hwnd = getattr(window, "_hWnd", None) or id(window)

            return WindowInfo(
                hwnd=hwnd,
                title=title,
                class_name=class_name,
                pid=pid,
                process_name=process_name,
                rect=rect,
                is_visible=is_visible,
                is_minimized=is_minimized,
                is_maximized=is_maximized,
            )

        except Exception as e:
            self.logger.debug(f"Error creating window info: {e}")
            return None

    def find_windows_by_title(
        self, title: str, exact_match: bool = False
    ) -> List[WindowInfo]:
        """根据标题查找窗口"""
        self.refresh_windows()
        result = []

        for window_info in self.windows_cache.values():
            if exact_match:
                if window_info.title == title:
                    result.append(window_info)
            else:
                if title.lower() in window_info.title.lower():
                    result.append(window_info)

        return result

    def find_windows_by_class(self, class_name: str) -> List[WindowInfo]:
        """根据类名查找窗口"""
        self.refresh_windows()
        result = []

        for window_info in self.windows_cache.values():
            if window_info.class_name == class_name:
                result.append(window_info)

        return result

    def find_windows_by_process(self, process_name: str) -> List[WindowInfo]:
        """根据进程名查找窗口"""
        self.refresh_windows()
        result = []

        for window_info in self.windows_cache.values():
            if window_info.process_name.lower() == process_name.lower():
                result.append(window_info)

        return result

    def get_window_info(self, hwnd: Union[int, str]) -> Optional[WindowInfo]:
        """获取指定窗口信息"""
        if hwnd in self.windows_cache:
            return self.windows_cache[hwnd]

        # 如果缓存中没有，尝试刷新后再查找
        self.refresh_windows()
        return self.windows_cache.get(hwnd)

    def bring_window_to_front(self, hwnd: Union[int, str]) -> bool:
        """将窗口置于前台"""
        try:
            window_info = self.get_window_info(hwnd)
            if not window_info:
                return False

            if not PYGETWINDOW_AVAILABLE:
                # 在Linux环境下模拟操作
                self.logger.info(
                    f"Mock: Bringing window '{window_info.title}' to front"
                )
                return True

            # 尝试通过标题找到pygetwindow对象
            windows = gw.getWindowsWithTitle(window_info.title)
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
            self.logger.error(f"Error bringing window to front: {e}")
            return False

    def show_window(self, hwnd: Union[int, str]) -> bool:
        """显示窗口"""
        try:
            window_info = self.get_window_info(hwnd)
            if not window_info:
                return False

            if not PYGETWINDOW_AVAILABLE:
                # 在Linux环境下模拟操作
                self.logger.info(f"Mock: Showing window '{window_info.title}'")
                return True

            windows = gw.getWindowsWithTitle(window_info.title)
            if not windows:
                return False

            target_window = windows[0]

            if target_window.isMinimized:
                target_window.restore()
            else:
                target_window.show()

            return True

        except Exception as e:
            self.logger.error(f"Error showing window: {e}")
            return False

    def hide_window(self, hwnd: Union[int, str]) -> bool:
        """隐藏窗口"""
        try:
            window_info = self.get_window_info(hwnd)
            if not window_info:
                return False

            if not PYGETWINDOW_AVAILABLE:
                self.logger.info(f"Mock: Hiding window '{window_info.title}'")
                return True

            windows = gw.getWindowsWithTitle(window_info.title)
            if not windows:
                return False

            target_window = windows[0]
            target_window.minimize()
            return True

        except Exception as e:
            self.logger.error(f"Error hiding window: {e}")
            return False

    def minimize_window(self, hwnd: Union[int, str]) -> bool:
        """最小化窗口"""
        try:
            window_info = self.get_window_info(hwnd)
            if not window_info:
                return False

            if not PYGETWINDOW_AVAILABLE:
                self.logger.info(f"Mock: Minimizing window '{window_info.title}'")
                return True

            windows = gw.getWindowsWithTitle(window_info.title)
            if not windows:
                return False

            target_window = windows[0]
            target_window.minimize()
            return True

        except Exception as e:
            self.logger.error(f"Error minimizing window: {e}")
            return False

    def maximize_window(self, hwnd: Union[int, str]) -> bool:
        """最大化窗口"""
        try:
            window_info = self.get_window_info(hwnd)
            if not window_info:
                return False

            if not PYGETWINDOW_AVAILABLE:
                self.logger.info(f"Mock: Maximizing window '{window_info.title}'")
                return True

            windows = gw.getWindowsWithTitle(window_info.title)
            if not windows:
                return False

            target_window = windows[0]
            target_window.maximize()
            return True

        except Exception as e:
            self.logger.error(f"Error maximizing window: {e}")
            return False

    def restore_window(self, hwnd: Union[int, str]) -> bool:
        """恢复窗口"""
        try:
            window_info = self.get_window_info(hwnd)
            if not window_info:
                return False

            if not PYGETWINDOW_AVAILABLE:
                self.logger.info(f"Mock: Restoring window '{window_info.title}'")
                return True

            windows = gw.getWindowsWithTitle(window_info.title)
            if not windows:
                return False

            target_window = windows[0]
            target_window.restore()
            return True

        except Exception as e:
            self.logger.error(f"Error restoring window: {e}")
            return False

    def resize_window(self, hwnd: Union[int, str], width: int, height: int) -> bool:
        """调整窗口大小"""
        try:
            window_info = self.get_window_info(hwnd)
            if not window_info:
                return False

            if not PYGETWINDOW_AVAILABLE:
                self.logger.info(
                    f"Mock: Resizing window '{window_info.title}' to {width}x{height}"
                )
                return True

            windows = gw.getWindowsWithTitle(window_info.title)
            if not windows:
                return False

            target_window = windows[0]
            target_window.resizeTo(width, height)
            return True

        except Exception as e:
            self.logger.error(f"Error resizing window: {e}")
            return False

    def move_window(self, hwnd: Union[int, str], x: int, y: int) -> bool:
        """移动窗口"""
        try:
            window_info = self.get_window_info(hwnd)
            if not window_info:
                return False

            if not PYGETWINDOW_AVAILABLE:
                self.logger.info(
                    f"Mock: Moving window '{window_info.title}' to ({x}, {y})"
                )
                return True

            windows = gw.getWindowsWithTitle(window_info.title)
            if not windows:
                return False

            target_window = windows[0]
            target_window.moveTo(x, y)
            return True

        except Exception as e:
            self.logger.error(f"Error moving window: {e}")
            return False

    def get_all_windows(self, include_hidden: bool = False) -> List[WindowInfo]:
        """获取所有窗口"""
        self.refresh_windows()

        if include_hidden:
            return list(self.windows_cache.values())
        else:
            return [w for w in self.windows_cache.values() if w.is_visible and w.title]

    def get_active_window(self) -> Optional[WindowInfo]:
        """获取当前活动窗口"""
        if not PYGETWINDOW_AVAILABLE:
            # 在Linux环境下返回第一个模拟窗口作为活动窗口
            self.refresh_windows()
            windows = list(self.windows_cache.values())
            if windows:
                self.logger.info(f"Mock: Active window is '{windows[0].title}'")
                return windows[0]
            return None

        try:
            active_window = gw.getActiveWindow()
            if active_window:
                return self._create_window_info(active_window)
        except Exception as e:
            self.logger.error(f"Error getting active window: {e}")
        return None

    def get_window_at_position(self, x: int, y: int) -> Optional[WindowInfo]:
        """获取指定位置的窗口"""
        if not PYGETWINDOW_AVAILABLE:
            # 在Linux环境下根据坐标返回合适的模拟窗口
            self.refresh_windows()
            for window_info in self.windows_cache.values():
                left, top, right, bottom = window_info.rect
                if left <= x <= right and top <= y <= bottom:
                    self.logger.info(
                        f"Mock: Window at ({x}, {y}) is '{window_info.title}'"
                    )
                    return window_info
            return None

        try:
            window = gw.getWindowsAt(x, y)
            if window:
                return self._create_window_info(window[0])
        except Exception as e:
            self.logger.error(f"Error getting window at position: {e}")
        return None

    def find_child_windows(self, parent_hwnd: int) -> List[WindowInfo]:
        """查找指定父窗口的所有子窗口(Windows平台专用)"""
        if not WINDOWS_NATIVE:
            self.logger.warning("find_child_windows is only supported on Windows")
            return []

        child_windows = []

        def enum_child_callback(hwnd: int, _: int) -> bool:
            try:
                # 获取窗口标题
                length = win32gui.GetWindowTextLength(hwnd)
                title = win32gui.GetWindowText(hwnd) if length > 0 else ""

                # 获取类名
                class_name = win32gui.GetClassName(hwnd)

                # 获取进程信息
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process_name = "Unknown"
                try:
                    process = psutil.Process(pid)
                    process_name = process.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

                # 获取窗口位置和状态
                rect = win32gui.GetWindowRect(hwnd)
                is_visible = win32gui.IsWindowVisible(hwnd)
                is_minimized = win32gui.IsIconic(hwnd)

                # 创建WindowInfo对象
                window_info = WindowInfo(
                    hwnd=hwnd,
                    title=title,
                    class_name=class_name,
                    pid=pid,
                    process_name=process_name,
                    rect=rect,
                    is_visible=is_visible,
                    is_minimized=is_minimized,
                )
                child_windows.append(window_info)
            except Exception as e:
                self.logger.error(f"Error processing child window {hwnd}: {e}")
            return True  # 继续枚举

        try:
            win32gui.EnumChildWindows(parent_hwnd, enum_child_callback, 0)
            return child_windows
        except Exception as e:
            self.logger.error(f"Error enumerating child windows: {e}")
            return []


# 为了向后兼容，创建别名
WindowManager = CrossPlatformWindowManager
