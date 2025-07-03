#!/bin/bash

# 每次启动自动安装需要的依赖（如果已安装会快速跳过）
pip install --quiet sqlalchemy pymysql

# 启动默认命令或你自己的逻辑（例如启动 jupyter notebook）
exec "$@"
