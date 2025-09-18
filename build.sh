#!/bin/bash

echo "🚀 HTTP请求工具 - 构建脚本"
echo "================================"

echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

python3 --version

echo "安装构建依赖..."
if ! pip3 install -r requirements-dev.txt; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "开始构建..."
if ! python3 build.py; then
    echo "❌ 构建失败"
    exit 1
fi

echo "✅ 构建完成!"
echo "查看 'release' 目录获取可执行文件"
