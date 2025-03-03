# main.py
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, 
                              QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
                              QLineEdit, QComboBox, QLabel, QFileDialog)
from PySide6.QtCore import Qt, QPoint, QTimer
from modules.deepseek_api import DeepSeekHelper
from modules.notepad import NoteManager
from modules.shortcut_manager import ShortcutManager
import json
import os

class FloatingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化模块
        self.note_manager = NoteManager()
        self.shortcut_manager = ShortcutManager()
        self.load_config()
        self.ai_helper = DeepSeekHelper(self.config.get("deepseek_api_key", ""))
        self.init_ui()
        
        # 定时保存配置
        QTimer.singleShot(5000, self.save_config)

    def init_ui(self):
        # 窗口基础设置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("""
            QMainWindow { 
                background: rgba(245, 245, 245, 0.9); 
                border-radius: 10px; 
            }
            QTabWidget::pane { 
                border: 1px solid #CCCCCC; 
                background: rgba(245, 245, 245, 0.9); 
            }
            QTextEdit, QComboBox, QPushButton, QLabel {
                background: rgba(255, 255, 255, 0.8); 
                border-radius: 5px; 
            }
        """)

        # 主布局
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 创建各功能标签页
        self.create_ai_tab()
        self.create_note_tab()
        self.create_shortcut_tab()

    def create_ai_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # 模式选择
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["默认模式", "编程模式", "创意模式"])
        
        # 输入区域
        self.ai_input = QTextEdit()
        self.ai_input.setPlaceholderText("输入您的问题...")
        
        # 输出区域
        self.ai_output = QTextEdit()
        self.ai_output.setReadOnly(True)
        
        # 提交按钮
        btn_submit = QPushButton("提问")
        btn_submit.clicked.connect(self.handle_ai_query)

        layout.addWidget(QLabel("选择模式:"))
        layout.addWidget(self.mode_combo)
        layout.addWidget(QLabel("问题输入:"))
        layout.addWidget(self.ai_input)
        layout.addWidget(QLabel("回答输出:"))
        layout.addWidget(self.ai_output)
        layout.addWidget(btn_submit)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "AI助手")

    def create_note_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.note_edit = QTextEdit()
        btn_save = QPushButton("保存便签")
        btn_save.clicked.connect(lambda: self.note_manager.save_note(self.note_edit.toPlainText()))
        
        layout.addWidget(QLabel("今日便签:"))
        layout.addWidget(self.note_edit)
        layout.addWidget(btn_save)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "每日便签")

    def create_shortcut_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.shortcut_list = QComboBox()
        self.shortcut_list.addItems(self.shortcut_manager.shortcuts.keys())
        
        btn_add = QPushButton("添加快捷方式")
        btn_add.clicked.connect(self.add_shortcut)
        btn_open = QPushButton("打开选中项")
        btn_open.clicked.connect(lambda: self.shortcut_manager.open_shortcut(
            self.shortcut_list.currentText()
        ))
        
        layout.addWidget(QLabel("快捷方式列表:"))
        layout.addWidget(self.shortcut_list)
        layout.addWidget(btn_add)
        layout.addWidget(btn_open)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "快捷启动")

    def add_shortcut(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if path:
            name = os.path.basename(path).split('.')[0]
            self.shortcut_manager.add_shortcut(name, path)
            self.shortcut_list.addItem(name)

    def handle_ai_query(self):
        question = self.ai_input.toPlainText()
        mode_map = {
            "默认模式": "default",
            "编程模式": "code", 
            "创意模式": "creative"
        }
        response = self.ai_helper.ask(
            question, 
            mode=mode_map[self.mode_combo.currentText()]
        )
        self.ai_output.setText(response)
    
    # 配置文件相关
    def load_config(self):
        try:
            with open("config.json", "r") as f:
                self.config = json.load(f)
        except:
            self.config = {"deepseek_api_key": ""}

    def save_config(self):
        with open("config.json", "w") as f:
            json.dump(self.config, f)

    # 窗口拖拽功能
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FloatingWindow()
    window.show()
    sys.exit(app.exec())