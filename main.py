import sys
import json
import time
import os
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QLineEdit, QTextEdit, 
                             QPushButton, QLabel, QTabWidget, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QSplitter, QListWidget,
                             QStatusBar, QMenuBar, QFileDialog, QMessageBox,
                             QProgressBar, QFrame, QScrollArea, QGroupBox,
                             QGridLayout, QSpinBox, QCheckBox)
from PySide6.QtCore import Qt, QThread, Signal as QSignal, QTimer
from PySide6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor
import requests

class RequestThread(QThread):
    """异步请求线程"""
    finished = QSignal(dict)
    error = QSignal(str)
    
    def __init__(self, method, url, headers, data, timeout=30):
        super().__init__()
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        self.timeout = timeout
        
    def run(self):
        try:
            start_time = time.time()
            
            if self.method in ["POST", "PUT", "PATCH"]:
                if isinstance(self.data, dict):
                    response = requests.request(
                        method=self.method,
                        url=self.url,
                        headers=self.headers,
                        json=self.data,
                        timeout=self.timeout
                    )
                else:
                    response = requests.request(
                        method=self.method,
                        url=self.url,
                        headers=self.headers,
                        data=self.data,
                        timeout=self.timeout
                    )
            else:
                response = requests.request(
                    method=self.method,
                    url=self.url,
                    headers=self.headers,
                    timeout=self.timeout
                )
            
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)  # 毫秒
            
            result = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'text': response.text,
                'response_time': response_time,
                'url': response.url,
                'request_headers': self.headers,
                'request_method': self.method,
                'request_data': self.data
            }
            
            try:
                result['json'] = response.json()
            except:
                result['json'] = None
                
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))

class HTTPClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTTP 请求工具 - 专业版")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # 初始化变量
        self.request_history = []
        self.current_request_thread = None
        
        # 设置应用样式
        self.setStyleSheet(self.get_app_stylesheet())
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 创建主界面
        self.create_main_interface()
        
        # 添加默认请求头
        self.add_default_headers()
        
        # 加载历史记录
        self.load_history()
    
    def get_app_stylesheet(self):
        return """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
            background-color: white;
        }
        
        QTabWidget::tab-bar {
            alignment: left;
        }
        
        QTabBar::tab {
            background-color: #e1e1e1;
            border: 1px solid #c0c0c0;
            padding: 8px 16px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            border-bottom-color: white;
        }
        
        QTabBar::tab:hover {
            background-color: #f0f0f0;
        }
        
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #106ebe;
        }
        
        QPushButton:pressed {
            background-color: #005a9e;
        }
        
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
        
        QLineEdit {
            border: 1px solid #ccc;
            padding: 8px;
            border-radius: 4px;
            background-color: white;
        }
        
        QLineEdit:focus {
            border-color: #0078d4;
        }
        
        QComboBox {
            border: 1px solid #ccc;
            padding: 8px;
            border-radius: 4px;
            background-color: white;
            min-width: 100px;
        }
        
        QComboBox:focus {
            border-color: #0078d4;
        }
        
        QTextEdit {
            border: 1px solid #ccc;
            background-color: white;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        
        QTableWidget {
            border: 1px solid #ccc;
            background-color: white;
            gridline-color: #e0e0e0;
        }
        
        QTableWidget::item {
            padding: 8px;
        }
        
        QListWidget {
            border: 1px solid #ccc;
            background-color: white;
        }
        
        QListWidget::item {
            padding: 8px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        QListWidget::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QLabel {
            color: #333;
        }
        """
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        save_action = file_menu.addAction('保存请求')
        save_action.triggered.connect(self.save_request)
        
        load_action = file_menu.addAction('加载请求')
        load_action.triggered.connect(self.load_request)
        
        file_menu.addSeparator()
        
        clear_history_action = file_menu.addAction('清空历史')
        clear_history_action.triggered.connect(self.clear_history)
        
        # 工具菜单
        tools_menu = menubar.addMenu('工具')
        
        format_json_action = tools_menu.addAction('格式化JSON')
        format_json_action.triggered.connect(self.format_json)
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        self.status_bar.showMessage('就绪')
    
    def create_main_interface(self):
        # 创建主分割器
        main_splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(main_splitter)
        
        # 左侧面板 - 历史记录
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # 右侧面板 - 主要功能区
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # 设置分割器比例
        main_splitter.setSizes([300, 900])
    
    def create_left_panel(self):
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # 历史记录组
        history_group = QGroupBox("请求历史")
        history_layout = QVBoxLayout(history_group)
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_from_history)
        history_layout.addWidget(self.history_list)
        
        # 历史记录操作按钮
        history_buttons_layout = QHBoxLayout()
        
        clear_btn = QPushButton("清空")
        clear_btn.clicked.connect(self.clear_history)
        clear_btn.setStyleSheet("QPushButton { background-color: #dc3545; } QPushButton:hover { background-color: #c82333; }")
        
        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(self.delete_history_item)
        delete_btn.setStyleSheet("QPushButton { background-color: #fd7e14; } QPushButton:hover { background-color: #e8690b; }")
        
        history_buttons_layout.addWidget(delete_btn)
        history_buttons_layout.addWidget(clear_btn)
        
        history_layout.addLayout(history_buttons_layout)
        left_layout.addWidget(history_group)
        
        return left_widget
    
    def create_right_panel(self):
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 请求配置区域
        request_group = QGroupBox("请求配置")
        request_layout = QVBoxLayout(request_group)
        
        # 第一行：方法和URL
        first_row = QHBoxLayout()
        
        # 请求方法
        method_label = QLabel("方法:")
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
        self.method_combo.setMinimumWidth(100)
        
        # URL输入
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("请输入完整的URL地址")
        
        first_row.addWidget(method_label)
        first_row.addWidget(self.method_combo)
        first_row.addWidget(url_label)
        first_row.addWidget(self.url_input)
        
        request_layout.addLayout(first_row)
        
        # 第二行：超时设置和发送按钮
        second_row = QHBoxLayout()
        
        timeout_label = QLabel("超时(秒):")
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 300)
        self.timeout_spin.setValue(30)
        self.timeout_spin.setMinimumWidth(80)
        
        # 发送按钮
        self.send_button = QPushButton("发送请求")
        self.send_button.clicked.connect(self.send_request)
        self.send_button.setMinimumHeight(40)
        
        # 保存按钮
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_request)
        save_button.setStyleSheet("QPushButton { background-color: #28a745; } QPushButton:hover { background-color: #218838; }")
        
        second_row.addWidget(timeout_label)
        second_row.addWidget(self.timeout_spin)
        second_row.addStretch()
        second_row.addWidget(save_button)
        second_row.addWidget(self.send_button)
        
        request_layout.addLayout(second_row)
        right_layout.addWidget(request_group)
        
        # 标签页区域
        self.tab_widget = QTabWidget()
        
        # 请求头标签页
        headers_widget = self.create_headers_tab()
        self.tab_widget.addTab(headers_widget, "请求头")
        
        # 请求体标签页
        self.body_edit = QTextEdit()
        self.body_edit.setPlaceholderText("请输入请求体内容（JSON、XML、文本等）")
        self.tab_widget.addTab(self.body_edit, "请求体")
        
        # 响应标签页
        response_widget = self.create_response_tab()
        self.tab_widget.addTab(response_widget, "响应")
        
        right_layout.addWidget(self.tab_widget)
        
        return right_widget
    
    def create_headers_tab(self):
        headers_widget = QWidget()
        headers_layout = QVBoxLayout(headers_widget)
        
        # 请求头操作按钮
        headers_buttons_layout = QHBoxLayout()
        
        add_header_btn = QPushButton("添加请求头")
        add_header_btn.clicked.connect(self.add_header_row)
        add_header_btn.setStyleSheet("QPushButton { background-color: #28a745; } QPushButton:hover { background-color: #218838; }")
        
        remove_header_btn = QPushButton("删除选中")
        remove_header_btn.clicked.connect(self.remove_selected_headers)
        remove_header_btn.setStyleSheet("QPushButton { background-color: #dc3545; } QPushButton:hover { background-color: #c82333; }")
        
        headers_buttons_layout.addWidget(add_header_btn)
        headers_buttons_layout.addWidget(remove_header_btn)
        headers_buttons_layout.addStretch()
        
        headers_layout.addLayout(headers_buttons_layout)
        
        # 请求头表格
        self.headers_table = QTableWidget()
        self.headers_table.setColumnCount(3)
        self.headers_table.setHorizontalHeaderLabels(["启用", "Key", "Value"])
        self.headers_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.headers_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.headers_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
        headers_layout.addWidget(self.headers_table)
        
        return headers_widget
    
    def create_response_tab(self):
        response_widget = QWidget()
        response_layout = QVBoxLayout(response_widget)
        
        # 响应信息栏
        response_info_layout = QHBoxLayout()
        
        self.status_label = QLabel("状态: 未发送")
        self.time_label = QLabel("响应时间: -")
        self.size_label = QLabel("大小: -")
        
        response_info_layout.addWidget(self.status_label)
        response_info_layout.addWidget(self.time_label)
        response_info_layout.addWidget(self.size_label)
        response_info_layout.addStretch()
        
        # 格式化按钮
        format_btn = QPushButton("格式化JSON")
        format_btn.clicked.connect(self.format_response_json)
        format_btn.setStyleSheet("QPushButton { background-color: #17a2b8; } QPushButton:hover { background-color: #138496; }")
        response_info_layout.addWidget(format_btn)
        
        response_layout.addLayout(response_info_layout)
        
        # 响应内容
        self.response_edit = QTextEdit()
        self.response_edit.setReadOnly(True)
        self.response_edit.setPlaceholderText("响应内容将在这里显示...")
        response_layout.addWidget(self.response_edit)
        
        return response_widget
    
    def add_default_headers(self):
        default_headers = [
            ("Content-Type", "application/json"),
            ("Accept", "application/json"),
            ("User-Agent", "HTTP-Client/1.0")
        ]
        self.headers_table.setRowCount(len(default_headers))
        for i, (key, value) in enumerate(default_headers):
            # 启用复选框
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            self.headers_table.setCellWidget(i, 0, checkbox)
            
            # Key和Value
            self.headers_table.setItem(i, 1, QTableWidgetItem(key))
            self.headers_table.setItem(i, 2, QTableWidgetItem(value))
    
    def add_header_row(self):
        """添加新的请求头行"""
        row_count = self.headers_table.rowCount()
        self.headers_table.insertRow(row_count)
        
        # 添加启用复选框
        checkbox = QCheckBox()
        checkbox.setChecked(True)
        self.headers_table.setCellWidget(row_count, 0, checkbox)
        
        # 添加空的Key和Value
        self.headers_table.setItem(row_count, 1, QTableWidgetItem(""))
        self.headers_table.setItem(row_count, 2, QTableWidgetItem(""))
    
    def remove_selected_headers(self):
        """删除选中的请求头"""
        selected_rows = set()
        for item in self.headers_table.selectedItems():
            selected_rows.add(item.row())
        
        for row in sorted(selected_rows, reverse=True):
            self.headers_table.removeRow(row)
    
    def format_json(self):
        """格式化当前标签页的JSON内容"""
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 1:  # 请求体标签页
            self.format_body_json()
        elif current_tab == 2:  # 响应标签页
            self.format_response_json()
    
    def format_body_json(self):
        """格式化请求体JSON"""
        try:
            text = self.body_edit.toPlainText()
            if text.strip():
                parsed = json.loads(text)
                formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
                self.body_edit.setPlainText(formatted)
                self.status_bar.showMessage("JSON格式化成功", 2000)
        except json.JSONDecodeError as e:
            QMessageBox.warning(self, "JSON格式错误", f"无法解析JSON: {str(e)}")
    
    def format_response_json(self):
        """格式化响应JSON"""
        try:
            text = self.response_edit.toPlainText()
            # 尝试从响应文本中提取JSON部分
            lines = text.split('\n')
            json_start = -1
            for i, line in enumerate(lines):
                if line.strip().startswith('{') or line.strip().startswith('['):
                    json_start = i
                    break
            
            if json_start >= 0:
                json_text = '\n'.join(lines[json_start:])
                parsed = json.loads(json_text)
                formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
                
                # 重新组合响应文本
                header_text = '\n'.join(lines[:json_start])
                self.response_edit.setPlainText(header_text + formatted)
                self.status_bar.showMessage("响应JSON格式化成功", 2000)
        except (json.JSONDecodeError, IndexError):
            QMessageBox.warning(self, "格式化失败", "响应内容不包含有效的JSON")
    
    def save_request(self):
        """保存当前请求配置"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存请求", "", "JSON文件 (*.json)"
        )
        
        if file_path:
            request_data = {
                'method': self.method_combo.currentText(),
                'url': self.url_input.text(),
                'headers': self.get_headers(),
                'body': self.body_edit.toPlainText(),
                'timeout': self.timeout_spin.value()
            }
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(request_data, f, indent=2, ensure_ascii=False)
                self.status_bar.showMessage(f"请求已保存到 {file_path}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "保存失败", f"无法保存文件: {str(e)}")
    
    def load_request(self):
        """加载请求配置"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "加载请求", "", "JSON文件 (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    request_data = json.load(f)
                
                # 设置界面数据
                self.method_combo.setCurrentText(request_data.get('method', 'GET'))
                self.url_input.setText(request_data.get('url', ''))
                self.body_edit.setPlainText(request_data.get('body', ''))
                self.timeout_spin.setValue(request_data.get('timeout', 30))
                
                # 设置请求头
                headers = request_data.get('headers', {})
                self.load_headers(headers)
                
                self.status_bar.showMessage(f"请求已从 {file_path} 加载", 3000)
            except Exception as e:
                QMessageBox.critical(self, "加载失败", f"无法加载文件: {str(e)}")
    
    def load_headers(self, headers_dict):
        """加载请求头到表格"""
        self.headers_table.setRowCount(0)
        
        for key, value in headers_dict.items():
            row_count = self.headers_table.rowCount()
            self.headers_table.insertRow(row_count)
            
            # 启用复选框
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            self.headers_table.setCellWidget(row_count, 0, checkbox)
            
            # Key和Value
            self.headers_table.setItem(row_count, 1, QTableWidgetItem(key))
            self.headers_table.setItem(row_count, 2, QTableWidgetItem(value))
    
    def clear_history(self):
        """清空历史记录"""
        reply = QMessageBox.question(
            self, "确认清空", "确定要清空所有历史记录吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.request_history.clear()
            self.history_list.clear()
            self.save_history()
            self.status_bar.showMessage("历史记录已清空", 2000)
    
    def delete_history_item(self):
        """删除选中的历史记录项"""
        current_row = self.history_list.currentRow()
        if current_row >= 0:
            self.history_list.takeItem(current_row)
            if current_row < len(self.request_history):
                del self.request_history[current_row]
                self.save_history()
                self.status_bar.showMessage("历史记录项已删除", 2000)
    
    def load_from_history(self, item):
        """从历史记录加载请求"""
        row = self.history_list.row(item)
        if row < len(self.request_history):
            request_data = self.request_history[row]
            
            self.method_combo.setCurrentText(request_data.get('method', 'GET'))
            self.url_input.setText(request_data.get('url', ''))
            self.body_edit.setPlainText(request_data.get('body', ''))
            self.timeout_spin.setValue(request_data.get('timeout', 30))
            
            # 加载请求头
            headers = request_data.get('headers', {})
            self.load_headers(headers)
            
            self.status_bar.showMessage("已从历史记录加载请求", 2000)
    
    def save_history(self):
        """保存历史记录到文件"""
        try:
            history_file = os.path.join(os.path.expanduser('~'), '.http_client_history.json')
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.request_history, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # 静默失败
    
    def load_history(self):
        """从文件加载历史记录"""
        try:
            history_file = os.path.join(os.path.expanduser('~'), '.http_client_history.json')
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.request_history = json.load(f)
                
                # 更新历史列表显示
                self.update_history_list()
        except Exception:
            self.request_history = []
    
    def update_history_list(self):
        """更新历史记录列表显示"""
        self.history_list.clear()
        for request in self.request_history:
            method = request.get('method', 'GET')
            url = request.get('url', '')
            timestamp = request.get('timestamp', '')
            
            # 截断长URL
            display_url = url if len(url) <= 50 else url[:47] + '...'
            display_text = f"{method} {display_url}\n{timestamp}"
            
            self.history_list.addItem(display_text)
    
    def add_to_history(self, method, url, headers, body, timeout):
        """添加请求到历史记录"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        request_data = {
            'method': method,
            'url': url,
            'headers': headers,
            'body': body,
            'timeout': timeout,
            'timestamp': timestamp
        }
        
        # 避免重复记录
        for existing in self.request_history:
            if (existing.get('method') == method and 
                existing.get('url') == url and 
                existing.get('body') == body):
                return
        
        self.request_history.insert(0, request_data)
        
        # 限制历史记录数量
        if len(self.request_history) > 50:
            self.request_history = self.request_history[:50]
        
        self.update_history_list()
        self.save_history()
    
    def get_headers(self):
        """获取启用的请求头"""
        headers = {}
        for row in range(self.headers_table.rowCount()):
            # 检查是否启用
            checkbox = self.headers_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                key_item = self.headers_table.item(row, 1)
                value_item = self.headers_table.item(row, 2)
                if key_item and value_item and key_item.text().strip() and value_item.text().strip():
                    headers[key_item.text().strip()] = value_item.text().strip()
        return headers
    
    def send_request(self):
        """发送HTTP请求"""
        url = self.url_input.text().strip()
        method = self.method_combo.currentText()
        headers = self.get_headers()
        timeout = self.timeout_spin.value()
        
        # 验证URL
        if not url:
            QMessageBox.warning(self, "输入错误", "请输入URL")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_input.setText(url)
        
        # 准备请求体数据
        body = self.body_edit.toPlainText().strip()
        data = None
        
        if method in ["POST", "PUT", "PATCH"] and body:
            try:
                # 尝试解析为JSON
                data = json.loads(body)
            except json.JSONDecodeError:
                # 如果不是JSON，作为文本处理
                data = body
        
        # 停止之前的请求
        if self.current_request_thread and self.current_request_thread.isRunning():
            self.current_request_thread.terminate()
            self.current_request_thread.wait()
        
        # 更新UI状态
        self.send_button.setEnabled(False)
        self.send_button.setText("发送中...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 无限进度条
        self.status_bar.showMessage("正在发送请求...")
        
        # 清空之前的响应
        self.response_edit.clear()
        self.status_label.setText("状态: 发送中...")
        self.time_label.setText("响应时间: -")
        self.size_label.setText("大小: -")
        
        # 切换到响应标签页
        self.tab_widget.setCurrentIndex(2)
        
        # 创建并启动请求线程
        self.current_request_thread = RequestThread(method, url, headers, data, timeout)
        self.current_request_thread.finished.connect(self.on_request_finished)
        self.current_request_thread.error.connect(self.on_request_error)
        self.current_request_thread.start()
        
        # 添加到历史记录
        self.add_to_history(method, url, headers, body, timeout)
    
    def on_request_finished(self, result):
        """请求完成处理"""
        # 恢复UI状态
        self.send_button.setEnabled(True)
        self.send_button.setText("发送请求")
        self.progress_bar.setVisible(False)
        
        # 显示响应信息
        status_code = result['status_code']
        response_time = result['response_time']
        response_text = result['text']
        response_headers = result['headers']
        
        # 更新状态标签
        status_color = self.get_status_color(status_code)
        self.status_label.setText(f"状态: <span style='color: {status_color}; font-weight: bold;'>{status_code}</span>")
        self.time_label.setText(f"响应时间: {response_time} ms")
        
        # 计算响应大小
        response_size = len(response_text.encode('utf-8'))
        size_text = self.format_size(response_size)
        self.size_label.setText(f"大小: {size_text}")
        
        # 显示响应内容
        self.response_edit.clear()
        
        # 响应头
        self.response_edit.append("=== 响应头 ===")
        for key, value in response_headers.items():
            self.response_edit.append(f"{key}: {value}")
        
        self.response_edit.append("\n=== 响应体 ===")
        
        # 尝试格式化JSON响应
        if result['json']:
            try:
                formatted_json = json.dumps(result['json'], indent=2, ensure_ascii=False)
                self.response_edit.append(formatted_json)
            except:
                self.response_edit.append(response_text)
        else:
            self.response_edit.append(response_text)
        
        # 更新状态栏
        self.status_bar.showMessage(f"请求完成 - {status_code} ({response_time} ms)", 5000)
    
    def on_request_error(self, error_message):
        """请求错误处理"""
        # 恢复UI状态
        self.send_button.setEnabled(True)
        self.send_button.setText("发送请求")
        self.progress_bar.setVisible(False)
        
        # 显示错误信息
        self.status_label.setText("状态: <span style='color: #dc3545; font-weight: bold;'>错误</span>")
        self.time_label.setText("响应时间: -")
        self.size_label.setText("大小: -")
        
        self.response_edit.clear()
        self.response_edit.append("=== 请求错误 ===")
        self.response_edit.append(f"错误信息: {error_message}")
        
        # 常见错误提示
        if "Connection" in error_message:
            self.response_edit.append("\n可能的原因:")
            self.response_edit.append("• 网络连接问题")
            self.response_edit.append("• 服务器无法访问")
            self.response_edit.append("• URL地址错误")
        elif "timeout" in error_message.lower():
            self.response_edit.append("\n可能的原因:")
            self.response_edit.append("• 请求超时")
            self.response_edit.append("• 服务器响应缓慢")
            self.response_edit.append("• 网络延迟过高")
        
        self.status_bar.showMessage(f"请求失败: {error_message}", 5000)
    
    def get_status_color(self, status_code):
        """根据状态码获取颜色"""
        if 200 <= status_code < 300:
            return "#28a745"  # 绿色 - 成功
        elif 300 <= status_code < 400:
            return "#17a2b8"  # 蓝色 - 重定向
        elif 400 <= status_code < 500:
            return "#fd7e14"  # 橙色 - 客户端错误
        else:
            return "#dc3545"  # 红色 - 服务器错误
    
    def format_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HTTPClient()
    window.show()
    sys.exit(app.exec())