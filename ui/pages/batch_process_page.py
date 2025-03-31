from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QPushButton, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

class BatchProcessPage(QWidget):
    """批量处理管理页面类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        # 创建主布局
        layout = QVBoxLayout(self)
        
        # 页面标题
        title = QLabel("批量处理管理")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        # 页面副标题
        subtitle = QLabel("管理批量处理任务，包括分类、分割、检测和变化检测等")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        # 常规批量处理任务创建区域
        self.create_task_creation_section(layout)
        
        # 变化检测专用任务创建区域
        self.create_change_detection_section(layout)
        
        # 添加弹性空间
        layout.addStretch()
    
    def create_task_creation_section(self, parent_layout):
        """创建常规任务创建区域（分类、分割、检测）"""
        # 创建内容框架
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        # 创建标题
        section_title = QLabel("分类 / 分割 / 检测")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 按钮容器
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        # 选择输入目录按钮
        self.select_input_btn = QPushButton("选择输入目录")
        self.select_input_btn.setObjectName("operation_btn")
        self.select_input_btn.setFixedWidth(180)
        self.select_input_btn.setFixedHeight(40)
        self.select_input_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.select_input_btn)
        
        # 选择输出目录按钮
        self.select_output_btn = QPushButton("选择输出目录")
        self.select_output_btn.setObjectName("operation_btn")
        self.select_output_btn.setFixedWidth(180)
        self.select_output_btn.setFixedHeight(40)
        self.select_output_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.select_output_btn)
        
        # 创建常规任务按钮（不包含变化检测）
        task_buttons = [
            ("场景分类", "classification"),
            ("语义分割", "segmentation"),
            ("目标检测", "detection")
        ]
        
        for text, task_type in task_buttons:
            btn = QPushButton(f"开始{text}任务")
            btn.setObjectName("operation_btn")
            btn.setFixedWidth(180)
            btn.setFixedHeight(40)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setProperty("task_type", task_type)
            button_layout.addWidget(btn)
            
            # 保存按钮引用
            setattr(self, f"create_{task_type}_btn", btn)
        
        # 添加弹性空间
        button_layout.addStretch()
        
        # 添加按钮容器到框架
        content_layout.addWidget(button_container)
        
        # 添加内容框架到父布局
        parent_layout.addWidget(content_frame)
    
    def create_change_detection_section(self, parent_layout):
        """创建变化检测专用任务创建区域"""
        # 创建内容框架
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        # 创建标题
        section_title = QLabel("变化检测")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 按钮容器
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        # 选择前期影像目录按钮
        self.select_before_btn = QPushButton("选择前期影像目录")
        self.select_before_btn.setObjectName("operation_btn")
        self.select_before_btn.setFixedWidth(180)
        self.select_before_btn.setFixedHeight(40)
        self.select_before_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.select_before_btn)
        
        # 选择后期影像目录按钮
        self.select_after_btn = QPushButton("选择后期影像目录")
        self.select_after_btn.setObjectName("operation_btn")
        self.select_after_btn.setFixedWidth(180)
        self.select_after_btn.setFixedHeight(40)
        self.select_after_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.select_after_btn)
        
        # 选择变化检测输出目录按钮
        self.select_change_output_btn = QPushButton("选择输出目录")
        self.select_change_output_btn.setObjectName("operation_btn")
        self.select_change_output_btn.setFixedWidth(180)
        self.select_change_output_btn.setFixedHeight(40)
        self.select_change_output_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.select_change_output_btn)
        
        # 创建变化检测任务按钮
        self.create_change_detection_btn = QPushButton("开始变化检测任务")
        self.create_change_detection_btn.setObjectName("operation_btn")
        self.create_change_detection_btn.setFixedWidth(180)
        self.create_change_detection_btn.setFixedHeight(40)
        self.create_change_detection_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.create_change_detection_btn.setProperty("task_type", "change_detection")
        button_layout.addWidget(self.create_change_detection_btn)
        
        # 添加弹性空间
        button_layout.addStretch()
        
        # 添加按钮容器到框架
        content_layout.addWidget(button_container)
        
        # 添加内容框架到父布局
        parent_layout.addWidget(content_frame)
    
    def connect_signals(self, controller):
        """连接信号到控制器"""
        # 连接常规任务目录选择按钮
        self.select_input_btn.clicked.connect(controller.select_input_directory)
        self.select_output_btn.clicked.connect(controller.select_output_directory)
        
        # 连接变化检测目录选择按钮
        self.select_before_btn.clicked.connect(controller.select_before_directory)
        self.select_after_btn.clicked.connect(controller.select_after_directory)
        self.select_change_output_btn.clicked.connect(controller.select_output_directory)
        
        # 连接常规任务创建按钮
        self.create_classification_btn.clicked.connect(lambda: controller.create_batch_task("classification"))
        self.create_segmentation_btn.clicked.connect(lambda: controller.create_batch_task("segmentation"))
        self.create_detection_btn.clicked.connect(lambda: controller.create_batch_task("detection"))
        
        # 连接变化检测任务创建按钮
        self.create_change_detection_btn.clicked.connect(lambda: controller.create_batch_task("change_detection")) 