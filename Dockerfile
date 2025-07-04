FROM python:3
# 安装基础依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libxml2-dev libxslt1-dev zlib1g-dev \
    && pip install --upgrade pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 设置默认工作目录
WORKDIR /opt/workspace

COPY *.py requirements.txt entrypoint.sh ./
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["bash", "entrypoint.sh"]