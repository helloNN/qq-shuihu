"""
主要API模块
提供简单易用的自动化接口
"""

import logging
import time
from typing import Optional, List, Dict, Any, Union

try:
    from .config_manager import config, ExecutionMode, ClickMode, ImageMode
    from .window_utils import CrossPlatformWindowManager, WindowInfo
    from .automation_engine import CrossPlatformAutomationEngine
    from .task_manager import (
        TaskManager,
        Task,
        TaskPriority,
        TaskStatus,
        TaskResult,
        ClickTask,
        ImageRecognitionTask,
        BaseTask,
        task_manager,
    )
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    import sys
    import os

    current_dir = os.path.dirname(__file__)
    sys.path.insert(0, current_dir)

    from config_manager import config, ExecutionMode, ClickMode, ImageMode
    from window_utils import CrossPlatformWindowManager, WindowInfo
    from automation_engine import CrossPlatformAutomationEngine
    from task_manager import (
        TaskManager,
        Task,
        TaskPriority,
        TaskStatus,
        TaskResult,
        ClickTask,
        ImageRecognitionTask,
        BaseTask,
        task_manager,
    )


class AutomationAPI:
    """自动化API主类"""

    def __init__(self, hwnd: int):
        """
        hwnd: 窗口句柄
        """
        self.window_manager = CrossPlatformWindowManager()
        self.automation_engine = CrossPlatformAutomationEngine()
        self.task_manager = task_manager
        self.hwnd = hwnd

        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def start(self):
        """启动自动化系统"""
        self.task_manager.start()
        self.logger.info("Automation system started")

    def stop(self):
        """停止自动化系统"""
        self.task_manager.stop()
        self.logger.info("Automation system stopped")

    # 配置相关方法
    def set_execution_mode(self, mode: Union[str, ExecutionMode]):
        """设置执行模式：线程或进程"""
        if isinstance(mode, str):
            mode = ExecutionMode(mode)
        config.set_execution_mode(mode)
        self.logger.info(f"Execution mode set to: {mode.value}")

    def set_click_mode(self, mode: Union[str, ClickMode]):
        """设置点击模式：前台或后台"""
        if isinstance(mode, str):
            mode = ClickMode(mode)
        config.set_click_mode(mode)
        self.logger.info(f"Click mode set to: {mode.value}")

    def set_image_mode(self, mode: Union[str, ImageMode]):
        """设置图像识别模式：前台或后台"""
        if isinstance(mode, str):
            mode = ImageMode(mode)
        config.set_image_mode(mode)
        self.logger.info(f"Image mode set to: {mode.value}")

    # 窗口管理方法
    def find_windows_by_title(
        self, title: str, exact_match: bool = False
    ) -> List[WindowInfo]:
        """根据标题查找窗口"""
        return self.window_manager.find_windows_by_title(title, exact_match)

    def find_windows_by_class(self, class_name: str) -> List[WindowInfo]:
        """根据类名查找窗口"""
        return self.window_manager.find_windows_by_class(class_name)

    def find_windows_by_process(self, process_name: str) -> List[WindowInfo]:
        """根据进程名查找窗口"""
        return self.window_manager.find_windows_by_process(process_name)

    def find_child_windows(self, parent_hwnd: Union[int, str]) -> List[WindowInfo]:
        """查找子窗口"""
        return self.window_manager.find_child_windows(parent_hwnd)

    def get_all_windows(self, include_hidden: bool = False) -> List[WindowInfo]:
        """获取所有窗口"""
        return self.window_manager.get_all_windows(include_hidden)

    def bring_window_to_front(self, hwnd: Union[int, str]) -> bool:
        """将窗口置于前台"""
        return self.window_manager.bring_window_to_front(hwnd)

    def show_window(self, hwnd: Union[int, str]) -> bool:
        """显示窗口"""
        return self.window_manager.show_window(hwnd)

    def hide_window(self, hwnd: Union[int, str]) -> bool:
        """隐藏窗口"""
        return self.window_manager.hide_window(hwnd)

    # 直接操作方法（同步）
    def click(self, x: int, y: int, button: str = "left") -> bool:
        print(f"点击了坐标: ({x}, {y})")
        return self.automation_engine.click(self.hwnd, x, y, button)

    def double_click(
        self, hwnd: Union[int, str], x: int, y: int, button: str = "left"
    ) -> bool:
        """直接双击"""
        return self.automation_engine.double_click(hwnd, x, y, button)

    def drag(
        self, hwnd: Union[int, str], start_x: int, start_y: int, end_x: int, end_y: int
    ) -> bool:
        """直接拖拽"""
        return self.automation_engine.drag(hwnd, start_x, start_y, end_x, end_y)

    def send_text(self, hwnd: Union[int, str], text: str) -> bool:
        """发送文本"""
        return self.automation_engine.send_text(hwnd, text)

    def send_key(
        self,
        hwnd: Union[int, str],
        key_code: Union[int, str],
        ctrl: bool = False,
        alt: bool = False,
        shift: bool = False,
    ) -> bool:
        """发送按键"""
        return self.automation_engine.send_key(hwnd, key_code, ctrl, alt, shift)

    def find_image(
        self, hwnd: Union[int, str], template_path: str, threshold: float = 0.8
    ) -> Optional[Dict[str, Any]]:
        """查找图像"""
        return self.automation_engine.find_image(hwnd, template_path, threshold)

    def click_image(
        self,
        hwnd: Union[int, str],
        template_path: str,
        threshold: float = 0.8,
        button: str = "left",
    ) -> bool:
        """点击图像"""
        return self.automation_engine.click_image(
            hwnd, template_path, threshold, button
        )

    def wait_for_image(
        self,
        hwnd: Union[int, str],
        template_path: str,
        timeout: int = 10,
        threshold: float = 0.8,
    ) -> Optional[Dict[str, Any]]:
        """等待图像出现"""
        return self.automation_engine.wait_for_image(
            hwnd, template_path, timeout, threshold
        )

    def capture_window(self, hwnd: Union[int, str]) -> Optional[Any]:
        """截取窗口"""
        return self.automation_engine.capture_window(hwnd)

    def scroll(
        self, hwnd: Union[int, str], x: int, y: int, direction: str, clicks: int = 3
    ) -> bool:
        """滚动"""
        return self.automation_engine.scroll(hwnd, x, y, direction, clicks)

    # 任务相关方法（异步）
    def create_click_task(
        self,
        hwnd: Union[int, str],
        x: int,
        y: int,
        button: str = "left",
        name: str = "",
        priority: Union[str, TaskPriority] = TaskPriority.NORMAL,
        max_retries: int = 3,
        timeout: int = 30,
        dependencies: List[str] = None,
    ) -> str:
        """创建点击任务"""
        if isinstance(priority, str):
            priority = TaskPriority[priority.upper()]

        task = Task(
            name=name or f"Click_{hwnd}_{x}_{y}",
            priority=priority,
            max_retries=max_retries,
            timeout=timeout,
            dependencies=dependencies or [],
        )

        click_task = ClickTask(task, hwnd, x, y, button)
        return self.task_manager.add_task(click_task)

    def create_image_recognition_task(
        self,
        hwnd: Union[int, str],
        template_path: str,
        threshold: float = 0.8,
        name: str = "",
        priority: Union[str, TaskPriority] = TaskPriority.NORMAL,
        max_retries: int = 3,
        timeout: int = 30,
        dependencies: List[str] = None,
    ) -> str:
        """创建图像识别任务"""
        if isinstance(priority, str):
            priority = TaskPriority[priority.upper()]

        task = Task(
            name=name or f"FindImage_{template_path}",
            priority=priority,
            max_retries=max_retries,
            timeout=timeout,
            dependencies=dependencies or [],
        )

        image_task = ImageRecognitionTask(task, hwnd, template_path, threshold)
        return self.task_manager.add_task(image_task)

    def create_custom_task(self, custom_task: BaseTask) -> str:
        """创建自定义任务"""
        return self.task_manager.add_task(custom_task)

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        return self.task_manager.cancel_task(task_id)

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """获取任务状态"""
        return self.task_manager.get_task_status(task_id)

    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """获取任务结果"""
        return self.task_manager.get_task_result(task_id)

    def wait_for_task(self, task_id: str, timeout: int = 60) -> Optional[TaskResult]:
        """等待任务完成"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = self.get_task_status(task_id)
            if status in [
                TaskStatus.COMPLETED,
                TaskStatus.FAILED,
                TaskStatus.CANCELLED,
            ]:
                return self.get_task_result(task_id)
            time.sleep(0.5)

        return None

    def get_task_statistics(self) -> Dict[str, Any]:
        """获取任务统计信息"""
        return self.task_manager.get_statistics()

    # 便捷方法
    def find_window_by_title_and_click(
        self,
        window_title: str,
        x: int,
        y: int,
        button: str = "left",
        exact_match: bool = False,
        use_task: bool = False,
    ) -> Union[bool, str]:
        """根据窗口标题查找窗口并点击"""
        windows = self.find_windows_by_title(window_title, exact_match)
        if not windows:
            self.logger.error(f"Window not found: {window_title}")
            return False

        hwnd = windows[0].hwnd

        if use_task:
            return self.create_click_task(hwnd, x, y, button)
        else:
            return self.click(hwnd, x, y, button)

    def find_window_by_title_and_click_image(
        self,
        window_title: str,
        template_path: str,
        threshold: float = 0.8,
        button: str = "left",
        exact_match: bool = False,
        use_task: bool = False,
    ) -> Union[bool, str]:
        """根据窗口标题查找窗口并点击图像"""
        windows = self.find_windows_by_title(window_title, exact_match)
        if not windows:
            self.logger.error(f"Window not found: {window_title}")
            return False

        hwnd = windows[0].hwnd

        if use_task:
            # 创建图像识别任务和点击任务的组合
            image_task_id = self.create_image_recognition_task(
                hwnd, template_path, threshold
            )

            # 等待图像识别完成
            image_result = self.wait_for_task(image_task_id, 30)
            if image_result and image_result.success:
                position = image_result.data["position"]
                return self.create_click_task(
                    hwnd, position["x"], position["y"], button
                )
            return False
        else:
            return self.click_image(hwnd, template_path, threshold, button)

    def batch_click(
        self, click_list: List[Dict[str, Any]], use_task: bool = False
    ) -> Union[List[bool], List[str]]:
        """批量点击"""
        results = []

        for click_info in click_list:
            hwnd = click_info["hwnd"]
            x = click_info["x"]
            y = click_info["y"]
            button = click_info.get("button", "left")

            if use_task:
                task_id = self.create_click_task(hwnd, x, y, button)
                results.append(task_id)
            else:
                success = self.click(hwnd, x, y, button)
                results.append(success)

                # 添加小延迟避免操作过快
                time.sleep(0.1)

        return results

    def chain_tasks(self, task_configs: List[Dict[str, Any]]) -> List[str]:
        """创建任务链（后续任务依赖前一个任务）"""
        task_ids = []

        for i, config in enumerate(task_configs):
            task_type = config["type"]
            dependencies = [task_ids[-1]] if i > 0 else []

            if task_type == "click":
                task_id = self.create_click_task(
                    hwnd=config["hwnd"],
                    x=config["x"],
                    y=config["y"],
                    button=config.get("button", "left"),
                    name=config.get("name", ""),
                    priority=config.get("priority", TaskPriority.NORMAL),
                    dependencies=dependencies,
                )
            elif task_type == "image":
                task_id = self.create_image_recognition_task(
                    hwnd=config["hwnd"],
                    template_path=config["template_path"],
                    threshold=config.get("threshold", 0.8),
                    name=config.get("name", ""),
                    priority=config.get("priority", TaskPriority.NORMAL),
                    dependencies=dependencies,
                )
            else:
                continue

            task_ids.append(task_id)

        return task_ids

    # 上下文管理器支持
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
