from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QScrollArea)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QCursor, QDesktopServices

from ui.widgets.selectable_label import SelectableLabel

class HelpPage(QWidget):
    """帮助页面类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # 减少边距，让内容占据更多空间
        
        title = QLabel("帮助中心")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("系统功能图解")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # 允许滚动区域内的内容随窗口调整大小
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.NoFrame)  # 去除边框
        
        # 创建滚动区域的内容容器
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)  # 增加图片之间的间距
        
        # 1. 场景分类图片及说明
        section_title1 = QLabel("场景分类")
        section_title1.setObjectName("section_title")
        scroll_layout.addWidget(section_title1)
        
        # 添加可点击的场景分类图片
        image_path1 = r"D:\VS_WORKBASE\rsiis\遥感影像智能解译系统V1.0\docs\demo_image\scene_classification_process.png"
        self.add_clickable_image(scroll_layout, image_path1, width=700)
        
        # 添加场景分类说明 (使用SelectableLabel使文本可选)
        class_desc_text = "场景分类对遥感影像进行整体分类，识别影像所属场景类别。本系统采用深度学习模型进行特征提取和分类，支持多达45种常见地物场景类型的识别，可应用于地理国情监测、城市规划等领域。"
        class_desc = SelectableLabel(class_desc_text)
        class_desc.setWordWrap(True)
        class_desc.setObjectName("desc_text")
        class_desc.setStyleSheet("background-color: transparent;")
        scroll_layout.addWidget(class_desc)
        
        # 添加分隔线
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setFrameShadow(QFrame.Sunken)
        separator1.setObjectName("separator")
        scroll_layout.addWidget(separator1)
        
        # 2. 语义分割图片及说明
        section_title2 = QLabel("语义分割")
        section_title2.setObjectName("section_title")
        scroll_layout.addWidget(section_title2)
        
        # 添加可点击的语义分割图片
        image_path2 = r"D:\VS_WORKBASE\rsiis\遥感影像智能解译系统V1.0\docs\demo_image\DeepLab_segmentation_process.png"
        self.add_clickable_image(scroll_layout, image_path2, width=700)
        
        # 添加语义分割说明 (使用SelectableLabel使文本可选)
        seg_desc_text = "语义分割基于DeepLab模型，对遥感影像进行像素级分类，可识别地物类型并生成分类图。该功能适用于土地覆盖分类、变化检测等应用场景。系统支持多种预训练模型和自定义训练。"
        seg_desc = SelectableLabel(seg_desc_text)
        seg_desc.setWordWrap(True)
        seg_desc.setObjectName("desc_text")
        seg_desc.setStyleSheet("background-color: transparent;")
        scroll_layout.addWidget(seg_desc)
        
        # 添加分隔线
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setObjectName("separator")
        scroll_layout.addWidget(separator2)
        
        # 3. 目标检测图片及说明
        section_title3 = QLabel("目标检测")
        section_title3.setObjectName("section_title")
        scroll_layout.addWidget(section_title3)
        
        # 添加可点击的目标检测图片
        image_path3 = r"D:\VS_WORKBASE\rsiis\遥感影像智能解译系统V1.0\docs\demo_image\yolo_detection_process.png"
        self.add_clickable_image(scroll_layout, image_path3, width=700)
        
        # 添加目标检测说明 (使用SelectableLabel使文本可选)
        det_desc_text = "目标检测基于YOLO系列模型，能够识别并定位遥感影像中的特定目标，如建筑物、车辆、飞机等，并提供位置信息和置信度。系统支持多尺度目标检测和实时推理，适用于军事侦察、灾害评估等应用场景。"
        det_desc = SelectableLabel(det_desc_text)
        det_desc.setWordWrap(True)
        det_desc.setObjectName("desc_text")
        det_desc.setStyleSheet("background-color: transparent;")
        scroll_layout.addWidget(det_desc)
        
        # 添加一些底部间距
        scroll_layout.addStretch()
        
        # 设置滚动区域内容
        scroll_area.setWidget(scroll_content)
        
        # 将滚动区域添加到主布局
        layout.addWidget(scroll_area, 1)  # 让scroll_area占据布局中的所有可用空间
        
        # 联系与支持 - 浅灰色小字体放在底部，可选中的文本
        contact_text = "技术支持邮箱: support@rsiis.com | 官方网站: www.rsiis.com | 文档中心: docs.rsiis.com"
        contact_label = SelectableLabel(contact_text)
        contact_label.setAlignment(Qt.AlignCenter)
        contact_label.setStyleSheet("color: #999999; font-size: 9pt; background-color: transparent; border: none;")
        contact_label.setMaximumHeight(30)  # 限制高度
        layout.addWidget(contact_label)
    
    def add_clickable_image(self, layout, image_path, width=None, height=None):
        """
        添加可点击图片，点击后可在系统默认图片查看器中打开
        :param layout: 要添加图片的布局
        :param image_path: 图片路径
        :param width: 图片宽度（可选）
        :param height: 图片高度（可选）
        :return: 添加的图片标签
        """
        # 创建图片标签
        image_label = QLabel()
        
        try:
            pixmap = QPixmap(image_path)
            
            # 如果指定了尺寸，则调整图片大小
            if width and height:
                pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            elif width:
                pixmap = pixmap.scaledToWidth(width, Qt.SmoothTransformation)
            elif height:
                pixmap = pixmap.scaledToHeight(height, Qt.SmoothTransformation)
            
            # 设置图片
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            
            # 使图片可点击
            image_label.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标形状为手型
            image_label.setToolTip("点击查看原始图片")
            
            # 存储图片路径
            image_label.setProperty("image_path", image_path)
            
            # 添加点击事件
            def open_image(event):
                path = image_label.property("image_path")
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))
            
            # 设置鼠标点击事件
            image_label.mousePressEvent = open_image
        
        except Exception as e:
            image_label.setText(f"无法加载图片: {e}")
        
        # 添加到布局
        layout.addWidget(image_label)
        
        return image_label 