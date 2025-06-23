# QQ水浒跨平台自动化项目

一个功能强大的跨平台软件自动化框架，支持Windows、macOS、Linux系统，提供多线程/多进程、前台/后台操作、图像识别等功能。

## 🚀 项目特性

- **跨平台支持**: 支持Windows、macOS、Linux三大主流操作系统
- **多执行模式**: 支持线程和进程两种执行模式，可通过配置动态切换
- **灵活操作模式**: 支持前台/后台点击和图像识别，适应不同场景需求
- **跨平台窗口管理**: 基于pygetwindow等跨平台库的窗口操作，支持隐藏窗口的后台操作
- **任务系统**: 类似React的任务管理系统，支持优先级、取消、重试等功能
- **图像识别**: 基于OpenCV的模板匹配，支持精确的图像定位和点击
- **简单易用**: 提供简洁的API接口，方便快速开发自动化脚本
- **Docker支持**: 提供高效的Docker容器化方案，支持实时代码更新

## 📁 项目结构

```
qq-shuihu/
├── src/                          # 源代码目录
│   ├── __init__.py
│   ├── config.py                 # 配置管理
│   ├── window_manager.py         # 跨平台窗口管理器
│   ├── automation.py             # 跨平台自动化引擎
│   ├── task_system.py            # 任务系统
│   └── main.py                   # 主要API接口
├── examples/                     # 示例代码
│   ├── basic_example.py          # 基础使用示例
│   └── advanced_example.py       # 高级使用示例
├── requirements.txt              # Python依赖包
├── Dockerfile                    # Docker构建文件
├── docker-compose.yml           # Docker Compose配置
└── README.md                     # 项目说明文档
```

## 🛠️ 环境要求

- **操作系统**: Windows 10/11、macOS 10.14+、Linux (Ubuntu 18.04+)
- **Python**: 3.8+
- **依赖包**: 见 `requirements.txt`

## 📦 安装依赖

```bash
# 安装Python依赖包
pip install -r requirements.txt
```

### 主要依赖包说明

- `pyautogui`: 跨平台GUI自动化库
- `pynput`: 跨平台输入控制库
- `pygetwindow`: 跨平台窗口管理库
- `opencv-python`: 图像处理和识别
- `numpy`: 数值计算
- `Pillow`: 图像处理
- `psutil`: 系统进程管理

### 系统特定依赖

#### Windows
```bash
# 可选：安装pywin32以获得更好的Windows API支持
pip install pywin32
```

#### macOS
```bash
# 可能需要安装额外的系统权限
# 在系统偏好设置 > 安全性与隐私 > 辅助功能中添加终端或Python
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk python3-dev

# 可能需要安装X11相关库
sudo apt-get install xvfb  # 用于无头环境
```

## 🚀 快速开始

### 基础使用

```python
from src.main import AutomationAPI, TaskPriority
from src.config import ClickMode, ImageMode

# 创建API实例
api = AutomationAPI()

try:
    # 启动自动化系统
    api.start()
    
    # 设置为前台模式（跨平台兼容性更好）
    api.set_click_mode(ClickMode.FOREGROUND)
    api.set_image_mode(ImageMode.FOREGROUND)
    
    # 查找窗口（根据操作系统自动适配）
    windows = api.find_windows_by_title("记事本")  # Windows
    # windows = api.find_windows_by_title("TextEdit")  # macOS
    # windows = api.find_windows_by_title("gedit")  # Linux
    
    if windows:
        hwnd = windows[0].hwnd
        
        # 直接点击
        api.click(hwnd, 100, 100)
        
        # 发送文本
        api.send_text(hwnd, "Hello, 跨平台自动化!")
        
        # 图像识别点击
        api.click_image(hwnd, "button.png", threshold=0.8)

finally:
    # 停止自动化系统
    api.stop()
```

### 跨平台窗口查找

```python
import platform

# 根据操作系统查找不同的应用
target_apps = []
if platform.system() == "Windows":
    target_apps = ["记事本", "Notepad", "Calculator"]
elif platform.system() == "Darwin":  # macOS
    target_apps = ["TextEdit", "Calculator", "Terminal"]
else:  # Linux
    target_apps = ["gedit", "Text Editor", "Calculator"]

for app_name in target_apps:
    windows = api.find_windows_by_title(app_name)
    if windows:
        print(f"找到应用: {app_name}")
        break
```

### 任务系统使用

```python
# 创建点击任务
task_id = api.create_click_task(
    hwnd=hwnd,
    x=100,
    y=100,
    name="点击任务",
    priority=TaskPriority.HIGH,
    max_retries=3
)

# 等待任务完成
result = api.wait_for_task(task_id, timeout=30)
print(f"任务结果: {result.success}")
```

### 自定义任务

```python
from src.task_system import BaseTask, Task, TaskResult

class CustomTask(BaseTask):
    def __init__(self, task: Task, custom_param: str):
        super().__init__(task)
        self.custom_param = custom_param
    
    def execute(self) -> TaskResult:
        # 实现自定义逻辑
        try:
            # 执行自定义操作
            result_data = {"param": self.custom_param}
            return TaskResult(success=True, data=result_data)
        except Exception as e:
            return TaskResult(success=False, error=str(e))

# 使用自定义任务
task = Task(name="自定义任务")
custom_task = CustomTask(task, "自定义参数")
task_id = api.create_custom_task(custom_task)
```

## 🔧 配置说明

### 执行模式配置

```python
from src.config import ExecutionMode

# 设置为线程模式（默认）
api.set_execution_mode(ExecutionMode.THREAD)

# 设置为进程模式
api.set_execution_mode(ExecutionMode.PROCESS)
```

### 操作模式配置

```python
from src.config import ClickMode, ImageMode

# 前台模式（需要窗口在前台，跨平台兼容性好）
api.set_click_mode(ClickMode.FOREGROUND)
api.set_image_mode(ImageMode.FOREGROUND)

# 后台模式（在某些平台可能受限）
api.set_click_mode(ClickMode.BACKGROUND)
api.set_image_mode(ImageMode.BACKGROUND)
```

## 📚 API 文档

### 窗口管理

```python
# 根据标题查找窗口
windows = api.find_windows_by_title("窗口标题", exact_match=False)

# 根据类名查找窗口（主要在Windows上有效）
windows = api.find_windows_by_class("类名")

# 根据进程名查找窗口
windows = api.find_windows_by_process("notepad.exe")  # Windows
windows = api.find_windows_by_process("TextEdit")     # macOS
windows = api.find_windows_by_process("gedit")        # Linux

# 获取所有窗口
windows = api.get_all_windows(include_hidden=True)

# 窗口操作
api.bring_window_to_front(hwnd)
api.show_window(hwnd)
api.hide_window(hwnd)
```

### 自动化操作

```python
# 点击操作
api.click(hwnd, x, y, button="left")
api.double_click(hwnd, x, y)
api.drag(hwnd, start_x, start_y, end_x, end_y)

# 输入操作
api.send_text(hwnd, "文本内容")
api.send_key(hwnd, key_code, ctrl=False, alt=False, shift=False)

# 图像识别
result = api.find_image(hwnd, "template.png", threshold=0.8)
api.click_image(hwnd, "button.png", threshold=0.8)
api.wait_for_image(hwnd, "loading.png", timeout=10)

# 其他操作
api.scroll(hwnd, x, y, direction="up", clicks=3)
image = api.capture_window(hwnd)
```

### 任务管理

```python
# 创建任务
click_task_id = api.create_click_task(hwnd, x, y, **options)
image_task_id = api.create_image_recognition_task(hwnd, template_path, **options)

# 任务控制
api.cancel_task(task_id)
status = api.get_task_status(task_id)
result = api.get_task_result(task_id)
result = api.wait_for_task(task_id, timeout=60)

# 批量操作
task_ids = api.batch_click(click_list, use_task=True)
task_ids = api.chain_tasks(task_configs)

# 统计信息
stats = api.get_task_statistics()
```

## 🐳 Docker 使用

### 构建镜像

```bash
# 构建基础镜像
docker build -t qq-shuihu-automation .

# 使用Docker Compose
docker-compose up -d
```

### 开发环境

```bash
# 开发模式（实时代码更新）
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### 生产环境

```bash
# 生产模式
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 挂载项目目录

```bash
# 挂载当前目录到容器，实现实时更新
docker run -v $(pwd):/app qq-shuihu-automation
```

## 📝 示例代码

### 运行基础示例

```bash
python examples/basic_example.py
```

### 运行高级示例

```bash
python examples/advanced_example.py
```

### 示例功能

- **跨平台窗口操作**: 查找窗口、点击、输入文本
- **任务系统**: 创建任务、任务依赖、任务重试
- **图像识别**: 截图、模板匹配、图像点击
- **批量操作**: 批量点击、任务链
- **错误处理**: 任务取消、重试机制
- **性能测试**: 大量任务处理性能测试
- **真实场景**: 模拟表单填写等实际应用

## 🔍 常见问题

### Q: 如何在不同操作系统上处理窗口？

A: 项目会自动检测操作系统并使用相应的窗口管理方法：

```python
import platform

if platform.system() == "Windows":
    # Windows特定的处理
    windows = api.find_windows_by_title("记事本")
elif platform.system() == "Darwin":  # macOS
    # macOS特定的处理
    windows = api.find_windows_by_title("TextEdit")
else:  # Linux
    # Linux特定的处理
    windows = api.find_windows_by_title("gedit")
```

### Q: 后台模式在所有平台都支持吗？

A: 后台模式的支持程度因操作系统而异：

- **Windows**: 通过pywin32可以实现真正的后台操作
- **macOS**: 受系统安全限制，可能需要特殊权限
- **Linux**: 在X11环境下支持，Wayland可能受限

建议在跨平台应用中优先使用前台模式以确保兼容性。

### Q: 如何提高图像识别的准确性？

A: 可以通过以下方式提高识别准确性：

1. 调整匹配阈值
2. 使用高质量的模板图像
3. 确保模板图像尺寸适中
4. 在稳定的环境下截取模板

```python
# 调整阈值
result = api.find_image(hwnd, "template.png", threshold=0.9)

# 查找所有匹配项
matches = api.automation_engine.find_all_images(hwnd, "template.png", threshold=0.8)
```

### Q: 如何处理权限问题？

A: 不同操作系统的权限要求：

**macOS**:
- 在"系统偏好设置" > "安全性与隐私" > "辅助功能"中添加终端或Python
- 可能需要在"屏幕录制"中也添加权限

**Linux**:
- 确保用户有访问X11显示的权限
- 在无头环境中可能需要使用xvfb

**Windows**:
- 通常不需要特殊权限
- 某些受保护的应用可能需要管理员权限

### Q: 如何处理任务失败和重试？

A: 任务系统内置了重试机制：

```python
# 创建带重试的任务
task_id = api.create_click_task(
    hwnd=hwnd,
    x=100,
    y=100,
    max_retries=3,  # 最多重试3次
    timeout=30      # 超时时间30秒
)

# 检查任务结果
result = api.wait_for_task(task_id)
if result:
    print(f"成功: {result.success}")
    print(f"重试次数: {result.retry_count}")
```

## 🔄 从pywin32迁移

本项目已从依赖pywin32的Windows专用方案迁移到跨平台方案：

### 主要变化

1. **窗口管理**: 从`win32gui`迁移到`pygetwindow`
2. **自动化操作**: 从`win32api`迁移到`pyautogui`和`pynput`
3. **窗口句柄**: 支持`Union[int, str]`类型以适应不同平台

### 迁移指南

如果你有基于旧版本的代码，主要需要注意：

1. **导入更改**: 无需更改，API保持兼容
2. **窗口句柄**: 现在可能是字符串类型，不仅仅是整数
3. **后台操作**: 在某些平台可能受限，建议测试

```python
# 旧代码（仍然兼容）
hwnd = windows[0].hwnd  # 可能是int或str
api.click(hwnd, 100, 100)

# 新代码（推荐的跨平台写法）
import platform
if platform.system() == "Windows":
    target_app = "记事本"
else:
    target_app = "TextEdit" if platform.system() == "Darwin" else "gedit"

windows = api.find_windows_by_title(target_app)
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [pyautogui](https://github.com/asweigart/pyautogui) - 跨平台GUI自动化
- [pynput](https://github.com/moses-palmer/pynput) - 跨平台输入控制
- [pygetwindow](https://github.com/asweigart/PyGetWindow) - 跨平台窗口管理
- [OpenCV](https://opencv.org/) - 图像处理和识别
- [psutil](https://github.com/giampaolo/psutil) - 系统进程管理

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件
- 创建 Discussion

---

**注意**: 本项目仅供学习和研究使用，请遵守相关法律法规，不得用于非法用途。使用时请注意各操作系统的权限要求和安全限制。
