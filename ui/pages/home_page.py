from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QScrollArea, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCursor, QDesktopServices
from PySide6.QtCore import QUrl

from ui.widgets.selectable_label import SelectableLabel

class HomePage(QWidget):
    """首页类，展示系统概述"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setObjectName("homeScrollArea")
        
        # 创建内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # 标题部分
        title = QLabel("遥感影像智能解译系统")
        title.setObjectName("page_title")
        content_layout.addWidget(title)
        
        subtitle = QLabel("一站式遥感影像处理与解译平台")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        content_layout.addWidget(subtitle)
        
        # 添加底部图片区
        images_container = QFrame()
        images_container.setObjectName("content_frame")
        images_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        images_layout = QVBoxLayout(images_container)
        
        demos_title = QLabel("功能演示")
        demos_title.setObjectName("section_title")
        images_layout.addWidget(demos_title)
        
        # 图片展示区域
        image_gallery = QFrame()
        gallery_layout = QHBoxLayout(image_gallery)
        gallery_layout.setContentsMargins(10, 10, 10, 10)
        gallery_layout.setSpacing(20)
        
        # 场景分类图片
        image_path1 = r"D:\VS_WORKBASE\rsiis\遥感影像智能解译系统V1.0\docs\demo_image\scene_classification_demo.jpg"
        self.add_clickable_image(gallery_layout, image_path1, width=280)
        
        # 语义分割图片
        image_path2 = r"D:\VS_WORKBASE\rsiis\遥感影像智能解译系统V1.0\docs\demo_image\segmentation_demo.jpg"
        self.add_clickable_image(gallery_layout, image_path2, width=280)
        
        # 目标检测图片
        image_path3 = r"D:\VS_WORKBASE\rsiis\遥感影像智能解译系统V1.0\docs\demo_image\detection_demo.jpg"
        self.add_clickable_image(gallery_layout, image_path3, width=280)
        
        images_layout.addWidget(image_gallery)
        content_layout.addWidget(images_container)
        
        # 设置弹性占位
        content_layout.addStretch(1)
        
        # 设置滚动区域内容
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
    
    def add_clickable_image(self, layout, image_path, width=None, height=None):
        """添加可点击图片"""
        # 创建一个标签显示图片
        img_label = QLabel()
        img_label.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        img_label.setAlignment(Qt.AlignCenter)
        
        try:
            pixmap = QPixmap(image_path)
            if width and height:
                pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            elif width:
                pixmap = pixmap.scaledToWidth(width, Qt.SmoothTransformation)
            elif height:
                pixmap = pixmap.scaledToHeight(height, Qt.SmoothTransformation)
                
            img_label.setPixmap(pixmap)
            
            # 添加点击事件
            def open_image(event):
                url = QUrl.fromLocalFile(image_path)
                QDesktopServices.openUrl(url)
            
            img_label.mousePressEvent = open_image
            
        except Exception as e:
            img_label.setText(f"无法加载图片: {e}")
        
        layout.addWidget(img_label)
        return img_label 