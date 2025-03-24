from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, 
                             QPushButton, QMainWindow, QWidget, QScrollArea, QToolBar, QSplitter)
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QPixmap, QImage, QIcon, QColor, QPainter, QPen, QFont, QAction

class GridParamsDialog(QDialog):
    """网格参数设置对话框"""
    def __init__(self, parent=None, image_size=(0, 0), current_rows=4, current_cols=4):
        super().__init__(parent)
        self.setWindowTitle("设置网格参数")
        self.resize(350, 200)
        self.image_size = image_size
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 显示图像尺寸信息
        image_info = QLabel(f"图像尺寸: {image_size[0]} × {image_size[1]} 像素")
        image_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_info)
        
        # 网格数量设置 - 行数
        rows_layout = QHBoxLayout()
        rows_label = QLabel("行数:")
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 100)
        self.rows_spin.setValue(current_rows)
        rows_layout.addWidget(rows_label)
        rows_layout.addWidget(self.rows_spin)
        layout.addLayout(rows_layout)
        
        # 网格数量设置 - 列数
        cols_layout = QHBoxLayout()
        cols_label = QLabel("列数:")
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 100)
        self.cols_spin.setValue(current_cols)
        cols_layout.addWidget(cols_label)
        cols_layout.addWidget(self.cols_spin)
        layout.addLayout(cols_layout)
        
        # 显示每个子块的像素信息
        self.grid_size_label = QLabel()
        self.grid_size_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.grid_size_label)
        
        # 更新网格尺寸显示
        self.update_grid_size()
        
        # 连接信号
        self.rows_spin.valueChanged.connect(self.update_grid_size)
        self.cols_spin.valueChanged.connect(self.update_grid_size)
        
        # 按钮
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("取消")
        ok_btn = QPushButton("确定")
        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        layout.addLayout(button_layout)
    
    def update_grid_size(self):
        """更新每个子块的像素信息"""
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        
        if self.image_size[0] > 0 and self.image_size[1] > 0:
            grid_width = self.image_size[0] // cols
            grid_height = self.image_size[1] // rows
            self.grid_size_label.setText(f"每个网格尺寸约: {grid_width} × {grid_height} 像素")
        else:
            self.grid_size_label.setText("无法计算网格尺寸 (未知图像尺寸)")
    
    def get_params(self):
        """获取设置的参数"""
        return {
            "grid_count": (self.rows_spin.value(), self.cols_spin.value())
        }


class ImageViewer(QWidget):
    """图像查看器控件，支持缩放"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = None
        self.scale_factor = 1.0
        self.offset = QPoint(0, 0)
        self.fit_to_view = True  # 默认适应视图
    
    def setPixmap(self, pixmap):
        """设置要显示的图像"""
        self.pixmap = pixmap
        self.scale_factor = 1.0
        self.offset = QPoint(0, 0)
        self.fit_to_view = True  # 重置为适应视图
        self.update()
    
    def paintEvent(self, event):
        """绘制事件"""
        if not self.pixmap:
            return
        
        painter = QPainter(self)
        
        if self.fit_to_view:
            # 计算适应视图的比例
            view_width = self.width()
            view_height = self.height()
            pixmap_width = self.pixmap.width()
            pixmap_height = self.pixmap.height()
            
            # 计算宽高比
            width_ratio = view_width / pixmap_width
            height_ratio = view_height / pixmap_height
            
            # 使用较小的比例，确保整个图像可见
            self.scale_factor = min(width_ratio, height_ratio)
        
        # 计算居中坐标和缩放尺寸
        scaled_size = self.pixmap.size() * self.scale_factor
        center_x = (self.width() - scaled_size.width()) / 2 + self.offset.x()
        center_y = (self.height() - scaled_size.height()) / 2 + self.offset.y()
        
        # 绘制图像
        painter.drawPixmap(int(center_x), int(center_y), 
                          int(scaled_size.width()), int(scaled_size.height()), 
                          self.pixmap)
    
    def wheelEvent(self, event):
        """鼠标滚轮事件，用于放大缩小"""
        if not self.pixmap:
            return
        
        # 缩放时禁用适应视图模式
        self.fit_to_view = False
            
        # 计算缩放系数
        angle = event.angleDelta().y()
        if angle > 0:
            self.scale_factor *= 1.1  # 放大10%
        else:
            self.scale_factor *= 0.9  # 缩小10%
        
        # 限制缩放范围
        if self.scale_factor < 0.1:
            self.scale_factor = 0.1
        elif self.scale_factor > 10.0:
            self.scale_factor = 10.0
            
        self.scaleImage()
        
    def scaleImage(self):
        """缩放图像"""
        if not self.pixmap:
            return
            
        # 计算图像缩放后的尺寸
        scaled_size = self.pixmap.size() * self.scale_factor
        
        # 如果缩放后的尺寸小于控件尺寸，则居中显示
        if scaled_size.width() < self.width():
            self.offset.setX(0)
        if scaled_size.height() < self.height():
            self.offset.setY(0)
            
        self.update()  # 更新显示
    
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件，切换适应视图和原始大小"""
        if not self.pixmap:
            return
        
        # 切换适应视图模式
        self.fit_to_view = not self.fit_to_view
        
        if not self.fit_to_view:
            # 原始大小 (1:1)
            self.scale_factor = 1.0
            self.offset = QPoint(0, 0)
        
        self.update()
        
    def resizeEvent(self, event):
        """窗口大小改变事件，适应视图模式下重新计算缩放"""
        if self.fit_to_view and self.pixmap:
            self.update()  # 触发重绘，paintEvent会重新计算比例
        super().resizeEvent(event)


class GridOverviewWindow(QMainWindow):
    """渔网分割示意图窗口"""
    def __init__(self, image_path, grid_result, fishnet_model=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("渔网分割示意图")
        self.resize(800, 600)
        
        self.image_path = image_path
        self.grid_result = grid_result
        self.fishnet_model = fishnet_model
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建图像查看器
        self.overview_viewer = ImageViewer()
        main_layout.addWidget(self.overview_viewer, 1)
        
        # 创建按钮
        button_layout = QHBoxLayout()
        self.view_images_button = QPushButton("查看分割后图像")
        
        # 设置按钮样式
        button_style = """
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: 1px solid #3a80d2;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #3a80d2;
            }
            QPushButton:pressed {
                background-color: #2a70c2;
            }
        """
        self.view_images_button.setStyleSheet(button_style)
        self.view_images_button.clicked.connect(self.open_grid_images_viewer)
        
        # 居中显示按钮
        button_layout.addStretch(1)
        button_layout.addWidget(self.view_images_button)
        button_layout.addStretch(1)
        
        main_layout.addLayout(button_layout)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # 加载图像
        self.load_overview_image()
        
    def load_overview_image(self):
        """加载并显示分割示意图"""
        try:
            # 如果提供了模型实例，优先使用模型创建分割示意图
            if self.fishnet_model:
                # 使用模型层创建分割示意图
                image_data = self.fishnet_model.create_overview_image_for_ui()
                
                if image_data:
                    # 创建QImage - 使用RGB格式确保颜色正确
                    overview_qimage = QImage(
                        image_data['data'],
                        image_data['width'],
                        image_data['height'],
                        image_data['bytes_per_line'],
                        QImage.Format_RGB888  # 使用RGB格式确保红色正确显示
                    )
                    
                    # 显示分割示意图
                    self.overview_viewer.setPixmap(QPixmap.fromImage(overview_qimage))
                    return
            
            # 备用方法：如果没有模型实例或模型方法失败，显示错误
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "加载失败", "无法加载分割示意图，请重新运行分割")
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "错误", f"处理图像时出错: {str(e)}")
    
    def open_grid_images_viewer(self):
        """打开分割图像查看器"""
        # 创建详细预览窗口，传递模型实例
        self.grid_viewer = GridImagesViewer(self.grid_result, self.fishnet_model)
        self.grid_viewer.show()


class GridPreviewWindow(QMainWindow):
    """渔网分割预览窗口"""
    def __init__(self, image_path, grid_result, fishnet_model=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("渔网分割预览")
        self.resize(1000, 600)
        
        self.image_path = image_path
        self.grid_result = grid_result
        self.fishnet_model = fishnet_model
        self.current_grid_index = 0
        
        # 设置中心部件为分割器
        splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(splitter)
        
        # 左侧容器 - 用于显示分割示意图和导航按钮
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        
        # 左侧滚动区域 - 用于显示分割示意图
        self.grid_overview_viewer = ImageViewer()
        left_layout.addWidget(self.grid_overview_viewer, 1)
        
        # 添加上一个和下一个按钮到分割图下方
        nav_buttons = QHBoxLayout()
        
        # 创建样式化的按钮
        self.prev_button = QPushButton("上一个")
        self.next_button = QPushButton("下一个")
        
        # 设置按钮样式
        button_style = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
                min-width: 80px;
                max-width: 120px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #999999;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                border-color: #dddddd;
                color: #aaaaaa;
            }
        """
        self.prev_button.setStyleSheet(button_style)
        self.next_button.setStyleSheet(button_style)
        
        self.prev_button.clicked.connect(self.show_previous_grid)
        self.next_button.clicked.connect(self.show_next_grid)
        
        # 创建索引标签并设置样式
        self.grid_index_label = QLabel("1/1")
        self.grid_index_label.setAlignment(Qt.AlignCenter)
        self.grid_index_label.setStyleSheet("font-size: 12px; padding: 5px;")
        self.grid_index_label.setMinimumWidth(60)
        
        # 使用弹性空间来使按钮居中
        nav_buttons.addStretch(1)
        nav_buttons.addWidget(self.prev_button)
        nav_buttons.addWidget(self.grid_index_label)
        nav_buttons.addWidget(self.next_button)
        nav_buttons.addStretch(1)
        
        # 添加导航按钮到布局中
        left_layout.addLayout(nav_buttons)
        
        # 设置适当的边距
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(10)
        
        splitter.addWidget(left_container)
        
        # 右侧 - 用于显示当前分割图片
        self.current_grid_viewer = ImageViewer()
        splitter.addWidget(self.current_grid_viewer)
        
        # 设置分割器比例
        splitter.setSizes([400, 600])
        
        # 加载和显示图像
        self.load_images()
        self.update_current_grid_display()

    def load_images(self):
        """加载原始图像和生成分割示意图"""
        try:
            # 如果提供了模型实例，优先使用模型创建分割示意图
            if self.fishnet_model:
                # 使用模型层创建分割示意图
                image_data = self.fishnet_model.create_overview_image_for_ui()
                
                if image_data:
                    # 创建QImage - 使用RGB格式确保颜色正确
                    overview_qimage = QImage(
                        image_data['data'],
                        image_data['width'],
                        image_data['height'],
                        image_data['bytes_per_line'],
                        QImage.Format_RGB888  # 使用RGB格式确保红色正确显示
                    )
                    
                    # 显示分割示意图
                    self.grid_overview_viewer.setPixmap(QPixmap.fromImage(overview_qimage))
                    return
            
            # 备用方法：如果没有模型实例或模型方法失败，显示错误
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "加载失败", "无法加载分割示意图，请重新运行分割")
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "错误", f"处理图像时出错: {str(e)}")
    
    def update_current_grid_display(self):
        """更新当前显示的网格图像"""
        if not self.grid_result or len(self.grid_result) == 0:
            return
        
        # 显示当前索引/总数
        total_grids = len(self.grid_result)
        self.grid_index_label.setText(f"{self.current_grid_index + 1}/{total_grids}")
        
        # 获取当前网格图像
        current_grid = self.grid_result[self.current_grid_index]
        if 'image' in current_grid:
            grid_image = current_grid['image']
            self.current_grid_viewer.setPixmap(QPixmap.fromImage(grid_image))
        
        # 更新按钮状态
        self.prev_button.setEnabled(self.current_grid_index > 0)
        self.next_button.setEnabled(self.current_grid_index < total_grids - 1)
    
    def show_previous_grid(self):
        """显示上一个网格"""
        if self.current_grid_index > 0:
            self.current_grid_index -= 1
            self.update_current_grid_display()
    
    def show_next_grid(self):
        """显示下一个网格"""
        if self.current_grid_index < len(self.grid_result) - 1:
            self.current_grid_index += 1
            self.update_current_grid_display()


class GridImagesViewer(QMainWindow):
    """渔网分割图像浏览器"""
    def __init__(self, grid_result, fishnet_model=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("渔网分割图像浏览")
        self.resize(800, 600)
        
        self.grid_result = grid_result
        self.fishnet_model = fishnet_model
        self.current_index = 0
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # 添加图像查看器
        self.image_viewer = ImageViewer()
        main_layout.addWidget(self.image_viewer, 1)
        
        # 添加图像信息标签
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        main_layout.addWidget(self.info_label)
        
        # 添加导航按钮布局
        nav_layout = QHBoxLayout()
        
        # 创建样式化的按钮
        self.prev_button = QPushButton("上一张")
        self.next_button = QPushButton("下一张")
        
        # 设置按钮样式 - 与GridPreviewWindow中使用的样式保持一致
        button_style = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
                min-width: 80px;
                max-width: 120px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #999999;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QPushButton:disabled {
                background-color: #f5f5f5;
                border-color: #dddddd;
                color: #aaaaaa;
            }
        """
        self.prev_button.setStyleSheet(button_style)
        self.next_button.setStyleSheet(button_style)
        
        # 添加导航按钮事件
        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)
        
        # 创建导航位置标签
        self.position_label = QLabel("1/1")
        self.position_label.setAlignment(Qt.AlignCenter)
        self.position_label.setStyleSheet("font-size: 12px; padding: 5px;")
        self.position_label.setMinimumWidth(60)
        
        # 使用弹性空间使按钮居中
        nav_layout.addStretch(1)
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.position_label)
        nav_layout.addWidget(self.next_button)
        nav_layout.addStretch(1)
        
        # 添加导航按钮布局到主布局
        main_layout.addLayout(nav_layout)
        
        # 初始化显示
        self.update_display()
    
    def update_display(self):
        """更新当前显示的图像"""
        if not self.grid_result or len(self.grid_result) == 0:
            self.info_label.setText("没有可用的网格图像")
            return
        
        # 获取当前网格
        current_grid = self.grid_result[self.current_index]
        row = current_grid.get('row', 0)
        col = current_grid.get('col', 0)
        
        # 更新信息标签
        self.info_label.setText(f"网格位置: 第 {row} 行, 第 {col} 列")
        
        # 更新位置标签
        total = len(self.grid_result)
        self.position_label.setText(f"{self.current_index + 1} / {total}")
        
        # 显示图像
        if 'image' in current_grid:
            grid_image = current_grid['image']
            self.image_viewer.setPixmap(QPixmap.fromImage(grid_image))
        
        # 更新按钮状态
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.grid_result) - 1)
        
    def show_previous_image(self):
        """显示上一张图像"""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()
    
    def show_next_image(self):
        """显示下一张图像"""
        if self.current_index < len(self.grid_result) - 1:
            self.current_index += 1
            self.update_display() 