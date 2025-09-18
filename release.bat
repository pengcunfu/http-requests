@echo off
setlocal

if "%~1"=="" (
    echo 用法: release.bat ^<版本号^>
    echo 示例: release.bat v2.0.1
    exit /b 1
)

echo 🚀 准备发布版本: %1
echo.

python release.py %1
if %errorlevel% neq 0 (
    echo ❌ 发布失败
    pause
    exit /b 1
)

echo.
echo ✅ 发布完成!
echo 检查GitHub Actions的构建状态。
pause
