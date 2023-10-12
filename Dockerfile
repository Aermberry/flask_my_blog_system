# 使用一个基础的 Python 镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 复制 pyproject.toml 和 poetry.lock 文件到工作目录
COPY pyproject.toml poetry.lock /app/

# 安装 Poetry 并使用它来安装项目依赖
RUN curl -sSL https://install.python-poetry.org | python - && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# 复制 Flask 应用程序的文件到工作目录
COPY . /app

# 暴露应用程序监听的端口（如果有的话）
EXPOSE 5000

# 启动 Flask 应用程序
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
