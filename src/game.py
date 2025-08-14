import sys
import os
import time
import platform

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import AutomationAPI, TaskPriority, ExecutionMode, ClickMode, ImageMode
from typing import List, Tuple


def main():
    """基础窗口操作示例"""
    print("=== 跨平台基础窗口操作示例 ===")
    print(f"当前操作系统: {platform.system()}")

    # 创建API实例
    api = AutomationAPI(197828)

    try:
        # 启动自动化系统
        api.start()

        # 设置为前台模式（跨平台兼容性更好）
        api.set_click_mode(ClickMode.FOREGROUND)
        api.set_image_mode(ImageMode.FOREGROUND)

        # 整个qq水浒软件的标题
        app_name = "MainWindow"
        app_child_name = "Chrome Legacy Window"

        api.click(445, 474)

    finally:
        # 停止自动化系统
        api.stop()


if __name__ == "__main__":
    main()
