# Docker 跨平台部署指南

本指南详细说明如何使用Docker部署和运行QQ水浒跨平台自动化项目。

## 📋 目录

- [快速开始](#快速开始)
- [构建和运行](#构建和运行)
- [环境配置](#环境配置)
- [故障排除](#故障排除)
- [高级用法](#高级用法)

## 🚀 快速开始

### 前置条件

确保已安装以下软件：

- [Docker](https://www.docker.com/get-started) (版本 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (版本 2.0+)

### 验证安装

```bash
# 检查Docker版本
docker --version

# 检查Docker Compose版本
docker-compose --version
```

## 🔧 构建和运行

### 1. 克隆项目

```bash
git clone <项目地址>
cd qq-shuihu
```

### 2. 构建镜像

```bash
# 构建跨平台自动化镜像
docker-compose build

# 或者单独构建
docker build -t qq-shuihu-automation .
```

### 3. 运行服务

```bash
# 启动所有服务
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f automation
```

### 4. 运行测试

```bash
# 运行跨平台功能测试
docker-compose run --rm test

# 或者进入容器手动测试
docker-compose exec automation bash
python test_cross_platform.py
```

## ⚙️ 环境配置

### 环境变量

在 `docker-compose.yml` 中可以配置以下环境变量：

```yaml
environment:
  - PYTHONPATH=/app/src          # Python路径
  - LOG_LEVEL=INFO               # 日志级别 (DEBUG/INFO/WARNING/ERROR)
  - MAX_WORKERS=4                # 最大工作线程数
  - TASK_TIMEOUT=30              # 任务超时时间(秒)
  - DISPLAY=:99                  # 虚拟显示器
  - CROSS_PLATFORM=true          # 启用跨平台模式
```

### 数据卷

项目使用以下数据卷：

```yaml
volumes:
  - .:/app                       # 项目源码(开发时)
  - automation_logs:/app/logs    # 日志文件
  - automation_screenshots:/app/screenshots  # 截图文件
  - automation_templates:/app/templates      # 模板文件
```

### 端口映射

```yaml
ports:
  - "8000:8000"    # API服务端口
  - "6379:6379"    # Redis端口(可选)
```

## 🐛 故障排除

### 常见问题

#### 1. 构建失败

**问题**: Docker构建时依赖安装失败

**解决方案**:
```bash
# 清理Docker缓存
docker system prune -a

# 重新构建，不使用缓存
docker-compose build --no-cache

# 分步安装依赖(已在Dockerfile中实现)
```

#### 2. GUI应用无法运行

**问题**: 图形界面相关功能报错

**解决方案**:
```bash
# 确保虚拟显示器正常运行
docker-compose exec automation ps aux | grep Xvfb

# 检查DISPLAY环境变量
docker-compose exec automation echo $DISPLAY

# 手动启动虚拟显示器
docker-compose exec automation /usr/local/bin/start-xvfb.sh
```

#### 3. 权限问题

**问题**: 文件权限错误

**解决方案**:
```bash
# 修复文件权限
sudo chown -R $USER:$USER .

# 或者使用root用户运行
docker-compose exec --user root automation bash
```

#### 4. 内存不足

**问题**: 容器内存不足导致程序崩溃

**解决方案**:
```bash
# 增加Docker内存限制
# 编辑 docker-compose.yml
deploy:
  resources:
    limits:
      memory: 4G  # 增加到4GB
```

### 调试命令

```bash
# 查看容器状态
docker-compose ps

# 查看实时日志
docker-compose logs -f automation

# 进入容器调试
docker-compose exec automation bash

# 检查容器资源使用
docker stats qq-shuihu-automation

# 查看容器内进程
docker-compose exec automation ps aux

# 测试网络连接
docker-compose exec automation ping google.com
```

## 🔬 高级用法

### 开发模式

```bash
# 使用开发配置启动
docker-compose -f docker-compose.yml -f docker-compose.override.yml up

# 进入开发容器
docker-compose exec automation bash

# 实时代码更新(已挂载项目目录)
# 修改代码后直接在容器内测试
python examples/basic_example.py
```

### 生产部署

```bash
# 创建生产配置文件 docker-compose.prod.yml
version: "3.8"
services:
  automation:
    environment:
      - LOG_LEVEL=WARNING
      - PRODUCTION=true
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G

# 使用生产配置启动
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 多平台构建

```bash
# 启用Docker buildx
docker buildx create --use

# 构建多平台镜像
docker buildx build --platform linux/amd64,linux/arm64 -t qq-shuihu-automation .

# 推送到镜像仓库
docker buildx build --platform linux/amd64,linux/arm64 -t your-registry/qq-shuihu-automation --push .
```

### 集群部署

```bash
# 使用Docker Swarm
docker swarm init

# 部署到集群
docker stack deploy -c docker-compose.yml qq-shuihu

# 扩展服务
docker service scale qq-shuihu_automation=3
```

### 监控和日志

```bash
# 启用Prometheus监控(如果配置了)
docker-compose --profile monitoring up -d

# 查看Grafana仪表板
open http://localhost:3001

# 集中日志管理
docker-compose logs --since 1h automation > automation.log
```

## 📚 相关文档

- [跨平台迁移指南](CROSS_PLATFORM_MIGRATION.md)
- [项目README](README.md)
- [API文档](docs/API.md)
- [Docker官方文档](https://docs.docker.com/)

## 💡 最佳实践

1. **资源管理**: 根据实际需求调整内存和CPU限制
2. **安全性**: 不要在生产环境中使用默认密码
3. **备份**: 定期备份重要数据卷
4. **更新**: 定期更新基础镜像和依赖包
5. **监控**: 配置适当的健康检查和监控

## 🆘 获取帮助

如果遇到问题，可以：

1. 查看本文档的故障排除部分
2. 检查Docker和Docker Compose版本
3. 查看容器日志: `docker-compose logs automation`
4. 提交Issue到项目仓库

---

*最后更新: 2024年6月23日*
