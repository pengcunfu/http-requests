# 🚀 GitHub + Nuitka 发布完整指南

这是一个完整的指南，教你如何将HTTP请求工具发布到GitHub并使用Nuitka编译。

## 📋 准备工作

### 1. 确保环境准备就绪
- Python 3.9+ 已安装
- Git 已安装并配置
- GitHub账户已创建

### 2. 检查项目文件
确保你的项目目录包含以下文件：
```
http-requests/
├── main.py                 # 主程序
├── version.py             # 版本信息
├── requirements.txt       # 基础依赖
├── requirements-dev.txt   # 开发依赖
├── build.py              # 构建脚本
├── release.py            # 发布脚本
├── setup_github.py       # GitHub设置助手
├── .gitignore            # Git忽略文件
├── .github/
│   └── workflows/
│       ├── ci.yml        # 持续集成
│       └── build-release.yml  # 构建发布
└── README.md             # 项目说明
```

## 🛠️ 第一步：设置GitHub仓库

### 方法一：使用自动化脚本（推荐）
```bash
python setup_github.py
```

这个脚本会自动：
1. 初始化Git仓库
2. 设置Git用户信息
3. 添加远程GitHub仓库
4. 创建初始提交
5. 推送代码到GitHub

### 方法二：手动设置

#### 1. 在GitHub上创建新仓库
1. 访问 https://github.com
2. 点击右上角的 "+" → "New repository"
3. 仓库名称：`http-requests`
4. 描述：`功能丰富的HTTP请求测试工具`
5. 选择 "Public"（或Private）
6. **不要**勾选 "Add a README file"
7. 点击 "Create repository"

#### 2. 本地初始化Git
```bash
# 初始化Git仓库
git init

# 设置用户信息（如果还没设置）
git config user.name "你的姓名"
git config user.email "你的邮箱"

# 添加远程仓库（替换为你的仓库URL）
git remote add origin https://github.com/你的用户名/http-requests.git

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: HTTP请求工具 v2.0.0"

# 推送到GitHub
git branch -M main
git push -u origin main
```

## 🔧 第二步：测试本地构建

在发布前，先测试本地构建是否正常：

### Windows
```bash
# 安装构建依赖
pip install -r requirements-dev.txt

# 创建应用图标（可选）
python create_icon.py

# 运行构建
build.bat
```

### Linux/macOS
```bash
# 安装构建依赖
pip3 install -r requirements-dev.txt

# 创建应用图标（可选）
python3 create_icon.py

# 运行构建
chmod +x build.sh
./build.sh
```

如果构建成功，你会在 `release/` 目录看到可执行文件。

## 🚀 第三步：发布第一个版本

### 方法一：使用发布脚本（推荐）
```bash
# Windows
release.bat v2.0.0

# Linux/macOS
python3 release.py v2.0.0
```

### 方法二：手动发布
```bash
# 1. 更新版本文件
# 编辑 version.py，确保版本号正确

# 2. 提交版本更新
git add version.py
git commit -m "Bump version to v2.0.0"

# 3. 创建标签
git tag -a v2.0.0 -m "Release v2.0.0"

# 4. 推送到GitHub
git push origin main
git push origin --tags
```

## 📦 第四步：监控构建过程

1. 推送标签后，访问你的GitHub仓库
2. 点击 "Actions" 标签页
3. 你会看到 "构建和发布" 工作流正在运行
4. 等待所有平台构建完成（通常需要10-20分钟）

## 🎉 第五步：检查发布结果

构建完成后：

1. 访问仓库的 "Releases" 页面
2. 你会看到新的发布 "HTTP请求工具 v2.0.0"
3. 发布包含三个平台的可执行文件：
   - `HTTP-Requests-Tool-Windows.zip`
   - `HTTP-Requests-Tool-Linux.tar.gz`
   - `HTTP-Requests-Tool-macOS.tar.gz`

## 🔄 后续版本发布

对于后续版本：

1. 完成代码更改
2. 测试功能
3. 运行发布脚本：
   ```bash
   python release.py v2.0.1
   ```
4. GitHub Actions会自动构建并发布

## 🛡️ 安全建议

1. **不要在代码中包含敏感信息**（API密钥、密码等）
2. **定期更新依赖**以修复安全漏洞
3. **为私有仓库设置适当的访问权限**

## 🐛 常见问题解决

### 构建失败
- 检查 requirements.txt 中的依赖版本
- 确保所有平台都支持你使用的依赖
- 查看GitHub Actions日志获取详细错误信息

### 推送失败
- 检查仓库URL是否正确
- 确认GitHub用户名和密码/Token
- 验证仓库访问权限

### Nuitka编译错误
- 更新Nuitka到最新版本
- 检查Python版本兼容性
- 简化代码依赖，避免复杂的包

## 📞 获取帮助

如果遇到问题：

1. 查看 [RELEASE_GUIDE.md](RELEASE_GUIDE.md) 详细发布说明
2. 检查GitHub Actions日志
3. 在项目仓库创建Issue
4. 查看Nuitka官方文档: https://nuitka.net/

## 🎯 下一步

- 设置自动化测试
- 添加代码质量检查
- 创建用户文档
- 收集用户反馈并改进

恭喜！你已经成功设置了完整的GitHub + Nuitka发布流程！ 🎉
