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
        
        subtitle = QLabel("对图像/影像进行网格化处理，便于精确分析，支持常规图像和GeoTIFF格式")
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
        self.import_btn = QPushButton("导入图像/影像")
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
        
        # 清空缓存按钮
        self.clear_cache_btn = QPushButton("清空缓存")
        self.clear_cache_btn.setObjectName("operation_btn")
        self.clear_cache_btn.setFixedWidth(180)
        self.clear_cache_btn.setFixedHeight(40)
        self.clear_cache_btn.setCursor(QCursor(Qt.PointingHandCursor))
        button_layout.addWidget(self.clear_cache_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
    def connect_signals(self, controller):
        """连接信号到控制器"""
        self.import_btn.clicked.connect(controller.import_image)
        self.grid_btn.clicked.connect(controller.set_grid_params)
        self.process_btn.clicked.connect(controller.start_fishnet)
        self.export_btn.clicked.connect(controller.export_result)
        self.clear_cache_btn.clicked.connect(controller.clear_cache)

    def reset_ui(self):
        """重置UI状态，清除所有分割结果显示"""
        # 由于当前页面没有image_view和info_widget，
        # 我们只需要执行最小的清理操作
        
        # 提示用户缓存已清空
        from PySide6.QtWidgets import QLabel
        
        # 清理上一次可能添加的临时标签
        for child in self.findChildren(QLabel, "temp_reset_label"):
            child.deleteLater()
            
        # 这里可以自定义其他清理逻辑
        # 但不要引用不存在的属性 