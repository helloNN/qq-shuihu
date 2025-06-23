# 跨平台迁移指南

## 概述

本项目已成功从依赖 pywin32 的 Windows 专用方案迁移到支持 Windows、macOS 和 Linux 的跨平台方案。

## 迁移内容

### 1. 窗口管理模块 (`src/window_manager.py`)

#### 原始问题
- 严重依赖 pywin32，只能在 Windows 上运行
- 使用 Windows 特定的 API (win32gui, win32con, win32process)

#### 解决方案
- **跨平台库**: 使用 `pygetwindow` 作为主要的跨平台窗口管理库
- **渐进式降级**: 在不同平台上优雅降级到可用的库
- **模拟模式**: 在 Linux 等不支持图形界面的环境中提供模拟窗口用于测试

#### 平台支持策略

**Windows:**
```python
# 优先级: pywin32 > pygetwindow
1. 尝试导入 pywin32 (win32gui, win32con, win32process)
2. 如果失败，回退到 pygetwindow
3. 提供完整的原生 Windows API 支持
```

**macOS:**
```python
# 优先级: Quartz/AppKit + pygetwindow
1. 尝试导入 macOS 原生库 (Quartz, AppKit)
2. 同时尝试导入 pygetwindow 作为补充
3. 提供 macOS 特定的窗口管理功能
```

**Linux:**
```python
# 策略: subprocess + 模拟模式
1. 使用 subprocess 进行系统调用
2. 在无 GUI 环境中创建模拟窗口
3. 提供基本的窗口管理功能
```

### 2. 自动化引擎 (`src/automation.py`)

#### 跨平台改进
- 使用 `pyautogui` 替代 Windows 特定的鼠标/键盘控制
- 使用 `opencv-python` 和 `PIL` 进行跨平台图像处理
- 使用 `pynput` 进行跨平台输入事件监听

### 3. 依赖管理

#### 新的依赖结构
```
核心依赖 (所有平台):
├── psutil>=5.8.0          # 进程管理
├── opencv-python>=4.5.0   # 图像处理
├── pillow>=8.0.0          # 图像处理
├── pyautogui>=0.9.50      # 自动化控制
├── pynput>=1.7.0          # 输入事件
└── pygetwindow>=0.0.9     # 窗口管理

平台特定依赖:
├── Windows: pywin32 (可选，用于增强功能)
├── macOS: Quartz, AppKit (系统自带)
└── Linux: X11 相关库 (可选)
```

## 使用指南

### 安装依赖

#### 基础安装
```bash
pip install -r requirements.txt
```

#### Windows 增强支持
```bash
pip install pywin32
```

#### Linux 图形界面支持
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk python3-dev

# CentOS/RHEL
sudo yum install tkinter python3-devel
```

### 测试跨平台功能

运行跨平台测试脚本：
```bash
python test_cross_platform.py
```

### Docker 支持

#### 简化版 Docker (无 GUI)
```bash
docker build -t qq-shuihu-automation-simple -f Dockerfile.simple .
docker run --rm qq-shuihu-automation-simple python test_cross_platform.py
```

#### 完整版 Docker (带 GUI 支持)
```bash
docker build -t qq-shuihu-automation .
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix qq-shuihu-automation
```

## API 兼容性

### 窗口管理 API

所有原有的 API 保持兼容，在不同平台上提供一致的接口：

```python
from src.window_manager import CrossPlatformWindowManager

wm = CrossPlatformWindowManager()

# 获取所有窗口 (跨平台)
windows = wm.get_all_windows()

# 查找窗口 (跨平台)
notepad_windows = wm.find_windows_by_title("记事本")

# 窗口操作 (跨平台)
wm.bring_window_to_front(window.hwnd)
wm.maximize_window(window.hwnd)
wm.minimize_window(window.hwnd)
```

### 自动化 API

```python
from src.main import AutomationAPI

api = AutomationAPI()
api.start()

# 屏幕截图 (跨平台)
screenshot = api.automation_engine.take_screenshot()

# 窗口截图 (跨平台)
window_shot = api.automation_engine.take_window_screenshot(hwnd)

# 鼠标/键盘操作 (跨平台)
api.automation_engine.click(x, y)
api.automation_engine.type_text("Hello World")
```

## 平台特定注意事项

### Windows
- 推荐安装 pywin32 以获得最佳性能和功能
- 支持所有原生 Windows 窗口管理功能
- 完全向后兼容

### macOS
- 需要授权应用访问辅助功能
- 某些功能可能需要管理员权限
- 建议在系统偏好设置中启用应用的屏幕录制权限

### Linux
- 在无 GUI 环境中自动启用模拟模式
- 建议安装 X11 相关库以获得完整功能
- Docker 环境中默认使用模拟模式

## 故障排除

### 常见问题

1. **pygetwindow 在 Linux 上不工作**
   - 这是预期行为，系统会自动回退到模拟模式
   - 模拟模式提供基本功能用于测试和开发

2. **macOS 权限问题**
   ```bash
   # 检查权限
   sudo spctl --assess --verbose /path/to/your/app
   
   # 重置权限
   sudo tccutil reset ScreenCapture
   sudo tccutil reset Accessibility
   ```

3. **Windows 上缺少 pywin32**
   ```bash
   pip install pywin32
   # 或者使用 conda
   conda install pywin32
   ```

### 性能优化

1. **Windows**: 安装 pywin32 可显著提升性能
2. **所有平台**: 调整截图质量和频率以优化性能
3. **Linux**: 在生产环境中考虑使用 headless 模式

## 迁移检查清单

- [x] 移除硬编码的 Windows 依赖
- [x] 实现跨平台窗口管理
- [x] 添加平台检测和适配
- [x] 创建模拟模式用于测试
- [x] 更新依赖列表
- [x] 编写跨平台测试
- [x] 创建 Docker 支持
- [x] 更新文档
- [x] 验证 API 兼容性
- [x] 添加错误处理和降级策略

## 后续改进

1. **增强 Linux 支持**: 添加更多 Linux 桌面环境的原生支持
2. **性能优化**: 针对不同平台优化性能
3. **功能扩展**: 添加更多平台特定的高级功能
4. **测试覆盖**: 扩展自动化测试覆盖率
5. **文档完善**: 添加更多使用示例和最佳实践

## 贡献指南

如果您想为跨平台支持做出贡献：

1. 确保代码在所有支持的平台上运行
2. 添加适当的平台检测和错误处理
3. 更新测试用例以覆盖新功能
4. 更新文档说明平台特定的行为
5. 遵循现有的代码风格和架构模式

---

**注意**: 本迁移保持了完全的向后兼容性，现有的 Windows 代码无需修改即可继续工作。
