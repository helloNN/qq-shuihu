"""
项目配置文件
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ExecutionMode(Enum):
    """执行模式：线程或进程"""

    THREAD = "thread"
    PROCESS = "process"


class ClickMode(Enum):
    """点击模式：前台或后台"""

    FOREGROUND = "foreground"
    BACKGROUND = "background"


class ImageMode(Enum):
    """图像识别模式：前台或后台"""

    FOREGROUND = "foreground"
    BACKGROUND = "background"


@dataclass
class AutomationConfig:
    """自动化配置类"""

    execution_mode: ExecutionMode = ExecutionMode.THREAD
    click_mode: ClickMode = ClickMode.BACKGROUND
    image_mode: ImageMode = ImageMode.BACKGROUND
    max_workers: int = 4
    task_timeout: int = 30
    retry_count: int = 3
    retry_delay: float = 1.0
    screenshot_quality: int = 95

    def set_execution_mode(self, mode: ExecutionMode):
        """设置执行模式"""
        self.execution_mode = mode

    def set_click_mode(self, mode: ClickMode):
        """设置点击模式"""
        self.click_mode = mode

    def set_image_mode(self, mode: ImageMode):
        """设置图像识别模式"""
        self.image_mode = mode


# 全局配置实例
config = AutomationConfig()
