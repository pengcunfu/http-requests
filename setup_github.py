#!/usr/bin/env python3
"""
GitHub仓库设置脚本
"""

import os
import sys
import subprocess
import webbrowser

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

def check_git_installed():
    """检查Git是否已安装"""
    return run_command("git --version") is not None

def init_git_repo():
    """初始化Git仓库"""
    if os.path.exists('.git'):
        print("✅ Git仓库已存在")
        return True
    
    if run_command("git init") is None:
        return False
    
    print("✅ Git仓库已初始化")
    return True

def setup_git_config():
    """设置Git配置"""
    print("\n请输入Git配置信息:")
    name = input("您的姓名: ").strip()
    email = input("您的邮箱: ").strip()
    
    if name:
        run_command(f'git config user.name "{name}"')
    if email:
        run_command(f'git config user.email "{email}"')
    
    print("✅ Git配置已设置")

def add_remote_origin():
    """添加远程仓库"""
    print("\n设置GitHub远程仓库:")
    print("请先在GitHub上创建新仓库，然后输入仓库URL")
    print("示例: https://github.com/username/http-requests.git")
    
    repo_url = input("GitHub仓库URL: ").strip()
    if not repo_url:
        print("⚠️ 跳过远程仓库设置")
        return False
    
    # 检查是否已有远程仓库
    existing_remote = run_command("git remote get-url origin")
    if existing_remote:
        print(f"远程仓库已存在: {existing_remote}")
        overwrite = input("是否覆盖? (y/N): ").lower()
        if overwrite == 'y':
            run_command("git remote remove origin")
        else:
            return True
    
    if run_command(f"git remote add origin {repo_url}") is None:
        return False
    
    print("✅ 远程仓库已设置")
    return True

def initial_commit():
    """创建初始提交"""
    # 检查是否有提交
    result = run_command("git log --oneline")
    if result is not None and result:
        print("✅ 已有Git提交历史")
        return True
    
    # 添加所有文件
    run_command("git add .")
    
    # 创建初始提交
    if run_command('git commit -m "Initial commit: HTTP请求工具 v2.0.0"') is None:
        return False
    
    print("✅ 初始提交已创建")
    return True

def push_to_github():
    """推送到GitHub"""
    # 检查是否有远程仓库
    remote = run_command("git remote get-url origin")
    if not remote:
        print("⚠️ 未设置远程仓库，跳过推送")
        return False
    
    # 设置默认分支
    run_command("git branch -M main")
    
    # 推送到GitHub
    if run_command("git push -u origin main") is None:
        print("❌ 推送失败，请检查:")
        print("1. GitHub仓库是否存在")
        print("2. 是否有推送权限")
        print("3. 网络连接是否正常")
        return False
    
    print("✅ 代码已推送到GitHub")
    return True

def update_readme_urls():
    """更新README中的URL"""
    repo_url = run_command("git remote get-url origin")
    if not repo_url:
        return
    
    # 提取仓库信息
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    
    # 读取README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换占位符URL
    content = content.replace('https://github.com/yourusername/http-requests', repo_url)
    
    # 写回文件
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ README中的URL已更新")

def main():
    """主函数"""
    print("🚀 GitHub仓库设置向导")
    print("=" * 50)
    
    # 检查Git
    if not check_git_installed():
        print("❌ 未找到Git，请先安装Git")
        print("下载地址: https://git-scm.com/downloads")
        sys.exit(1)
    
    # 初始化Git仓库
    if not init_git_repo():
        print("❌ Git仓库初始化失败")
        sys.exit(1)
    
    # 设置Git配置
    setup_git_config()
    
    # 添加远程仓库
    has_remote = add_remote_origin()
    
    # 更新README URLs
    if has_remote:
        update_readme_urls()
    
    # 创建初始提交
    if not initial_commit():
        print("❌ 初始提交失败")
        sys.exit(1)
    
    # 推送到GitHub
    if has_remote:
        if push_to_github():
            repo_url = run_command("git remote get-url origin")
            if repo_url:
                print(f"\n🎉 设置完成!")
                print(f"GitHub仓库: {repo_url}")
                
                # 询问是否打开浏览器
                open_browser = input("是否在浏览器中打开GitHub仓库? (Y/n): ").lower()
                if open_browser != 'n':
                    webbrowser.open(repo_url)
    
    print("\n📋 下一步:")
    print("1. 在GitHub仓库中启用Actions")
    print("2. 检查仓库设置中的权限")
    print("3. 运行 'python release.py v2.0.0' 创建第一个发布")

if __name__ == "__main__":
    main()
