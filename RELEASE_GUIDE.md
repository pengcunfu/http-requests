# 发布指南

本文档介绍如何使用GitHub发布HTTP请求工具的新版本。

## 🚀 快速发布

### 1. 准备工作
确保你的代码已经准备好并测试通过：
```bash
# 确保所有更改已提交
git status

# 如果有未提交的更改，先提交
git add .
git commit -m "准备发布 v2.0.1"
```

### 2. 发布新版本
使用自动化发布脚本：
```bash
# Windows
release.bat v2.0.1

# Linux/macOS
python3 release.py v2.0.1
```

这个脚本会：
- 更新 `version.py` 中的版本号
- 创建Git标签
- 推送到GitHub
- 触发自动化构建

### 3. 监控构建过程
1. 访问你的GitHub仓库
2. 点击 "Actions" 标签页
3. 查看 "构建和发布" 工作流的状态

## 🔧 手动发布

如果你更喜欢手动控制每个步骤：

### 1. 更新版本号
编辑 `version.py` 文件：
```python
__version__ = "2.0.1"  # 更新版本号
```

### 2. 提交更改
```bash
git add version.py
git commit -m "Bump version to v2.0.1"
```

### 3. 创建标签
```bash
git tag -a v2.0.1 -m "Release v2.0.1"
```

### 4. 推送到GitHub
```bash
git push origin main
git push origin --tags
```

### 5. 手动触发构建
1. 在GitHub仓库页面，点击 "Actions"
2. 选择 "构建和发布" 工作流
3. 点击 "Run workflow"
4. 输入版本号 `v2.0.1`
5. 点击 "Run workflow"

## 📦 构建结果

自动化构建完成后，会生成以下文件：
- `HTTP-Requests-Tool-Windows.zip` - Windows可执行文件
- `HTTP-Requests-Tool-Linux.tar.gz` - Linux可执行文件
- `HTTP-Requests-Tool-macOS.tar.gz` - macOS可执行文件

这些文件会自动发布到GitHub Releases页面。

## 🛠️ 本地构建测试

在发布前，建议先进行本地构建测试：

### Windows
```bash
build.bat
```

### Linux/macOS
```bash
./build.sh
```

构建成功后，在 `release/` 目录中会生成对应的可执行文件。

## 📋 发布清单

在发布前，确保以下事项已完成：

- [ ] 所有功能已测试
- [ ] 版本号已更新
- [ ] README.md 已更新
- [ ] 更新日志已完善
- [ ] 本地构建测试通过
- [ ] 所有更改已提交到Git

## 🐛 故障排除

### 构建失败
1. 检查GitHub Actions日志
2. 确认所有依赖正确安装
3. 验证Python版本兼容性

### 发布失败
1. 检查GitHub token权限
2. 确认标签格式正确（v1.2.3）
3. 验证仓库设置允许创建发布

### 权限问题
确保你有仓库的以下权限：
- 推送代码
- 创建标签
- 创建发布
- 上传构建产物

## 📞 支持

如果遇到发布相关问题，请：
1. 查看GitHub Actions日志
2. 检查本文档的故障排除部分
3. 在仓库中创建Issue寻求帮助
