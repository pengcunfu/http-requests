@echo off
echo 🚀 HTTP请求工具 - 构建脚本
echo ================================

echo 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python
    pause
    exit /b 1
)

echo 安装构建依赖...
pip install -r requirements-dev.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo 开始构建...
python build.py
if %errorlevel% neq 0 (
    echo ❌ 构建失败
    pause
    exit /b 1
)

echo ✅ 构建完成!
echo 查看 'release' 目录获取可执行文件
pause
