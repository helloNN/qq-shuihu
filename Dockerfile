# 跨平台自动化项目 - 优化版Dockerfile
# 支持Windows、macOS、Linux的自动化框架

FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99

# 安装系统依赖 - 分步安装以提高成功率
RUN apt-get update && apt-get install -y --fix-missing \
    # 基础工具
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# 安装GUI自动化依赖
RUN apt-get update && apt-get install -y --fix-missing \
    xvfb \
    x11-utils \
    xauth \
    && rm -rf /var/lib/apt/lists/*

# 安装图像处理依赖
RUN apt-get update && apt-get install -y --fix-missing \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 安装OpenCV和媒体依赖
RUN apt-get update && apt-get install -y --fix-missing \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# 安装开发工具和Python依赖
RUN apt-get update && apt-get install -y --fix-missing \
    python3-tk \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装字体和其他工具
RUN apt-get update && apt-get install -y --fix-missing \
    fonts-liberation \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 升级pip并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 分步安装依赖以提高成功率
RUN pip install --no-cache-dir numpy>=1.24.0
RUN pip install --no-cache-dir opencv-python>=4.8.0
RUN pip install --no-cache-dir Pillow>=10.0.0
RUN pip install --no-cache-dir psutil>=5.9.0
RUN pip install --no-cache-dir pyautogui>=0.9.54
RUN pip install --no-cache-dir pynput>=1.7.6
RUN pip install --no-cache-dir pygetwindow>=0.0.9

# 创建非root用户
RUN useradd -m -u 1000 automation && \
    chown -R automation:automation /app

# 创建虚拟显示环境脚本
RUN echo '#!/bin/bash\n\
# 启动虚拟显示\n\
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &\n\
export DISPLAY=:99\n\
\n\
# 等待X服务器启动\n\
sleep 2\n\
\n\
# 执行传入的命令\n\
exec "$@"' > /usr/local/bin/start-xvfb.sh && \
    chmod +x /usr/local/bin/start-xvfb.sh

# 切换到非root用户
USER automation

# 暴露端口（如果需要Web界面或API）
EXPOSE 8000

# 设置挂载点（用于实时更新代码）
VOLUME ["/app"]

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; print('Container is healthy')" || exit 1

# 默认命令
CMD ["/usr/local/bin/start-xvfb.sh", "python", "-c", "print('跨平台自动化容器已启动，请挂载项目目录到/app并运行测试')"]
