"""
QQ水浒跨平台自动化项目
一个功能强大的跨平台软件自动化框架
"""

__version__ = "2.0.0"
__author__ = "QQ水浒自动化团队"
__description__ = "跨平台软件自动化框架，支持Windows、macOS、Linux"

# 导出主要API
try:
    from .main import (
        AutomationAPI,
        TaskPriority,
        api,
        start_automation,
        stop_automation,
        set_thread_mode,
        set_process_mode,
        set_foreground_mode,
        set_background_mode,
        find_window,
        click,
        click_image,
        create_click_task,
        create_image_task,
        wait_for_task,
        get_task_status,
    )

    from .config import (
        config,
        ExecutionMode,
        ClickMode,
        ImageMode,
    )

    from .window_manager import (
        CrossPlatformWindowManager,
        WindowInfo,
    )

    from .automation import (
        CrossPlatformAutomationEngine,
    )

    from .task_system import (
        TaskManager,
        Task,
        TaskPriority,
        TaskStatus,
        TaskResult,
        BaseTask,
        ClickTask,
        ImageRecognitionTask,
        task_manager,
    )
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    try:
        from main import (
            AutomationAPI,
            TaskPriority,
            api,
            start_automation,
            stop_automation,
            set_thread_mode,
            set_process_mode,
            set_foreground_mode,
            set_background_mode,
            find_window,
            click,
            click_image,
            create_click_task,
            create_image_task,
            wait_for_task,
            get_task_status,
        )

        from config import (
            config,
            ExecutionMode,
            ClickMode,
            ImageMode,
        )

        from window_manager import (
            CrossPlatformWindowManager,
            WindowInfo,
        )

        from automation import (
            CrossPlatformAutomationEngine,
        )

        from task_system import (
            TaskManager,
            Task,
            TaskPriority,
            TaskStatus,
            TaskResult,
            BaseTask,
            ClickTask,
            ImageRecognitionTask,
            task_manager,
        )
    except ImportError:
        # 如果都失败了，设置为None，避免导入错误
        AutomationAPI = None
        TaskPriority = None
        api = None
        config = None
        ExecutionMode = None
        ClickMode = None
        ImageMode = None
        CrossPlatformWindowManager = None
        WindowInfo = None
        CrossPlatformAutomationEngine = None
        TaskManager = None
        Task = None
        TaskStatus = None
        TaskResult = None
        BaseTask = None
        ClickTask = None
        ImageRecognitionTask = None
        task_manager = None

# 向后兼容的别名
WindowManager = CrossPlatformWindowManager
AutomationEngine = CrossPlatformAutomationEngine

__all__ = [
    # 主要API
    "AutomationAPI",
    "TaskPriority",
    "api",
    # 便捷函数
    "start_automation",
    "stop_automation",
    "set_thread_mode",
    "set_process_mode",
    "set_foreground_mode",
    "set_background_mode",
    "find_window",
    "click",
    "click_image",
    "create_click_task",
    "create_image_task",
    "wait_for_task",
    "get_task_status",
    # 配置
    "config",
    "ExecutionMode",
    "ClickMode",
    "ImageMode",
    # 窗口管理
    "CrossPlatformWindowManager",
    "WindowManager",  # 向后兼容
    "WindowInfo",
    # 自动化引擎
    "CrossPlatformAutomationEngine",
    "AutomationEngine",  # 向后兼容
    # 任务系统
    "TaskManager",
    "Task",
    "TaskStatus",
    "TaskResult",
    "BaseTask",
    "ClickTask",
    "ImageRecognitionTask",
    "task_manager",
]
