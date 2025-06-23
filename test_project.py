"""
项目测试脚本
用于验证项目代码的基本功能和正确性
"""

import sys
import os
import traceback

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_imports():
    """测试所有模块的导入"""
    print("=== 测试模块导入 ===")

    try:
        # 测试配置模块
        from config import config, ExecutionMode, ClickMode, ImageMode

        print("✓ config 模块导入成功")

        # 测试窗口管理器
        from window_manager import WindowManager, WindowInfo

        print("✓ window_manager 模块导入成功")

        # 测试自动化引擎
        from automation import AutomationEngine

        print("✓ automation 模块导入成功")

        # 测试任务系统
        from task_system import (
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

        print("✓ task_system 模块导入成功")

        # 测试主API
        from main import AutomationAPI, api

        print("✓ main 模块导入成功")

        return True

    except Exception as e:
        print(f"✗ 模块导入失败: {e}")
        traceback.print_exc()
        return False


def test_config():
    """测试配置系统"""
    print("\n=== 测试配置系统 ===")

    try:
        from config import config, ExecutionMode, ClickMode, ImageMode

        # 测试执行模式设置
        config.set_execution_mode(ExecutionMode.THREAD)
        assert config.execution_mode == ExecutionMode.THREAD
        print("✓ 线程模式设置成功")

        config.set_execution_mode(ExecutionMode.PROCESS)
        assert config.execution_mode == ExecutionMode.PROCESS
        print("✓ 进程模式设置成功")

        # 测试点击模式设置
        config.set_click_mode(ClickMode.FOREGROUND)
        assert config.click_mode == ClickMode.FOREGROUND
        print("✓ 前台点击模式设置成功")

        config.set_click_mode(ClickMode.BACKGROUND)
        assert config.click_mode == ClickMode.BACKGROUND
        print("✓ 后台点击模式设置成功")

        # 测试图像模式设置
        config.set_image_mode(ImageMode.FOREGROUND)
        assert config.image_mode == ImageMode.FOREGROUND
        print("✓ 前台图像模式设置成功")

        config.set_image_mode(ImageMode.BACKGROUND)
        assert config.image_mode == ImageMode.BACKGROUND
        print("✓ 后台图像模式设置成功")

        return True

    except Exception as e:
        print(f"✗ 配置系统测试失败: {e}")
        traceback.print_exc()
        return False


def test_window_manager():
    """测试窗口管理器"""
    print("\n=== 测试窗口管理器 ===")

    try:
        from window_manager import WindowManager

        manager = WindowManager()
        print("✓ WindowManager 实例创建成功")

        # 测试获取所有窗口
        windows = manager.get_all_windows()
        print(f"✓ 获取到 {len(windows)} 个窗口")

        # 测试查找特定窗口（这里不会报错，即使找不到）
        notepad_windows = manager.find_windows_by_title("记事本")
        print(f"✓ 查找记事本窗口: {len(notepad_windows)} 个")

        # 测试按进程查找
        explorer_windows = manager.find_windows_by_process("explorer.exe")
        print(f"✓ 查找资源管理器窗口: {len(explorer_windows)} 个")

        return True

    except Exception as e:
        print(f"✗ 窗口管理器测试失败: {e}")
        traceback.print_exc()
        return False


def test_task_system():
    """测试任务系统"""
    print("\n=== 测试任务系统 ===")

    try:
        from task_system import Task, TaskPriority, TaskStatus, TaskManager

        # 测试任务创建
        task = Task(
            name="测试任务", priority=TaskPriority.NORMAL, max_retries=3, timeout=30
        )
        print("✓ Task 实例创建成功")

        # 测试任务管理器
        manager = TaskManager()
        print("✓ TaskManager 实例创建成功")

        # 测试枚举
        assert TaskPriority.HIGH.value > TaskPriority.NORMAL.value
        print("✓ 任务优先级枚举正常")

        assert TaskStatus.PENDING.value == "pending"
        print("✓ 任务状态枚举正常")

        return True

    except Exception as e:
        print(f"✗ 任务系统测试失败: {e}")
        traceback.print_exc()
        return False


def test_automation_engine():
    """测试自动化引擎"""
    print("\n=== 测试自动化引擎 ===")

    try:
        from automation import AutomationEngine

        engine = AutomationEngine()
        print("✓ AutomationEngine 实例创建成功")

        # 测试无效窗口句柄（不会崩溃，只是返回False）
        result = engine.click(99999, 100, 100)
        print(f"✓ 无效句柄点击测试: {result}")

        return True

    except Exception as e:
        print(f"✗ 自动化引擎测试失败: {e}")
        traceback.print_exc()
        return False


def test_main_api():
    """测试主API"""
    print("\n=== 测试主API ===")

    try:
        from main import AutomationAPI

        api = AutomationAPI()
        print("✓ AutomationAPI 实例创建成功")

        # 测试配置方法
        api.set_execution_mode("thread")
        print("✓ 执行模式设置成功")

        api.set_click_mode("background")
        print("✓ 点击模式设置成功")

        api.set_image_mode("background")
        print("✓ 图像模式设置成功")

        # 测试窗口查找（不会报错）
        windows = api.find_windows_by_title("不存在的窗口")
        print(f"✓ 窗口查找测试: {len(windows)} 个")

        return True

    except Exception as e:
        print(f"✗ 主API测试失败: {e}")
        traceback.print_exc()
        return False


def test_convenience_functions():
    """测试便捷函数"""
    print("\n=== 测试便捷函数 ===")

    try:
        from main import (
            set_thread_mode,
            set_process_mode,
            set_foreground_mode,
            set_background_mode,
            find_window,
        )

        # 测试模式设置函数
        set_thread_mode()
        print("✓ set_thread_mode() 执行成功")

        set_process_mode()
        print("✓ set_process_mode() 执行成功")

        set_foreground_mode()
        print("✓ set_foreground_mode() 执行成功")

        set_background_mode()
        print("✓ set_background_mode() 执行成功")

        # 测试窗口查找函数
        window = find_window("不存在的窗口")
        print(f"✓ find_window() 执行成功: {window}")

        return True

    except Exception as e:
        print(f"✗ 便捷函数测试失败: {e}")
        traceback.print_exc()
        return False


def test_example_imports():
    """测试示例代码的导入"""
    print("\n=== 测试示例代码导入 ===")

    try:
        # 测试基础示例
        sys.path.append(os.path.join(os.path.dirname(__file__), "examples"))

        # 不直接运行示例，只测试导入
        import importlib.util

        # 测试基础示例导入
        basic_spec = importlib.util.spec_from_file_location(
            "basic_example",
            os.path.join(os.path.dirname(__file__), "examples", "basic_example.py"),
        )
        basic_module = importlib.util.module_from_spec(basic_spec)
        basic_spec.loader.exec_module(basic_module)
        print("✓ basic_example.py 导入成功")

        # 测试高级示例导入
        advanced_spec = importlib.util.spec_from_file_location(
            "advanced_example",
            os.path.join(os.path.dirname(__file__), "examples", "advanced_example.py"),
        )
        advanced_module = importlib.util.module_from_spec(advanced_spec)
        advanced_spec.loader.exec_module(advanced_module)
        print("✓ advanced_example.py 导入成功")

        return True

    except Exception as e:
        print(f"✗ 示例代码导入失败: {e}")
        traceback.print_exc()
        return False


def test_dependencies():
    """测试依赖包"""
    print("\n=== 测试依赖包 ===")

    required_packages = [
        "win32api",
        "win32gui",
        "win32con",
        "win32process",
        "cv2",
        "numpy",
        "PIL",
        "psutil",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} 可用")
        except ImportError:
            print(f"✗ {package} 缺失")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n缺失的包: {missing_packages}")
        print("请运行: pip install -r requirements.txt")
        return False

    return True


def run_all_tests():
    """运行所有测试"""
    print("开始项目代码验证测试...\n")

    tests = [
        ("依赖包检查", test_dependencies),
        ("模块导入", test_imports),
        ("配置系统", test_config),
        ("窗口管理器", test_window_manager),
        ("任务系统", test_task_system),
        ("自动化引擎", test_automation_engine),
        ("主API", test_main_api),
        ("便捷函数", test_convenience_functions),
        ("示例代码", test_example_imports),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"运行测试: {test_name}")
        print("=" * 50)

        try:
            if test_func():
                passed += 1
                print(f"\n✓ {test_name} 测试通过")
            else:
                print(f"\n✗ {test_name} 测试失败")
        except Exception as e:
            print(f"\n✗ {test_name} 测试异常: {e}")
            traceback.print_exc()

    print(f"\n{'='*60}")
    print(f"测试结果: {passed}/{total} 通过")
    print("=" * 60)

    if passed == total:
        print("🎉 所有测试通过！项目代码验证成功！")
        return True
    else:
        print("❌ 部分测试失败，请检查上述错误信息")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
