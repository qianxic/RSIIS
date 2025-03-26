from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

class SampleMakingPage(QWidget):
    """批量影像解译页面类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # 页面标题
        title = QLabel("批量影像解译")
        title.setObjectName("page_title")
        main_layout.addWidget(title)
        
        # 页面副标题
        subtitle = QLabel("支持各类解译任务的批量化的图片、影像解译")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        main_layout.addWidget(subtitle)
        
        # 第一部分：通用批量解译
        self.create_general_section(main_layout)
        
        # 第二部分：批量变化检测
        self.create_change_detection_section(main_layout)
        
        # 添加弹性空间
        main_layout.addStretch()
    
    def create_general_section(self, parent_layout):
        """创建通用批量解译部分"""
        # 创建标题
        section_header = QLabel("分类\\分割\\检测")
        section_header.setObjectName("section_header")
        parent_layout.addWidget(section_header)
        
        # 创建内容框架
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        frame_layout = QVBoxLayout(content_frame)
        frame_layout.setContentsMargins(10, 10, 10, 10)
        
        # 操作区标题
        operation_title = QLabel("操作区")
        operation_title.setObjectName("section_title")
        frame_layout.addWidget(operation_title)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        # 导入按钮
        self.import_btn = QPushButton("导入遥感影像数据集")
        self.import_btn.setObjectName("operation_btn")
        self.import_btn.setFixedWidth(180)
        self.import_btn.setFixedHeight(40)
        self.import_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.import_btn)
        
        # 批量场景分类按钮
        self.scene_btn = QPushButton("场景分类")
        self.scene_btn.setObjectName("operation_btn")
        self.scene_btn.setFixedWidth(180)
        self.scene_btn.setFixedHeight(40)
        self.scene_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.scene_btn)
        
        # 批量语义分割按钮
        self.segment_btn = QPushButton("语义分割")
        self.segment_btn.setObjectName("operation_btn")
        self.segment_btn.setFixedWidth(180)
        self.segment_btn.setFixedHeight(40)
        self.segment_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.segment_btn)
        
        # 批量目标检测按钮
        self.detection_btn = QPushButton("目标检测")
        self.detection_btn.setObjectName("operation_btn")
        self.detection_btn.setFixedWidth(180)
        self.detection_btn.setFixedHeight(40)
        self.detection_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.detection_btn)
        
        # 导出按钮
        self.export_btn = QPushButton("导出解译结果")
        self.export_btn.setObjectName("operation_btn")
        self.export_btn.setFixedWidth(180)
        self.export_btn.setFixedHeight(40)
        self.export_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.export_btn)
        
        # 添加弹性空间
        button_layout.addStretch()
        
        # 添加按钮容器到框架
        frame_layout.addWidget(button_container)
        
        # 添加内容框架到父布局
        parent_layout.addWidget(content_frame)
    
    def create_change_detection_section(self, parent_layout):
        """创建批量变化检测部分"""
        # 创建标题
        section_header = QLabel("变化检测")
        section_header.setObjectName("section_header")
        parent_layout.addWidget(section_header)
        
        # 创建内容框架
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        frame_layout = QVBoxLayout(content_frame)
        frame_layout.setContentsMargins(10, 10, 10, 10)
        
        # 操作区标题
        operation_title = QLabel("操作区")
        operation_title.setObjectName("section_title")
        frame_layout.addWidget(operation_title)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        # 导入前期影像按钮
        self.cd_import_before_btn = QPushButton("导入前时相数据集")
        self.cd_import_before_btn.setObjectName("operation_btn")
        self.cd_import_before_btn.setFixedWidth(180)
        self.cd_import_before_btn.setFixedHeight(40)
        self.cd_import_before_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.cd_import_before_btn)
        
        # 导入后期影像按钮
        self.cd_import_after_btn = QPushButton("导入后时相数据集")
        self.cd_import_after_btn.setObjectName("operation_btn")
        self.cd_import_after_btn.setFixedWidth(180)
        self.cd_import_after_btn.setFixedHeight(40)
        self.cd_import_after_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.cd_import_after_btn)
        
        # 处理按钮
        self.cd_process_btn = QPushButton("开始变化检测")
        self.cd_process_btn.setObjectName("operation_btn")
        self.cd_process_btn.setFixedWidth(180)
        self.cd_process_btn.setFixedHeight(40)
        self.cd_process_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.cd_process_btn)
        
        # 导出结果按钮
        self.cd_export_btn = QPushButton("导出检测结果")
        self.cd_export_btn.setObjectName("operation_btn")
        self.cd_export_btn.setFixedWidth(180)
        self.cd_export_btn.setFixedHeight(40)
        self.cd_export_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.cd_export_btn)
        
        # 添加弹性空间
        button_layout.addStretch()
        
        # 添加按钮容器到框架
        frame_layout.addWidget(button_container)
        
        # 添加内容框架到父布局
        parent_layout.addWidget(content_frame)
    
    def connect_signals(self, controller):
        """连接信号到控制器"""
        # 通用批量解译信号
        self.import_btn.clicked.connect(controller.import_dataset)
        self.scene_btn.clicked.connect(controller.start_batch_scene_classification)
        self.segment_btn.clicked.connect(controller.start_batch_semantic_segmentation)
        self.detection_btn.clicked.connect(controller.start_batch_object_detection)
        self.export_btn.clicked.connect(controller.export_results)
        
        # 批量变化检测信号
        self.cd_import_before_btn.clicked.connect(controller.import_before_dataset)
        self.cd_import_after_btn.clicked.connect(controller.import_after_dataset)
        self.cd_process_btn.clicked.connect(controller.start_batch_change_detection)
        self.cd_export_btn.clicked.connect(controller.export_change_detection_results) 