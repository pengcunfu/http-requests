#!/usr/bin/env python3
"""
创建简单的应用图标
"""

from PySide6.QtGui import QPixmap, QPainter, QBrush, QColor, QFont
from PySide6.QtCore import Qt
import sys

def create_icon():
    """创建简单的HTTP图标"""
    # 创建64x64的图片
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    
    # 创建画笔
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # 绘制背景圆形
    painter.setBrush(QBrush(QColor(52, 152, 219)))  # 蓝色背景
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(4, 4, 56, 56)
    
    # 绘制HTTP文字
    painter.setPen(QColor(255, 255, 255))
    font = QFont("Arial", 12, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "HTTP")
    
    painter.end()
    
    # 保存为ICO文件（Windows）
    pixmap.save("icon.ico", "ICO")
    
    # 保存为PNG文件（通用）
    pixmap.save("icon.png", "PNG")
    
    print("✅ 图标文件已创建: icon.ico, icon.png")

if __name__ == "__main__":
    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication(sys.argv)
        create_icon()
        print("图标创建成功！")
    except ImportError:
        print("需要安装PySide6才能创建图标")
        print("pip install PySide6")
