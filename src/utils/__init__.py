"""
QQ水浒跨平台自动化项目 - 工具模块
包含核心的自动化功能组件
"""

from .api_core import AutomationAPI, TaskPriority
from .automation_engine import CrossPlatformAutomationEngine
from .window_utils import CrossPlatformWindowManager
from .task_manager import TaskManager, BaseTask, Task, TaskResult, TaskStatus
from .config_manager import ExecutionMode, ClickMode, ImageMode, AutomationConfig

__all__ = [
    "AutomationAPI",
    "TaskPriority",
    "CrossPlatformAutomationEngine",
    "CrossPlatformWindowManager",
    "TaskManager",
    "BaseTask",
    "Task",
    "TaskResult",
    "TaskStatus",
    "ExecutionMode",
    "ClickMode",
    "ImageMode",
    "AutomationConfig",
]
