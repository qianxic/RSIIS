from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QPushButton)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor

class SettingPage(QWidget):
    """设置页面类"""
    
    # 定义信号
    theme_changed = Signal(bool)  # 当主题更改时发射，True表示切换到暗色主题，False表示切换到亮色主题
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # 主题标志
        self.is_dark_theme = False
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        layout = QVBoxLayout(self)
        
        title = QLabel("设置")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("系统设置和参数配置")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("常规设置")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 常规设置内容区域
        settings_area = QFrame()
        settings_area.setObjectName("settings_area")
        settings_layout = QVBoxLayout(settings_area)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        self.theme_btn = QPushButton("切换到暗色主题")
        self.theme_btn.setObjectName("operation_btn")
        self.theme_btn.setFixedWidth(180)
        self.theme_btn.setFixedHeight(40)
        self.theme_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.theme_btn.clicked.connect(self.toggle_theme)
        button_layout.addWidget(self.theme_btn)
        
        self.auth_btn = QPushButton("账户与授权")
        self.auth_btn.setObjectName("operation_btn")
        self.auth_btn.setFixedWidth(180)
        self.auth_btn.setFixedHeight(40)
        self.auth_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.auth_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        settings_layout.addWidget(button_container)
        
        content_layout.addWidget(settings_area)
        
        # 添加关于部分
        section_title2 = QLabel("关于系统")
        section_title2.setObjectName("section_title")
        content_layout.addWidget(section_title2)
        
        about_frame = QFrame()
        about_frame.setObjectName("about_frame")
        content_layout.addWidget(about_frame)
        
        about_layout = QVBoxLayout(about_frame)
        
        self.about_text = QLabel("遥感影像智能解译系统 V1.0\n© 2023-2024 RSIIS团队 版权所有")
        self.about_text.setWordWrap(True)
        self.about_text.setObjectName("about_text")
        about_layout.addWidget(self.about_text)
        
        layout.addWidget(content_frame)
        layout.addStretch()
    
    def toggle_theme(self):
        """切换主题样式"""
        # 切换主题标志
        self.is_dark_theme = not self.is_dark_theme
        
        # 更新按钮文本
        if self.is_dark_theme:
            self.theme_btn.setText("切换到亮色主题")
        else:
            self.theme_btn.setText("切换到暗色主题")
        
        # 发送信号
        self.theme_changed.emit(self.is_dark_theme)
    
    def connect_signals(self, controller):
        """连接信号到控制器"""
        self.auth_btn.clicked.connect(controller.manage_account) 