#!/bin/bash
# 激活NS项目虚拟环境
source .venv/bin/activate
echo "✅ NS项目虚拟环境已激活"
echo "Python: $(which python)"
echo "版本: $(python --version)"
