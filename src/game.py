import sys
import os
import time
import platform

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import AutomationAPI, TaskPriority, ExecutionMode, ClickMode, ImageMode
from typing import List, Tuple


def basic_window_operations():
    """基础窗口操作示例"""
    print("=== 跨平台基础窗口操作示例 ===")
    print(f"当前操作系统: {platform.system()}")

    # 创建API实例
    api = AutomationAPI()

    try:
        # 启动自动化系统
        api.start()

        # 设置为前台模式（跨平台兼容性更好）
        api.set_click_mode(ClickMode.FOREGROUND)
        api.set_image_mode(ImageMode.FOREGROUND)

        # 整个qq水浒软件的标题
        app_name = "MainWindow"
        app_child_name = "Chrome Legacy Window"

        print(f"开始查找目标窗口 - 主窗口: '{app_name}', 子窗口: '{app_child_name}'")
        parent_windows = api.find_windows_by_title(app_name, exact_match=True)

        if len(parent_windows) == 0:
            print("未找到窗口")
            return
        print(
            f"找到 {len(parent_windows)} 个匹配的父窗口, hwnd: {parent_windows[0].hwnd}"
        )

        # 查找所有子窗口
        child_windows = api.find_child_windows(parent_windows[0].hwnd)
        hwnds = []
        for child in child_windows:
            print(f"  子窗口: {child.title} (句柄: {child.hwnd})")
            if child.title == app_child_name:
                hwnds.append(child.hwnd)

        print(f"找到 {len(hwnds)} 个匹配的子窗口", hwnds)
        if len(hwnds) == 0:
            print("未找到匹配的子窗口")
            return

        print("\n操作完成!")

    finally:
        # 停止自动化系统
        api.stop()


if __name__ == "__main__":
    basic_window_operations()
