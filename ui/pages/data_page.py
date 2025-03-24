from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

class DataPage(QWidget):
    """数据获取页面类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        layout = QVBoxLayout(self)
        
        title = QLabel("数据获取")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("获取遥感影像数据，支持多种来源和格式")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        # 在线下载按钮
        self.download_btn = QPushButton("在线下载")
        self.download_btn.setObjectName("operation_btn")
        self.download_btn.setFixedWidth(180)
        self.download_btn.setFixedHeight(40)
        self.download_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.download_btn)
        
        # 本地导入按钮
        self.import_btn = QPushButton("本地导入")
        self.import_btn.setObjectName("operation_btn")
        self.import_btn.setFixedWidth(180)
        self.import_btn.setFixedHeight(40)
        self.import_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.import_btn)
        
        # 数据管理按钮
        self.manage_btn = QPushButton("数据管理")
        self.manage_btn.setObjectName("operation_btn")
        self.manage_btn.setFixedWidth(180)
        self.manage_btn.setFixedHeight(40)
        self.manage_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.manage_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
        layout.addWidget(content_frame)
        layout.addStretch()
    
    def connect_signals(self, controller):
        """连接信号到控制器"""
        self.import_btn.clicked.connect(controller.import_local)
        self.download_btn.clicked.connect(controller.download_data)
        self.manage_btn.clicked.connect(controller.manage_data) 