#!/usr/bin/env python3
"""
Nuitka构建脚本 - HTTP请求工具
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def run_command(cmd, shell=True):
    """运行命令并处理错误"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=shell, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', 'main.build', 'main.dist', 'main.onefile-build']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理目录: {dir_name}")
            shutil.rmtree(dir_name)

def build_with_nuitka():
    """使用Nuitka编译应用"""
    print("开始Nuitka编译...")
    
    # 基础编译参数
    cmd_parts = [
        "python", "-m", "nuitka",
        "--standalone",  # 独立可执行文件
        "--enable-plugin=pyside6",  # PySide6插件
        "--assume-yes-for-downloads",  # 自动确认下载
        "--output-dir=dist",  # 输出目录
    ]
    
    # 平台特定设置
    system = platform.system()
    if system == "Windows":
        cmd_parts.extend([
            "--windows-disable-console",  # 隐藏控制台窗口
            "--windows-icon-from-ico=icon.ico" if os.path.exists("icon.ico") else "",
        ])
        output_name = "HTTP-Requests-Tool.exe"
    elif system == "Darwin":  # macOS
        cmd_parts.extend([
            "--macos-create-app-bundle",
        ])
        output_name = "HTTP-Requests-Tool.app"
    else:  # Linux
        output_name = "HTTP-Requests-Tool"
    
    cmd_parts.extend([
        f"--output-filename={output_name}",
        "main.py"
    ])
    
    # 过滤空字符串
    cmd_parts = [part for part in cmd_parts if part]
    
    cmd = " ".join(cmd_parts)
    
    if run_command(cmd):
        print("✅ Nuitka编译成功!")
        return True
    else:
        print("❌ Nuitka编译失败!")
        return False

def create_portable_package():
    """创建便携版压缩包"""
    print("创建便携版压缩包...")
    
    system = platform.system()
    if system == "Windows":
        app_name = "HTTP-Requests-Tool.exe"
        archive_name = "HTTP-Requests-Tool-Windows"
    elif system == "Darwin":
        app_name = "HTTP-Requests-Tool.app"
        archive_name = "HTTP-Requests-Tool-macOS"
    else:
        app_name = "HTTP-Requests-Tool"
        archive_name = "HTTP-Requests-Tool-Linux"
    
    dist_path = Path("dist") / "main.dist"
    if not dist_path.exists():
        print("❌ 找不到编译输出目录")
        return False
    
    # 创建发布目录
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # 复制应用文件
    app_dir = release_dir / archive_name
    if app_dir.exists():
        shutil.rmtree(app_dir)
    
    shutil.copytree(dist_path, app_dir)
    
    # 添加README和许可证
    shutil.copy2("README.md", app_dir / "README.md")
    
    # 创建压缩包
    if system == "Windows":
        archive_path = release_dir / f"{archive_name}.zip"
        shutil.make_archive(str(archive_path).replace('.zip', ''), 'zip', release_dir, archive_name)
    else:
        archive_path = release_dir / f"{archive_name}.tar.gz"
        shutil.make_archive(str(archive_path).replace('.tar.gz', ''), 'gztar', release_dir, archive_name)
    
    print(f"✅ 便携版压缩包已创建: {archive_path}")
    return True

def main():
    """主函数"""
    print("🚀 HTTP请求工具 - Nuitka构建脚本")
    print("=" * 50)
    
    # 检查是否安装了nuitka
    try:
        subprocess.run(["python", "-m", "nuitka", "--version"], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ 未找到Nuitka，请先安装:")
        print("pip install nuitka")
        sys.exit(1)
    
    # 清理之前的构建
    clean_build_dirs()
    
    # 编译应用
    if not build_with_nuitka():
        sys.exit(1)
    
    # 创建便携版
    if not create_portable_package():
        sys.exit(1)
    
    print("\n🎉 构建完成!")
    print("检查 'release' 目录获取最终的可执行文件。")

if __name__ == "__main__":
    main()
