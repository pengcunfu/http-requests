# HTTP请求解析工具使用说明

## 功能简介

这个工具可以直接解析原始的HTTP请求文本，自动提取方法、URL、请求头和请求体，并填充到主界面中。

## 使用方法

### 1. 打开导入对话框

- 运行程序后，点击菜单栏 **工具 → 导入原始请求**

### 2. 粘贴原始HTTP请求

在对话框中粘贴从浏览器开发者工具、Postman、Fiddler等工具复制的原始HTTP请求。

**支持的格式示例：**

```
GET /admin/inspection.Report/getInspectionData HTTP/1.1
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Host: localhost:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
ba-user-token: 2d7f3b9f-f256-4f1a-b338-ed4f2bc117c5
```

或带请求体的POST请求：

```
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer token123

{"username": "test", "email": "test@example.com"}
```

### 3. 解析请求

- 点击 **解析** 按钮
- 在"解析预览"区域查看解析结果
- 确认无误后，点击 **导入** 按钮

### 4. 发送请求

导入后，所有数据会自动填充到主界面：
- 请求方法
- URL地址
- 所有请求头
- 请求体（如果有）

您可以直接点击"发送请求"按钮进行测试。

## 从浏览器复制HTTP请求

### Chrome/Edge开发者工具

1. 按 `F12` 打开开发者工具
2. 切换到 **Network（网络）** 标签
3. 执行要捕获的请求
4. 在请求列表中右键点击目标请求
5. 选择 **Copy → Copy as cURL (bash)** 或直接复制请求头
6. 粘贴到工具中

### Firefox开发者工具

1. 按 `F12` 打开开发者工具
2. 切换到 **网络** 标签
3. 找到目标请求，右键点击
4. 选择 **复制 → 复制为cURL** 或 **复制请求头**
5. 粘贴到工具中

## 支持的HTTP方法

- GET
- POST
- PUT
- DELETE
- PATCH
- HEAD
- OPTIONS
- CONNECT
- TRACE

## 功能特性

✅ 自动识别HTTP方法和路径
✅ 智能判断HTTP/HTTPS协议
✅ 解析所有请求头
✅ 支持带请求体的请求
✅ 错误提示和验证
✅ 预览解析结果

## 技术实现

### 核心模块

- `http_parser.py` - HTTP请求解析器
- `HTTPRequestParser` - 解析器主类
- `RawRequestDialog` - 导入对话框

### 测试

运行测试脚本验证解析功能：

```bash
python test_parser.py
```

## 示例

### 示例1：GET请求

**输入：**
```
GET /admin/inspection.Report/getInspectionData HTTP/1.1
Host: localhost:8000
Accept: application/json
```

**解析结果：**
- 方法：GET
- URL：http://localhost:8000/admin/inspection.Report/getInspectionData
- 请求头：Host, Accept

### 示例2：POST请求

**输入：**
```
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json

{"name": "张三", "age": 25}
```

**解析结果：**
- 方法：POST
- URL：http://api.example.com/api/users
- 请求头：Host, Content-Type
- 请求体：{"name": "张三", "age": 25}

## 常见问题

**Q: 为什么我的请求解析失败？**
A: 请确保请求文本格式正确，至少包含请求行（方法、路径、协议）。

**Q: 支持HTTPS吗？**
A: 支持。解析器会根据Host中的端口号（443）或主机名自动判断协议。

**Q: 可以解析cURL命令吗？**
A: 目前不直接支持cURL命令格式，需要转换为标准HTTP请求格式。

## 更新日志

### v1.0.0 (2025-11-21)
- 初始版本发布
- 支持基本HTTP请求解析
- 集成到主界面
- 添加测试用例
