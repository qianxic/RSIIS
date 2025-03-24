from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

from ui.widgets.selectable_label import SelectableLabel

class FishnetPage(QWidget):
    """渔网分割页面类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        layout = QVBoxLayout(self)
        
        title = QLabel("渔网分割")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("对遥感影像进行网格化处理，便于精确分析")
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
        
        # 导入按钮
        self.import_btn = QPushButton("导入遥感影像")
        self.import_btn.setObjectName("operation_btn")
        self.import_btn.setFixedWidth(180)
        self.import_btn.setFixedHeight(40)
        self.import_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.import_btn)
        
        # 设置网格参数按钮
        self.grid_btn = QPushButton("设置网格参数")
        self.grid_btn.setObjectName("operation_btn")
        self.grid_btn.setFixedWidth(180)
        self.grid_btn.setFixedHeight(40)
        self.grid_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.grid_btn)
        
        # 开始分割按钮
        self.process_btn = QPushButton("开始分割")
        self.process_btn.setObjectName("operation_btn")
        self.process_btn.setFixedWidth(180)
        self.process_btn.setFixedHeight(40)
        self.process_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.process_btn)
        
        # 导出结果按钮
        self.export_btn = QPushButton("导出分割结果")
        self.export_btn.setObjectName("operation_btn")
        self.export_btn.setFixedWidth(180)
        self.export_btn.setFixedHeight(40)
        self.export_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.export_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
        # 添加网格参数说明区域
        settings_section = QLabel("网格参数说明")
        settings_section.setObjectName("section_title")
        content_layout.addWidget(settings_section)
        
        settings_frame = QFrame()
        settings_frame.setObjectName("settings_area")
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setContentsMargins(10, 10, 10, 10)
        
        # 添加网格参数说明
        grid_params_text = """渔网分割参数说明:
1. 网格大小 - 定义每个网格的像素宽度和高度，推荐值为256×256或512×512像素
2. 重叠像素 - 相邻网格之间的重叠像素数，用于避免边界效应，推荐值为32或64像素
3. 注意事项 - 选择合适的网格大小可以平衡计算效率和精度，较大的重叠像素有助于提高边界区域的识别精度"""
        
        grid_params_desc = SelectableLabel(grid_params_text)
        grid_params_desc.setWordWrap(True)
        grid_params_desc.setObjectName("desc_text")
        settings_layout.addWidget(grid_params_desc)
        
        content_layout.addWidget(settings_frame)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
    def connect_signals(self, controller):
        """连接信号到控制器"""
        self.import_btn.clicked.connect(controller.import_image)
        self.grid_btn.clicked.connect(controller.set_grid_params)
        self.process_btn.clicked.connect(controller.start_fishnet)
        self.export_btn.clicked.connect(controller.export_result) 