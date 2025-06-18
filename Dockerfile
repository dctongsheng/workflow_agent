FROM python:3.11-slim

# 安装 uv
RUN pip install uv

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 使用 uv 安装依赖
RUN uv sync

# 暴露端口（如果需要的话）
EXPOSE 8000

# 启动命令
CMD ["uv", "run", "planning_generate_api/app.py"] 