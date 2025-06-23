#!/usr/bin/env python3
"""
跨平台功能测试脚本
验证项目在不同操作系统上的兼容性
"""

import sys
import os
import platform
import time
import traceback

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    # 尝试直接导入
    try:
        from src.main import AutomationAPI, TaskPriority
        from src.config import ExecutionMode, ClickMode, ImageMode
        from src.window_manager import CrossPlatformWindowManager, WindowInfo
        from src.automation import CrossPlatformAutomationEngine
    except ImportError:
        # 如果失败，尝试不带src前缀的导入
        from main import AutomationAPI, TaskPriority
        from config import ExecutionMode, ClickMode, ImageMode
        from window_manager import CrossPlatformWindowManager, WindowInfo
        from automation import CrossPlatformAutomationEngine
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖包已正确安装")
    print("请确保在项目根目录下运行此脚本")
    sys.exit(1)


def print_system_info():
    """打印系统信息"""
    print("=" * 60)
    print("跨平台自动化系统测试")
    print("=" * 60)
    print(f"操作系统: {platform.system()}")
    print(f"系统版本: {platform.platform()}")
    print(f"Python版本: {platform.python_version()}")
    print(f"架构: {platform.machine()}")
    print("-" * 60)


def test_imports():
    """测试模块导入"""
    print("测试模块导入...")

    try:
        # 测试核心模块
        try:
            from src.main import AutomationAPI
            from src.config import config
            from src.window_manager import CrossPlatformWindowManager
            from src.automation import CrossPlatformAutomationEngine
            from src.task_system import TaskManager
        except ImportError:
            from main import AutomationAPI
            from config import config
            from window_manager import CrossPlatformWindowManager
            from automation import CrossPlatformAutomationEngine
            from task_system import TaskManager

        print("✓ 核心模块导入成功")

        # 测试依赖包
        import pyautogui
        import pynput
        import pygetwindow
        import cv2
        import numpy
        import PIL
        import psutil

        print("✓ 依赖包导入成功")
        return True

    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False


def test_window_manager():
    """测试窗口管理器"""
    print("\n测试窗口管理器...")

    try:
        wm = CrossPlatformWindowManager()

        # 测试获取所有窗口
        windows = wm.get_all_windows(include_hidden=False)
        print(f"✓ 找到 {len(windows)} 个可见窗口")

        if windows:
            # 显示前5个窗口信息
            print("前5个窗口:")
            for i, window in enumerate(windows[:5]):
                print(
                    f"  {i+1}. {window.title} (PID: {window.pid}, 进程: {window.process_name})"
                )

        # 测试活动窗口
        active_window = wm.get_active_window()
        if active_window:
            print(f"✓ 当前活动窗口: {active_window.title}")
        else:
            print("! 无法获取活动窗口")

        return True

    except Exception as e:
        print(f"✗ 窗口管理器测试失败: {e}")
        traceback.print_exc()
        return False


def test_automation_engine():
    """测试自动化引擎"""
    print("\n测试自动化引擎...")

    try:
        engine = CrossPlatformAutomationEngine()

        # 测试屏幕截图
        screenshot = engine.capture_screen()
        if screenshot is not None:
            print(f"✓ 屏幕截图成功，尺寸: {screenshot.shape}")
        else:
            print("! 屏幕截图失败")

        # 测试窗口截图（如果有窗口）
        wm = CrossPlatformWindowManager()
        windows = wm.get_all_windows()

        if windows:
            window = windows[0]
            window_screenshot = engine.capture_window(window.hwnd)
            if window_screenshot is not None:
                print(f"✓ 窗口截图成功，尺寸: {window_screenshot.shape}")
            else:
                print("! 窗口截图失败")

        return True

    except Exception as e:
        print(f"✗ 自动化引擎测试失败: {e}")
        traceback.print_exc()
        return False


def test_api_basic():
    """测试基础API功能"""
    print("\n测试基础API功能...")

    try:
        api = AutomationAPI()

        # 测试启动和停止
        api.start()
        print("✓ API启动成功")

        # 测试配置设置
        api.set_execution_mode(ExecutionMode.THREAD)
        api.set_click_mode(ClickMode.FOREGROUND)
        api.set_image_mode(ImageMode.FOREGROUND)
        print("✓ 配置设置成功")

        # 测试窗口查找
        windows = api.get_all_windows()
        print(f"✓ 找到 {len(windows)} 个窗口")

        # 测试任务统计
        stats = api.get_task_statistics()
        print(f"✓ 任务统计: {stats}")

        api.stop()
        print("✓ API停止成功")

        return True

    except Exception as e:
        print(f"✗ 基础API测试失败: {e}")
        traceback.print_exc()
        return False


def test_platform_specific():
    """测试平台特定功能"""
    print("\n测试平台特定功能...")

    system = platform.system()

    try:
        api = AutomationAPI()
        api.start()

        # 根据平台测试不同的应用
        target_apps = []
        if system == "Windows":
            target_apps = ["记事本", "Notepad", "Calculator", "计算器"]
        elif system == "Darwin":  # macOS
            target_apps = ["TextEdit", "Calculator", "Terminal", "Finder"]
        else:  # Linux
            target_apps = ["gedit", "Text Editor", "Calculator", "Terminal"]

        found_apps = []
        for app_name in target_apps:
            windows = api.find_windows_by_title(app_name)
            if windows:
                found_apps.append(app_name)

        if found_apps:
            print(f"✓ 找到平台应用: {found_apps}")
        else:
            print(f"! 未找到目标应用，请打开以下任一应用: {target_apps}")

        api.stop()
        return True

    except Exception as e:
        print(f"✗ 平台特定测试失败: {e}")
        traceback.print_exc()
        return False


def test_task_system():
    """测试任务系统"""
    print("\n测试任务系统...")

    try:
        api = AutomationAPI()
        api.start()

        # 获取一个可用窗口
        windows = api.get_all_windows()
        if not windows:
            print("! 没有可用窗口，跳过任务系统测试")
            api.stop()
            return True

        hwnd = windows[0].hwnd

        # 创建一个简单的点击任务
        task_id = api.create_click_task(
            hwnd=hwnd,
            x=10,  # 使用安全的坐标
            y=10,
            name="测试点击任务",
            priority=TaskPriority.NORMAL,
        )

        print(f"✓ 创建任务: {task_id}")

        # 等待任务完成
        result = api.wait_for_task(task_id, timeout=10)
        if result:
            print(f"✓ 任务完成，成功: {result.success}")
        else:
            print("! 任务超时")

        # 获取统计信息
        stats = api.get_task_statistics()
        print(f"✓ 任务统计: {stats}")

        api.stop()
        return True

    except Exception as e:
        print(f"✗ 任务系统测试失败: {e}")
        traceback.print_exc()
        return False


def test_error_handling():
    """测试错误处理"""
    print("\n测试错误处理...")

    try:
        api = AutomationAPI()
        api.start()

        # 测试无效窗口句柄
        invalid_hwnd = "invalid_hwnd_12345"
        result = api.click(invalid_hwnd, 100, 100)
        print(f"✓ 无效窗口句柄处理: {result}")

        # 测试任务取消
        task_id = api.create_click_task(
            hwnd=invalid_hwnd, x=100, y=100, name="测试取消任务"
        )

        cancel_result = api.cancel_task(task_id)
        print(f"✓ 任务取消: {cancel_result}")

        api.stop()
        return True

    except Exception as e:
        print(f"✗ 错误处理测试失败: {e}")
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print_system_info()

    tests = [
        ("模块导入", test_imports),
        ("窗口管理器", test_window_manager),
        ("自动化引擎", test_automation_engine),
        ("基础API", test_api_basic),
        ("平台特定功能", test_platform_specific),
        ("任务系统", test_task_system),
        ("错误处理", test_error_handling),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ {test_name} 测试异常: {e}")
            results[test_name] = False

    # 打印总结
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)

    passed = 0
    total = len(tests)

    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1

    print("-" * 60)
    print(f"总计: {passed}/{total} 个测试通过")

    if passed == total:
        print("🎉 所有测试通过！跨平台功能正常。")
        return True
    else:
        print("⚠️  部分测试失败，请检查错误信息。")
        return False


def main():
    """主函数"""
    try:
        success = run_all_tests()

        print("\n" + "=" * 60)
        print("测试建议:")
        print("=" * 60)

        system = platform.system()

        if system == "Windows":
            print("• 在Windows上，建议安装pywin32以获得更好的支持:")
            print("  pip install pywin32")
        elif system == "Darwin":  # macOS
            print("• 在macOS上，请确保已授予必要的权限:")
            print("  系统偏好设置 > 安全性与隐私 > 辅助功能")
            print("  系统偏好设置 > 安全性与隐私 > 屏幕录制")
        else:  # Linux
            print("• 在Linux上，请确保安装了必要的系统包:")
            print("  sudo apt-get install python3-tk python3-dev")
            print("• 确保DISPLAY环境变量已正确设置")

        print("\n如果遇到问题，请参考:")
        print("• README.md - 基本使用说明")
        print("• CROSS_PLATFORM_MIGRATION.md - 跨平台迁移指南")

        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n\n用户中断测试")
        return 1
    except Exception as e:
        print(f"\n\n测试过程中发生未预期的错误: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
