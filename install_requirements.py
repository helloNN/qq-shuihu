#!/usr/bin/env python3
"""
QQ水浒跨平台自动化项目 - 依赖包安装脚本
按照两步安装流程：先安装核心依赖，再安装平台特定依赖
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def get_platform_requirements():
    """根据操作系统返回对应的requirements文件名"""
    system = platform.system().lower()

    requirements_map = {
        "windows": "requirements-windows.txt",
        "darwin": "requirements-macos.txt",  # macOS
        "linux": "requirements-linux.txt",
    }

    return requirements_map.get(system, None)


def check_requirements_file(filename):
    """检查requirements文件是否存在"""
    file_path = Path(filename)
    if not file_path.exists():
        print(f"❌ 错误: 找不到文件 {filename}")
        return False
    return True


def install_requirements(filename, description="依赖包"):
    """安装指定的requirements文件"""
    print(f"📦 正在安装{description}: {filename}")

    try:
        # 使用subprocess运行pip install命令
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", filename],
            check=True,
            capture_output=True,
            text=True,
        )

        print(f"✅ {description}安装成功!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ {description}安装失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ {description}安装过程中发生错误: {e}")
        return False


def print_platform_info():
    """打印平台信息"""
    print("🖥️  系统信息:")
    print(f"   操作系统: {platform.system()}")
    print(f"   系统版本: {platform.release()}")
    print(f"   架构: {platform.machine()}")
    print(f"   Python版本: {platform.python_version()}")
    print()


def print_installation_guide():
    """打印手动安装指南"""
    print("📋 手动安装指南:")
    print("   步骤1: pip install -r requirements.txt        # 安装核心依赖")
    print("   步骤2: 根据平台安装特定依赖:")
    print("     Windows: pip install -r requirements-windows.txt")
    print("     macOS:   pip install -r requirements-macos.txt")
    print("     Linux:   pip install -r requirements-linux.txt")
    print()


def main():
    """主函数"""
    print("🚀 QQ水浒跨平台自动化项目 - 依赖包安装工具")
    print("=" * 60)

    # 打印平台信息
    print_platform_info()

    # 检查核心依赖文件
    core_requirements = "requirements.txt"
    if not check_requirements_file(core_requirements):
        print("❌ 找不到核心依赖文件!")
        print_installation_guide()
        return 1

    # 获取平台特定的requirements文件
    platform_requirements = get_platform_requirements()
    platform_name = platform.system()

    print(f"🎯 检测到当前平台: {platform_name}")
    print(f"📄 将按以下顺序安装:")
    print(f"   1. {core_requirements} (核心依赖)")

    if platform_requirements and check_requirements_file(platform_requirements):
        print(f"   2. {platform_requirements} ({platform_name}特定依赖)")
        has_platform_deps = True
    else:
        print(f"   2. 无{platform_name}特定依赖文件")
        has_platform_deps = False

    print()

    # 询问用户是否继续安装
    try:
        user_input = input(f"🔍 是否开始安装依赖包? (y/N): ").strip().lower()
        if user_input not in ["y", "yes", "是"]:
            print("⏹️  安装已取消")
            print_installation_guide()
            return 0
    except (KeyboardInterrupt, EOFError):
        print("\n⏹️  安装已取消")
        return 0

    print("\n" + "=" * 60)
    print("开始安装过程...")
    print("=" * 60)

    # 步骤1: 安装核心依赖
    print("\n📋 步骤 1/2: 安装核心跨平台依赖")
    print("-" * 40)
    success_core = install_requirements(core_requirements, "核心依赖")

    if not success_core:
        print("\n❌ 核心依赖安装失败，停止安装过程")
        print_installation_guide()
        return 1

    # 步骤2: 安装平台特定依赖
    success_platform = True
    if has_platform_deps:
        print(f"\n📋 步骤 2/2: 安装{platform_name}特定依赖")
        print("-" * 40)
        success_platform = install_requirements(
            platform_requirements, f"{platform_name}特定依赖"
        )

        if not success_platform:
            print(f"\n⚠️  {platform_name}特定依赖安装失败，但核心功能仍可使用")
    else:
        print(f"\n📋 步骤 2/2: 跳过{platform_name}特定依赖（无需安装）")

    # 安装结果总结
    print("\n" + "=" * 60)
    print("安装结果总结:")
    print("=" * 60)

    if success_core and success_platform:
        print("🎉 所有依赖包安装完成! 项目已准备就绪!")
        print("\n🚀 现在可以运行项目了:")
        print("   python examples/basic_example.py")
        print("   python examples/advanced_example.py")
        return 0
    elif success_core:
        print("✅ 核心依赖安装成功，基本功能可用")
        print("⚠️  部分平台特定功能可能受限")
        print("\n🚀 可以尝试运行项目:")
        print("   python examples/basic_example.py")
        return 0
    else:
        print("❌ 安装失败")
        print("\n💡 请尝试手动安装:")
        print_installation_guide()
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  安装已被用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        sys.exit(1)
