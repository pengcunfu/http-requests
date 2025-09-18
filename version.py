"""
版本信息管理
"""

__version__ = "2.0.0"
__author__ = "HTTP Client Team"
__email__ = "team@httpclient.dev"
__description__ = "一个功能丰富、界面美观的HTTP请求测试工具"
__url__ = "https://github.com/yourusername/http-requests"

# 版本历史
VERSION_HISTORY = {
    "2.0.0": {
        "date": "2024-12-18",
        "changes": [
            "全新的现代化界面设计",
            "添加异步请求处理",
            "新增历史记录功能",
            "支持配置保存和加载",
            "增强的错误处理和用户提示",
            "添加JSON格式化功能",
            "改进的请求头管理",
            "详细的响应信息显示"
        ]
    }
}

def get_version():
    """获取当前版本"""
    return __version__

def get_version_info():
    """获取详细版本信息"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "url": __url__
    }
