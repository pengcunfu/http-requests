#!/usr/bin/env python3
"""
HTTP请求解析工具 - 主入口文件
"""
import sys
import os

# 添加app目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from PySide6.QtWidgets import QApplication
from app.main_gui import HTTPRequestParserGUI


def main():
    """主函数"""
    # 创建QApplication实例
    app = QApplication(sys.argv)

    # 设置应用程序名称
    app.setApplicationName("HTTP请求解析工具")
    app.setOrganizationName("PyTools")

    # 创建主窗口
    window = HTTPRequestParserGUI()
    window.show()

    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()