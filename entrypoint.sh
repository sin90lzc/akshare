#!/bin/bash

# 每次启动更新akshare
pip install akshare --upgrade -i https://pypi.org/simple

# 启动默认命令或你自己的逻辑（例如启动 jupyter notebook）
exec "$@"
