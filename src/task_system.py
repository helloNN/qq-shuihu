"""
任务系统模块
实现类似React的任务管理：优先级、取消、重试等功能
"""

import time
import threading
import multiprocessing
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Callable, List, Union
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future
import uuid
import queue
import logging

from .config import config, ExecutionMode


class TaskPriority(Enum):
    """任务优先级"""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4


class TaskStatus(Enum):
    """任务状态"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


@dataclass
class TaskResult:
    """任务结果"""

    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    retry_count: int = 0


@dataclass
class Task:
    """任务基类"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    timeout: int = 30
    retry_count: int = 0
    max_retries: int = 3
    retry_delay: float = 1.0
    result: Optional[TaskResult] = None
    cancel_event: Optional[threading.Event] = field(default_factory=threading.Event)
    dependencies: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            self.name = f"Task_{self.id[:8]}"


class BaseTask(ABC):
    """任务基础抽象类"""

    def __init__(self, task: Task):
        self.task = task

    @abstractmethod
    def execute(self) -> TaskResult:
        """执行任务的抽象方法"""
        pass

    def is_cancelled(self) -> bool:
        """检查任务是否被取消"""
        return self.task.cancel_event and self.task.cancel_event.is_set()

    def cancel(self):
        """取消任务"""
        if self.task.cancel_event:
            self.task.cancel_event.set()
            self.task.status = TaskStatus.CANCELLED


class ClickTask(BaseTask):
    """点击任务"""

    def __init__(
        self, task: Task, hwnd: Union[int, str], x: int, y: int, button: str = "left"
    ):
        super().__init__(task)
        self.hwnd = hwnd
        self.x = x
        self.y = y
        self.button = button

    def execute(self) -> TaskResult:
        """执行点击任务"""
        start_time = time.time()

        try:
            if self.is_cancelled():
                return TaskResult(success=False, error="Task cancelled")

            from .automation import CrossPlatformAutomationEngine

            engine = CrossPlatformAutomationEngine()

            success = engine.click(self.hwnd, self.x, self.y, self.button)

            execution_time = time.time() - start_time

            if success:
                return TaskResult(
                    success=True,
                    data={"hwnd": self.hwnd, "x": self.x, "y": self.y},
                    execution_time=execution_time,
                )
            else:
                return TaskResult(
                    success=False,
                    error="Click operation failed",
                    execution_time=execution_time,
                )

        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                success=False, error=str(e), execution_time=execution_time
            )


class ImageRecognitionTask(BaseTask):
    """图像识别任务"""

    def __init__(
        self,
        task: Task,
        hwnd: Union[int, str],
        template_path: str,
        threshold: float = 0.8,
    ):
        super().__init__(task)
        self.hwnd = hwnd
        self.template_path = template_path
        self.threshold = threshold

    def execute(self) -> TaskResult:
        """执行图像识别任务"""
        start_time = time.time()

        try:
            if self.is_cancelled():
                return TaskResult(success=False, error="Task cancelled")

            from .automation import CrossPlatformAutomationEngine

            engine = CrossPlatformAutomationEngine()

            result = engine.find_image(self.hwnd, self.template_path, self.threshold)

            execution_time = time.time() - start_time

            if result:
                return TaskResult(
                    success=True, data=result, execution_time=execution_time
                )
            else:
                return TaskResult(
                    success=False,
                    error="Image not found",
                    execution_time=execution_time,
                )

        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                success=False, error=str(e), execution_time=execution_time
            )


class TaskManager:
    """任务管理器"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_objects: Dict[str, BaseTask] = {}
        self.task_queue = queue.PriorityQueue()
        self.running_tasks: Dict[str, Future] = {}
        self.completed_tasks: Dict[str, Task] = {}
        self.executor = None
        self.is_running = False
        self.worker_thread = None
        self.lock = threading.Lock()

        # 根据配置选择执行器
        self._setup_executor()

    def _setup_executor(self):
        """根据配置设置执行器"""
        if config.execution_mode == ExecutionMode.THREAD:
            self.executor = ThreadPoolExecutor(max_workers=config.max_workers)
        else:
            self.executor = ProcessPoolExecutor(max_workers=config.max_workers)

    def add_task(self, task_obj: BaseTask) -> str:
        """添加任务"""
        with self.lock:
            task = task_obj.task
            self.tasks[task.id] = task
            self.task_objects[task.id] = task_obj

            # 将任务添加到优先级队列
            priority_value = -task.priority.value  # 负值用于优先级队列的排序
            self.task_queue.put((priority_value, task.created_at, task.id))

            logging.info(f"Task {task.name} ({task.id}) added to queue")

        return task.id

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        with self.lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task_obj = self.task_objects.get(task_id)

                if task_obj:
                    task_obj.cancel()

                # 如果任务正在运行，尝试取消Future
                if task_id in self.running_tasks:
                    future = self.running_tasks[task_id]
                    future.cancel()

                task.status = TaskStatus.CANCELLED
                logging.info(f"Task {task.name} ({task.id}) cancelled")
                return True

        return False

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """获取任务状态"""
        with self.lock:
            if task_id in self.tasks:
                return self.tasks[task_id].status
            elif task_id in self.completed_tasks:
                return self.completed_tasks[task_id].status
        return None

    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """获取任务结果"""
        with self.lock:
            if task_id in self.tasks:
                return self.tasks[task_id].result
            elif task_id in self.completed_tasks:
                return self.completed_tasks[task_id].result
        return None

    def start(self):
        """启动任务管理器"""
        if self.is_running:
            return

        self.is_running = True
        self.worker_thread = threading.Thread(target=self._worker_loop)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        logging.info("TaskManager started")

    def stop(self):
        """停止任务管理器"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join()

        if self.executor:
            self.executor.shutdown(wait=True)

        logging.info("TaskManager stopped")

    def _worker_loop(self):
        """工作线程循环"""
        while self.is_running:
            try:
                # 从队列获取任务
                try:
                    priority, created_at, task_id = self.task_queue.get(timeout=1.0)
                except queue.Empty:
                    continue

                with self.lock:
                    if task_id not in self.tasks:
                        continue

                    task = self.tasks[task_id]
                    task_obj = self.task_objects[task_id]

                    # 检查任务是否已被取消
                    if task.status == TaskStatus.CANCELLED:
                        continue

                    # 检查依赖任务是否完成
                    if not self._check_dependencies(task):
                        # 重新放入队列等待
                        self.task_queue.put((priority, created_at, task_id))
                        continue

                    # 提交任务执行
                    task.status = TaskStatus.RUNNING
                    task.started_at = time.time()

                    future = self.executor.submit(self._execute_task, task_obj)
                    self.running_tasks[task_id] = future

                # 处理任务完成
                self._handle_task_completion(task_id, future)

            except Exception as e:
                logging.error(f"Error in worker loop: {e}")

    def _check_dependencies(self, task: Task) -> bool:
        """检查任务依赖是否满足"""
        for dep_id in task.dependencies:
            if dep_id in self.tasks:
                dep_task = self.tasks[dep_id]
                if dep_task.status != TaskStatus.COMPLETED:
                    return False
            elif dep_id in self.completed_tasks:
                dep_task = self.completed_tasks[dep_id]
                if dep_task.status != TaskStatus.COMPLETED:
                    return False
            else:
                return False  # 依赖任务不存在
        return True

    def _execute_task(self, task_obj: BaseTask) -> TaskResult:
        """执行任务"""
        try:
            return task_obj.execute()
        except Exception as e:
            return TaskResult(success=False, error=str(e))

    def _handle_task_completion(self, task_id: str, future: Future):
        """处理任务完成"""
        try:
            result = future.result(timeout=config.task_timeout)

            with self.lock:
                if task_id not in self.tasks:
                    return

                task = self.tasks[task_id]
                task.result = result
                task.completed_at = time.time()

                if result.success:
                    task.status = TaskStatus.COMPLETED
                    logging.info(f"Task {task.name} ({task.id}) completed successfully")
                else:
                    # 检查是否需要重试
                    if task.retry_count < task.max_retries:
                        task.retry_count += 1
                        task.status = TaskStatus.RETRYING

                        # 延迟后重新加入队列
                        def retry_task():
                            time.sleep(task.retry_delay)
                            priority_value = -task.priority.value
                            self.task_queue.put((priority_value, time.time(), task_id))

                        threading.Thread(target=retry_task, daemon=True).start()
                        logging.info(
                            f"Task {task.name} ({task.id}) will retry ({task.retry_count}/{task.max_retries})"
                        )
                        return
                    else:
                        task.status = TaskStatus.FAILED
                        logging.error(
                            f"Task {task.name} ({task.id}) failed: {result.error}"
                        )

                # 移动到完成任务列表
                self.completed_tasks[task_id] = self.tasks.pop(task_id)
                self.task_objects.pop(task_id, None)
                self.running_tasks.pop(task_id, None)

        except Exception as e:
            with self.lock:
                if task_id in self.tasks:
                    task = self.tasks[task_id]
                    task.status = TaskStatus.FAILED
                    task.result = TaskResult(success=False, error=str(e))
                    task.completed_at = time.time()

                    self.completed_tasks[task_id] = self.tasks.pop(task_id)
                    self.task_objects.pop(task_id, None)
                    self.running_tasks.pop(task_id, None)

            logging.error(f"Task {task_id} execution error: {e}")

    def get_statistics(self) -> Dict[str, Any]:
        """获取任务统计信息"""
        with self.lock:
            pending_count = len(
                [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
            )
            running_count = len(
                [t for t in self.tasks.values() if t.status == TaskStatus.RUNNING]
            )
            completed_count = len(
                [
                    t
                    for t in self.completed_tasks.values()
                    if t.status == TaskStatus.COMPLETED
                ]
            )
            failed_count = len(
                [
                    t
                    for t in self.completed_tasks.values()
                    if t.status == TaskStatus.FAILED
                ]
            )
            cancelled_count = len(
                [
                    t
                    for t in self.completed_tasks.values()
                    if t.status == TaskStatus.CANCELLED
                ]
            )

            return {
                "pending": pending_count,
                "running": running_count,
                "completed": completed_count,
                "failed": failed_count,
                "cancelled": cancelled_count,
                "total": pending_count
                + running_count
                + completed_count
                + failed_count
                + cancelled_count,
            }


# 全局任务管理器实例
task_manager = TaskManager()
