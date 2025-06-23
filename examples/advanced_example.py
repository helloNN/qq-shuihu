"""
跨平台高级使用示例
演示复杂的自动化场景和自定义任务
支持Windows、macOS、Linux
"""

import sys
import os
import time
import threading
import platform
from typing import Dict, Any, Union

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from main import AutomationAPI, TaskPriority
from config import ExecutionMode, ClickMode, ImageMode
from task_system import BaseTask, Task, TaskResult
from automation import CrossPlatformAutomationEngine


class CustomTextInputTask(BaseTask):
    """自定义文本输入任务"""

    def __init__(
        self, task: Task, hwnd: Union[int, str], text: str, delay: float = 0.05
    ):
        super().__init__(task)
        self.hwnd = hwnd
        self.text = text
        self.delay = delay

    def execute(self) -> TaskResult:
        """执行文本输入"""
        start_time = time.time()

        try:
            if self.is_cancelled():
                return TaskResult(success=False, error="Task cancelled")

            engine = CrossPlatformAutomationEngine()

            # 逐字符输入文本，支持取消
            for i, char in enumerate(self.text):
                if self.is_cancelled():
                    return TaskResult(
                        success=False,
                        error="Task cancelled during execution",
                        data={"chars_typed": i},
                    )

                success = engine.send_text(self.hwnd, char)
                if not success:
                    return TaskResult(
                        success=False,
                        error=f"Failed to send character: {char}",
                        data={"chars_typed": i},
                    )

                time.sleep(self.delay)

            execution_time = time.time() - start_time
            return TaskResult(
                success=True,
                data={"text": self.text, "chars_typed": len(self.text)},
                execution_time=execution_time,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                success=False, error=str(e), execution_time=execution_time
            )


class CustomWaitTask(BaseTask):
    """自定义等待任务"""

    def __init__(self, task: Task, wait_seconds: float):
        super().__init__(task)
        self.wait_seconds = wait_seconds

    def execute(self) -> TaskResult:
        """执行等待"""
        start_time = time.time()

        try:
            # 可中断的等待
            elapsed = 0
            while elapsed < self.wait_seconds:
                if self.is_cancelled():
                    return TaskResult(
                        success=False,
                        error="Task cancelled",
                        data={"waited_seconds": elapsed},
                    )

                time.sleep(0.1)
                elapsed = time.time() - start_time

            return TaskResult(
                success=True,
                data={"waited_seconds": self.wait_seconds},
                execution_time=elapsed,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                success=False, error=str(e), execution_time=execution_time
            )


class CustomScreenshotTask(BaseTask):
    """自定义截图任务"""

    def __init__(self, task: Task, hwnd: Union[int, str], save_path: str):
        super().__init__(task)
        self.hwnd = hwnd
        self.save_path = save_path

    def execute(self) -> TaskResult:
        """执行截图"""
        start_time = time.time()

        try:
            if self.is_cancelled():
                return TaskResult(success=False, error="Task cancelled")

            import cv2

            engine = CrossPlatformAutomationEngine()

            # 截取窗口图像
            image = engine.capture_window(self.hwnd)
            if image is None:
                return TaskResult(success=False, error="Failed to capture window")

            # 保存图像
            success = cv2.imwrite(self.save_path, image)
            if not success:
                return TaskResult(
                    success=False, error=f"Failed to save image to {self.save_path}"
                )

            execution_time = time.time() - start_time
            return TaskResult(
                success=True,
                data={"save_path": self.save_path, "image_shape": image.shape},
                execution_time=execution_time,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                success=False, error=str(e), execution_time=execution_time
            )


def find_available_window(api):
    """查找可用的应用窗口"""
    target_apps = []
    if platform.system() == "Windows":
        target_apps = ["记事本", "Notepad", "Calculator", "计算器"]
    elif platform.system() == "Darwin":  # macOS
        target_apps = ["TextEdit", "Calculator", "Terminal"]
    else:  # Linux
        target_apps = ["gedit", "Text Editor", "Calculator", "Terminal"]

    for app_name in target_apps:
        windows = api.find_windows_by_title(app_name)
        if windows:
            return windows[0]
    return None


def custom_task_example():
    """自定义任务示例"""
    print("=== 跨平台自定义任务示例 ===")
    print(f"当前操作系统: {platform.system()}")

    api = AutomationAPI()

    try:
        api.start()

        # 查找可用窗口
        window = find_available_window(api)
        if not window:
            print("未找到可用的应用窗口，请先打开文本编辑器或计算器")
            return

        hwnd = window.hwnd
        print(f"使用窗口: {window.title}")

        # 创建自定义文本输入任务
        text_task = Task(
            name="自定义文本输入", priority=TaskPriority.HIGH, max_retries=2
        )
        custom_text_task = CustomTextInputTask(
            text_task, hwnd, "这是自定义任务输入的文本！", 0.1
        )

        # 创建自定义等待任务
        wait_task = Task(name="自定义等待", priority=TaskPriority.NORMAL)
        custom_wait_task = CustomWaitTask(wait_task, 2.0)

        # 创建自定义截图任务
        screenshot_task = Task(name="自定义截图", priority=TaskPriority.LOW)
        custom_screenshot_task = CustomScreenshotTask(
            screenshot_task, hwnd, "screenshot.png"
        )

        # 添加任务到管理器
        text_task_id = api.create_custom_task(custom_text_task)
        wait_task_id = api.create_custom_task(custom_wait_task)
        screenshot_task_id = api.create_custom_task(custom_screenshot_task)

        print(f"文本任务ID: {text_task_id}")
        print(f"等待任务ID: {wait_task_id}")
        print(f"截图任务ID: {screenshot_task_id}")

        # 等待任务完成
        results = {}
        for task_id, name in [
            (text_task_id, "文本"),
            (wait_task_id, "等待"),
            (screenshot_task_id, "截图"),
        ]:
            result = api.wait_for_task(task_id, timeout=30)
            results[name] = result
            print(f"{name}任务结果: {result.success if result else 'Timeout'}")
            if result and result.data:
                print(f"  数据: {result.data}")

        return results

    finally:
        api.stop()


def multi_window_automation():
    """多窗口自动化示例"""
    print("\n=== 跨平台多窗口自动化示例 ===")

    api = AutomationAPI()

    try:
        api.start()
        api.set_execution_mode(ExecutionMode.THREAD)

        # 根据操作系统查找多个窗口
        target_process = ""
        if platform.system() == "Windows":
            target_process = "notepad.exe"
            target_name = "记事本"
        elif platform.system() == "Darwin":  # macOS
            target_process = "TextEdit"
            target_name = "TextEdit"
        else:  # Linux
            target_process = "gedit"
            target_name = "gedit"

        app_windows = api.find_windows_by_process(target_process)
        if len(app_windows) < 2:
            print(f"需要至少2个{target_name}窗口，请多开几个{target_name}")
            return

        print(f"找到 {len(app_windows)} 个{target_name}窗口")

        # 为每个窗口创建任务
        task_ids = []
        for i, window in enumerate(app_windows[:3]):  # 最多处理3个窗口
            # 点击任务
            click_task_id = api.create_click_task(
                hwnd=window.hwnd,
                x=100,
                y=100,
                name=f"窗口{i+1}_点击",
                priority=TaskPriority.NORMAL,
            )
            task_ids.append(click_task_id)

            # 文本输入任务
            text_task = Task(
                name=f"窗口{i+1}_文本输入",
                priority=TaskPriority.NORMAL,
                dependencies=[click_task_id],
            )
            custom_text_task = CustomTextInputTask(
                text_task, window.hwnd, f"这是窗口{i+1}的自动化文本输入！\n"
            )
            text_task_id = api.create_custom_task(custom_text_task)
            task_ids.append(text_task_id)

        print(f"创建了 {len(task_ids)} 个任务")

        # 等待所有任务完成
        completed_count = 0
        for task_id in task_ids:
            result = api.wait_for_task(task_id, timeout=30)
            if result and result.success:
                completed_count += 1

        print(f"完成了 {completed_count}/{len(task_ids)} 个任务")

        # 获取统计信息
        stats = api.get_task_statistics()
        print(f"任务统计: {stats}")

    finally:
        api.stop()


def performance_test():
    """性能测试示例"""
    print("\n=== 跨平台性能测试示例 ===")

    api = AutomationAPI()

    try:
        api.start()

        # 查找可用窗口
        window = find_available_window(api)
        if not window:
            print("未找到可用的应用窗口")
            return

        hwnd = window.hwnd

        # 测试大量任务的处理性能
        task_count = 50
        print(f"创建 {task_count} 个任务进行性能测试...")

        start_time = time.time()
        task_ids = []

        # 创建大量点击任务
        for i in range(task_count):
            x = 50 + (i % 10) * 20
            y = 50 + (i // 10) * 20

            task_id = api.create_click_task(
                hwnd=hwnd,
                x=x,
                y=y,
                name=f"性能测试任务_{i}",
                priority=TaskPriority.NORMAL if i % 2 == 0 else TaskPriority.LOW,
            )
            task_ids.append(task_id)

        creation_time = time.time() - start_time
        print(f"任务创建耗时: {creation_time:.2f}秒")

        # 等待所有任务完成
        print("等待任务完成...")
        completion_start = time.time()

        completed_tasks = 0
        failed_tasks = 0

        for task_id in task_ids:
            result = api.wait_for_task(task_id, timeout=60)
            if result:
                if result.success:
                    completed_tasks += 1
                else:
                    failed_tasks += 1
            else:
                failed_tasks += 1

        completion_time = time.time() - completion_start
        total_time = time.time() - start_time

        print(f"任务执行耗时: {completion_time:.2f}秒")
        print(f"总耗时: {total_time:.2f}秒")
        print(f"成功任务: {completed_tasks}")
        print(f"失败任务: {failed_tasks}")
        print(f"平均每任务耗时: {total_time/task_count:.3f}秒")

        # 获取最终统计
        final_stats = api.get_task_statistics()
        print(f"最终统计: {final_stats}")

    finally:
        api.stop()


def error_handling_example():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")

    api = AutomationAPI()

    try:
        api.start()

        # 测试无效窗口句柄
        print("测试无效窗口句柄...")
        invalid_hwnd = 99999
        result = api.click(invalid_hwnd, 100, 100)
        print(f"无效窗口句柄点击结果: {result}")

        # 测试任务取消
        print("测试任务取消...")
        wait_task = Task(name="长时间等待任务", priority=TaskPriority.NORMAL)
        long_wait_task = CustomWaitTask(wait_task, 10.0)  # 等待10秒

        task_id = api.create_custom_task(long_wait_task)
        print(f"创建长时间任务: {task_id}")

        # 等待2秒后取消任务
        time.sleep(2)
        cancel_result = api.cancel_task(task_id)
        print(f"任务取消结果: {cancel_result}")

        # 检查任务状态
        status = api.get_task_status(task_id)
        print(f"任务状态: {status}")

        # 测试任务重试
        print("测试任务重试...")

        # 创建一个会失败的任务（点击无效窗口）
        retry_task_id = api.create_click_task(
            hwnd=invalid_hwnd, x=100, y=100, name="重试测试任务", max_retries=3
        )

        result = api.wait_for_task(retry_task_id, timeout=30)
        print(f"重试任务结果: {result.success if result else 'Timeout'}")
        if result:
            print(f"重试次数: {result.retry_count}")

    finally:
        api.stop()


def real_world_scenario():
    """真实世界场景示例：自动化填写表单"""
    print("\n=== 跨平台真实场景示例：自动化填写表单 ===")

    api = AutomationAPI()

    try:
        api.start()
        api.set_click_mode(ClickMode.FOREGROUND)  # 跨平台兼容性更好

        # 查找可用窗口（模拟表单窗口）
        window = find_available_window(api)
        if not window:
            print("未找到可用的应用窗口，请先打开文本编辑器")
            return

        hwnd = window.hwnd
        print(f"使用窗口模拟表单: {window.title}")

        # 模拟表单填写流程
        form_data = {
            "name": "张三",
            "age": "25",
            "email": "zhangsan@example.com",
            "address": "北京市朝阳区某某街道123号",
        }

        # 创建表单填写任务链
        task_configs = []

        # 1. 点击姓名字段
        task_configs.append(
            {"type": "click", "hwnd": hwnd, "x": 100, "y": 50, "name": "点击姓名字段"}
        )

        # 2. 输入姓名
        name_task = Task(name="输入姓名", priority=TaskPriority.NORMAL)
        name_input_task = CustomTextInputTask(
            name_task, hwnd, f"姓名: {form_data['name']}\n"
        )

        # 3. 点击年龄字段
        task_configs.append(
            {"type": "click", "hwnd": hwnd, "x": 100, "y": 100, "name": "点击年龄字段"}
        )

        # 4. 输入年龄
        age_task = Task(name="输入年龄", priority=TaskPriority.NORMAL)
        age_input_task = CustomTextInputTask(
            age_task, hwnd, f"年龄: {form_data['age']}\n"
        )

        # 5. 点击邮箱字段
        task_configs.append(
            {"type": "click", "hwnd": hwnd, "x": 100, "y": 150, "name": "点击邮箱字段"}
        )

        # 6. 输入邮箱
        email_task = Task(name="输入邮箱", priority=TaskPriority.NORMAL)
        email_input_task = CustomTextInputTask(
            email_task, hwnd, f"邮箱: {form_data['email']}\n"
        )

        # 7. 点击地址字段
        task_configs.append(
            {"type": "click", "hwnd": hwnd, "x": 100, "y": 200, "name": "点击地址字段"}
        )

        # 8. 输入地址
        address_task = Task(name="输入地址", priority=TaskPriority.NORMAL)
        address_input_task = CustomTextInputTask(
            address_task, hwnd, f"地址: {form_data['address']}\n"
        )

        # 执行任务链
        print("开始执行表单填写任务...")

        # 创建点击任务链
        click_task_ids = api.chain_tasks(task_configs)

        # 手动添加文本输入任务并设置依赖关系
        text_tasks = [
            (name_input_task, 0),  # 依赖第1个点击任务
            (age_input_task, 2),  # 依赖第3个点击任务
            (email_input_task, 4),  # 依赖第5个点击任务
            (address_input_task, 6),  # 依赖第7个点击任务
        ]

        text_task_ids = []
        for text_task_obj, click_index in text_tasks:
            if click_index < len(click_task_ids):
                text_task_obj.task.dependencies = [click_task_ids[click_index]]
            text_task_id = api.create_custom_task(text_task_obj)
            text_task_ids.append(text_task_id)

        all_task_ids = click_task_ids + text_task_ids

        # 等待所有任务完成
        print("等待任务完成...")
        completed = 0
        for i, task_id in enumerate(all_task_ids):
            result = api.wait_for_task(task_id, timeout=60)
            if result and result.success:
                completed += 1
                print(f"任务 {i+1} 完成")
            else:
                print(f"任务 {i+1} 失败")

        print(f"表单填写完成！成功执行 {completed}/{len(all_task_ids)} 个任务")

    finally:
        api.stop()


if __name__ == "__main__":
    print("跨平台自动化高级示例程序")
    print(f"当前操作系统: {platform.system()}")
    print("请确保已安装所需依赖包并打开相应的应用程序")
    print("=" * 50)

    try:
        # 运行高级示例
        custom_task_example()
        multi_window_automation()
        performance_test()
        error_handling_example()
        real_world_scenario()

        print("\n所有高级示例执行完成!")

    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback

        traceback.print_exc()
