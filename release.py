#!/usr/bin/env python3
"""
版本发布脚本
"""

import os
import sys
import subprocess
import re
from datetime import datetime
from pathlib import Path

def run_command(cmd, shell=True):
    """运行命令并返回结果"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=shell, check=True, 
                              capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return None

def validate_version(version):
    """验证版本号格式"""
    pattern = r'^v?\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$'
    return re.match(pattern, version) is not None

def update_version_file(version):
    """更新版本文件"""
    version_clean = version.lstrip('v')
    
    # 读取当前版本文件
    with open('version.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新版本号
    content = re.sub(r'__version__ = "[^"]*"', f'__version__ = "{version_clean}"', content)
    
    # 写入更新后的内容
    with open('version.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 版本文件已更新: {version_clean}")

def check_git_status():
    """检查Git状态"""
    status = run_command("git status --porcelain")
    if status:
        print("❌ 工作目录不干净，请先提交所有更改:")
        print(status)
        return False
    return True

def create_git_tag(version):
    """创建Git标签"""
    tag_message = f"Release {version}"
    
    # 创建标签
    if run_command(f'git tag -a {version} -m "{tag_message}"') is None:
        return False
    
    print(f"✅ Git标签已创建: {version}")
    return True

def push_to_github():
    """推送到GitHub"""
    # 推送代码
    if run_command("git push origin main") is None:
        return False
    
    # 推送标签
    if run_command("git push origin --tags") is None:
        return False
    
    print("✅ 代码和标签已推送到GitHub")
    return True

def build_locally():
    """本地构建测试"""
    print("开始本地构建测试...")
    if run_command("python build.py") is None:
        return False
    print("✅ 本地构建成功")
    return True

def main():
    """主函数"""
    print("🚀 HTTP请求工具 - 版本发布脚本")
    print("=" * 50)
    
    # 获取版本号
    if len(sys.argv) != 2:
        print("用法: python release.py <版本号>")
        print("示例: python release.py v2.0.1")
        sys.exit(1)
    
    version = sys.argv[1]
    
    # 验证版本号格式
    if not validate_version(version):
        print("❌ 版本号格式无效。请使用格式: v1.2.3 或 1.2.3")
        sys.exit(1)
    
    # 确保版本号以v开头
    if not version.startswith('v'):
        version = 'v' + version
    
    print(f"准备发布版本: {version}")
    
    # 检查Git状态
    if not check_git_status():
        sys.exit(1)
    
    # 更新版本文件
    update_version_file(version)
    
    # 提交版本更新
    run_command("git add version.py")
    run_command(f'git commit -m "Bump version to {version}"')
    
    # 本地构建测试
    build_choice = input("是否进行本地构建测试? (y/N): ").lower()
    if build_choice == 'y':
        if not build_locally():
            print("❌ 本地构建失败，发布中止")
            sys.exit(1)
    
    # 确认发布
    confirm = input(f"确认发布版本 {version}? (y/N): ").lower()
    if confirm != 'y':
        print("发布已取消")
        sys.exit(0)
    
    # 创建Git标签
    if not create_git_tag(version):
        sys.exit(1)
    
    # 推送到GitHub
    if not push_to_github():
        sys.exit(1)
    
    print(f"\n🎉 版本 {version} 发布完成!")
    print("GitHub Actions将自动构建并创建发布。")
    print(f"查看发布状态: https://github.com/yourusername/http-requests/actions")

if __name__ == "__main__":
    main()
