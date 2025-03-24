from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

class SegmentPage(QWidget):
    """语义分割页面类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        layout = QVBoxLayout(self)
        
        title = QLabel("语义分割")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("对遥感影像进行语义分割，像素级别区分不同地物类型")
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
        
        self.import_btn = QPushButton("导入遥感影像")
        self.import_btn.setObjectName("operation_btn")
        self.import_btn.setFixedWidth(180)
        self.import_btn.setFixedHeight(40)
        self.import_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.import_btn)
        
        self.process_btn = QPushButton("开始语义分割")
        self.process_btn.setObjectName("operation_btn")
        self.process_btn.setFixedWidth(180)
        self.process_btn.setFixedHeight(40)
        self.process_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.process_btn)
        
        self.export_btn = QPushButton("导出分割结果")
        self.export_btn.setObjectName("operation_btn")
        self.export_btn.setFixedWidth(180)
        self.export_btn.setFixedHeight(40)
        self.export_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.export_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
        layout.addWidget(content_frame)
        layout.addStretch()
    
    def connect_signals(self, controller):
        """连接信号到控制器"""
        self.import_btn.clicked.connect(controller.import_image)
        self.process_btn.clicked.connect(controller.start_segmentation)
        self.export_btn.clicked.connect(controller.export_result) 