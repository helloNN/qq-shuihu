"""
跨平台自动化基础使用示例
演示如何使用自动化API进行基本操作
支持Windows、macOS、Linux
"""

import sys
import os
import time
import platform

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from main import AutomationAPI, TaskPriority
from config import ExecutionMode, ClickMode, ImageMode


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

        # 根据操作系统查找不同的应用窗口
        target_apps = []
        if platform.system() == "Windows":
            target_apps = ["记事本", "Notepad", "Calculator", "计算器"]
        elif platform.system() == "Darwin":  # macOS
            target_apps = ["TextEdit", "Calculator", "Terminal"]
        else:  # Linux
            target_apps = ["gedit", "Text Editor", "Calculator", "Terminal"]

        print("查找目标应用窗口...")
        window = None
        for app_name in target_apps:
            windows = api.find_windows_by_title(app_name)
            if windows:
                window = windows[0]
                print(f"找到窗口: {window.title} (句柄: {window.hwnd})")
                break

        if not window:
            print(f"未找到目标应用窗口，请先打开以下任一应用: {target_apps}")
            return

        # 将窗口置于前台
        print("将窗口置于前台...")
        api.bring_window_to_front(window.hwnd)
        time.sleep(1)

        # 点击窗口中心
        print("点击窗口中心...")
        center_x = (window.rect[2] - window.rect[0]) // 2
        center_y = (window.rect[3] - window.rect[1]) // 2
        api.click(window.hwnd, center_x, center_y)

        # 发送文本
        print("发送文本...")
        api.send_text(window.hwnd, "Hello, 跨平台自动化测试!")

        print("基础操作完成!")

    finally:
        # 停止自动化系统
        api.stop()


def task_system_example():
    """任务系统示例"""
    print("\n=== 跨平台任务系统示例 ===")

    api = AutomationAPI()

    try:
        api.start()
        api.set_execution_mode(ExecutionMode.THREAD)

        # 查找可用窗口
        window = find_available_window(api)
        if not window:
            print("未找到可用的应用窗口")
            return

        hwnd = window.hwnd

        # 创建点击任务
        print("创建点击任务...")
        task_id1 = api.create_click_task(
            hwnd=hwnd, x=100, y=100, name="点击任务1", priority=TaskPriority.HIGH
        )

        # 创建文本输入任务（这里用点击任务模拟）
        task_id2 = api.create_click_task(
            hwnd=hwnd,
            x=200,
            y=150,
            name="点击任务2",
            priority=TaskPriority.NORMAL,
            dependencies=[task_id1],  # 依赖第一个任务
        )

        print(f"任务1 ID: {task_id1}")
        print(f"任务2 ID: {task_id2}")

        # 等待任务完成
        print("等待任务完成...")
        result1 = api.wait_for_task(task_id1, timeout=30)
        result2 = api.wait_for_task(task_id2, timeout=30)

        print(f"任务1结果: {result1.success if result1 else 'Timeout'}")
        print(f"任务2结果: {result2.success if result2 else 'Timeout'}")

        # 获取统计信息
        stats = api.get_task_statistics()
        print(f"任务统计: {stats}")

    finally:
        api.stop()


def image_recognition_example():
    """图像识别示例"""
    print("\n=== 跨平台图像识别示例 ===")

    api = AutomationAPI()

    try:
        api.start()

        # 查找可用窗口进行截图测试
        window = find_available_window(api)
        if not window:
            print("未找到可用的应用窗口")
            return

        hwnd = window.hwnd

        # 截取窗口图像
        print("截取窗口图像...")
        image = api.capture_window(hwnd)

        if image is not None:
            print(f"成功截取图像，尺寸: {image.shape}")
        else:
            print("截取图像失败")

        # 注意：这里需要准备一个模板图像文件
        template_path = "template.png"
        if os.path.exists(template_path):
            print("查找模板图像...")
            result = api.find_image(hwnd, template_path, threshold=0.8)

            if result:
                print(
                    f"找到图像，位置: {result['position']}, 置信度: {result['confidence']}"
                )

                # 点击找到的图像
                api.click_image(hwnd, template_path, threshold=0.8)
                print("点击图像完成")
            else:
                print("未找到匹配的图像")
        else:
            print(f"模板图像文件不存在: {template_path}")

    finally:
        api.stop()


def batch_operations_example():
    """批量操作示例"""
    print("\n=== 跨平台批量操作示例 ===")

    api = AutomationAPI()

    try:
        api.start()

        # 查找可用窗口
        window = find_available_window(api)
        if not window:
            print("未找到可用的应用窗口")
            return

        hwnd = window.hwnd

        # 准备批量点击数据
        click_list = [
            {"hwnd": hwnd, "x": 50, "y": 50},
            {"hwnd": hwnd, "x": 100, "y": 100},
            {"hwnd": hwnd, "x": 150, "y": 150},
            {"hwnd": hwnd, "x": 200, "y": 200},
        ]

        # 同步批量点击
        print("执行同步批量点击...")
        results = api.batch_click(click_list, use_task=False)
        print(f"同步点击结果: {results}")

        time.sleep(2)

        # 异步批量点击
        print("执行异步批量点击...")
        task_ids = api.batch_click(click_list, use_task=True)
        print(f"任务IDs: {task_ids}")

        # 等待所有任务完成
        for task_id in task_ids:
            result = api.wait_for_task(task_id, timeout=30)
            print(f"任务 {task_id} 结果: {result.success if result else 'Timeout'}")

    finally:
        api.stop()


def task_chain_example():
    """任务链示例"""
    print("\n=== 跨平台任务链示例 ===")

    api = AutomationAPI()

    try:
        api.start()

        # 查找可用窗口
        window = find_available_window(api)
        if not window:
            print("未找到可用的应用窗口")
            return

        hwnd = window.hwnd

        # 定义任务链配置
        task_configs = [
            {"type": "click", "hwnd": hwnd, "x": 100, "y": 100, "name": "第一步点击"},
            {"type": "click", "hwnd": hwnd, "x": 200, "y": 150, "name": "第二步点击"},
            {"type": "click", "hwnd": hwnd, "x": 300, "y": 200, "name": "第三步点击"},
        ]

        # 创建任务链
        print("创建任务链...")
        task_ids = api.chain_tasks(task_configs)
        print(f"任务链IDs: {task_ids}")

        # 等待所有任务完成
        for i, task_id in enumerate(task_ids):
            print(f"等待任务 {i+1} 完成...")
            result = api.wait_for_task(task_id, timeout=30)
            print(f"任务 {i+1} 结果: {result.success if result else 'Timeout'}")

    finally:
        api.stop()


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


def context_manager_example():
    """上下文管理器示例"""
    print("\n=== 跨平台上下文管理器示例 ===")

    # 使用with语句自动管理API生命周期
    with AutomationAPI() as api:
        # 查找所有窗口
        windows = api.get_all_windows()
        print(f"找到 {len(windows)} 个窗口:")

        for window in windows[:5]:  # 只显示前5个
            print(f"  - {window.title} ({window.process_name}) - 句柄: {window.hwnd}")

        # 根据操作系统查找特定进程的窗口
        if platform.system() == "Windows":
            process_names = ["notepad.exe", "calc.exe"]
        elif platform.system() == "Darwin":  # macOS
            process_names = ["TextEdit", "Calculator"]
        else:  # Linux
            process_names = ["gedit", "gnome-calculator"]

        for process_name in process_names:
            process_windows = api.find_windows_by_process(process_name)
            if process_windows:
                print(f"\n找到 {len(process_windows)} 个 {process_name} 窗口")
                break
        else:
            print(f"\n未找到目标进程窗口: {process_names}")


if __name__ == "__main__":
    print("跨平台自动化示例程序")
    print(f"当前操作系统: {platform.system()}")
    print("请确保已安装所需依赖包:")
    print("  - pyautogui")
    print("  - pynput")
    print("  - pygetwindow")
    print("  - opencv-python")
    print("  - numpy")
    print("  - Pillow")
    print("  - psutil")
    print("-" * 50)

    try:
        # 运行各种示例
        basic_window_operations()
        task_system_example()
        image_recognition_example()
        batch_operations_example()
        task_chain_example()
        context_manager_example()

        print("\n所有示例执行完成!")

    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        import traceback

        traceback.print_exc()
