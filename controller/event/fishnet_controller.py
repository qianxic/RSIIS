from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QImage, QColor

import os
from PIL import Image

# 导入Function层的渔网分割模型
from Function.data.fishnet_seg import FishnetSegmentation

# 导入UI组件
from ui.widgets.grid_dialogs import (GridParamsDialog, ImageViewer, 
                                   GridOverviewWindow, GridPreviewWindow, 
                                   GridImagesViewer)

class FishnetController(QObject):
    """渔网分割页面的控制器类，处理UI与功能逻辑之间的交互"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # 功能层引用
        self.grid_generator = None
        
        # 创建模型层实例
        self.fishnet_model = FishnetSegmentation()
        
        # 当前加载的图像路径
        self.current_image_path = None
        
        # 当前网格参数
        self.grid_params = {
            "grid_count": (4, 4)
        }
        
        # 分割结果
        self.grid_result = None
        # 预览窗口
        self.overview_window = None
        self.preview_window = None
    
    def setup(self, grid_generator=None):
        """设置功能层引用"""
        self.grid_generator = grid_generator
    
    def import_image(self):
        """导入遥感影像"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, 
            "选择遥感影像", 
            "", 
            "遥感影像文件 (*.tif *.tiff *.img *.jpg *.png);;所有文件 (*.*)"
        )
        
        if file_path:
            self.current_image_path = file_path
            
            # 使用模型层加载图像
            success, image_info = self.fishnet_model.load_image(file_path)
            
            if success:
                QMessageBox.information(None, "导入成功", f"成功导入图像：{file_path}")
                return True
            else:
                QMessageBox.warning(None, "导入失败", f"无法加载图像：{image_info.get('error', '未知错误')}")
                return False
        
        return False
    
    def set_grid_params(self):
        """设置网格参数 - 使用对话框让用户以网格数量方式输入参数"""
        # 确保已导入图像
        if not self.current_image_path:
            QMessageBox.warning(None, "错误", "请先导入遥感影像")
            return False
            
        # 获取当前图像尺寸
        image_size = (0, 0)
        if self.current_image_path:
            try:
                with Image.open(self.current_image_path) as img:
                    image_size = img.size
            except Exception as e:
                QMessageBox.warning(None, "警告", f"无法获取图像尺寸: {str(e)}")
        
        # 获取当前设置的网格数量
        current_params = self.fishnet_model.grid_params
        rows, cols = current_params.get("grid_count", (4, 4))
        
        # 创建并显示参数设置对话框
        dialog = GridParamsDialog(
            None,
            image_size=image_size,
            current_rows=rows,
            current_cols=cols
        )
        
        # 如果用户点击确定
        if dialog.exec_():
            # 获取用户设置的参数
            params = dialog.get_params()
            grid_count = params["grid_count"]
            
            # 使用模型层设置参数
            success, grid_info = self.fishnet_model.set_grid_parameters(grid_count)
            
            if success:
                # 更新控制器中的参数
                self.grid_params = params
                
                # 显示确认信息
                grid_width = grid_info.get("grid_size", (0, 0))[0]
                grid_height = grid_info.get("grid_size", (0, 0))[1]
                
                QMessageBox.information(
                    None, 
                    "参数设置", 
                    f"网格数量: {grid_count[0]}×{grid_count[1]}, "
                    f"每格尺寸约: {grid_width}×{grid_height}像素"
                )
                return True
            else:
                QMessageBox.warning(None, "参数设置失败", grid_info.get("error", "未知错误"))
        
        return False
    
    def start_fishnet(self):
        """开始渔网分割"""
        if not self.current_image_path:
            QMessageBox.warning(None, "错误", "请先导入遥感影像")
            return False
        
        # 使用模型层生成网格
        success, result = self.fishnet_model.generate_grid()
        
        if success:
            # 将模型层的结果转换为UI层可用的格式
            self.grid_result = []
            ui_compatible_results = self.fishnet_model.get_ui_compatible_results()
            
            for grid in ui_compatible_results:
                # 复制基本信息
                ui_grid = {
                    'position': grid['position'],
                    'row': grid['row'],
                    'col': grid['col']
                }
                
                # 将图像数据转换为QImage
                image_data = grid['image_data']
                if image_data:
                    # 创建QImage时使用直接的RGB888格式，避免颜色转换错误
                    ui_grid['image'] = QImage(
                        image_data['data'],
                        image_data['width'],
                        image_data['height'],
                        image_data['bytes_per_line'],
                        QImage.Format_RGB888  # 使用RGB格式，不是BGR
                    )
                else:
                    # 创建红色的错误指示图像
                    error_img = QImage(100, 100, QImage.Format_RGB888)
                    error_img.fill(QColor(255, 0, 0))  # 纯红色
                    ui_grid['image'] = error_img
                
                self.grid_result.append(ui_grid)
            
            # 显示预览窗口
            self.show_preview()
            return True
        else:
            if isinstance(result, dict) and 'error' in result:
                error_msg = result['error']
            else:
                error_msg = "未知错误"
            QMessageBox.critical(None, "错误", f"渔网分割失败: {error_msg}")
            return False
    
    def show_preview(self):
        """显示渔网分割预览窗口"""
        if not self.grid_result or not self.current_image_path:
            QMessageBox.warning(None, "错误", "没有可用的分割结果")
            return
        
        # 如果已有预览窗口，先关闭
        if hasattr(self, 'overview_window') and self.overview_window and self.overview_window.isVisible():
            self.overview_window.close()
        
        # 创建并显示示意图窗口
        self.overview_window = GridOverviewWindow(self.current_image_path, self.grid_result, self.fishnet_model)
        self.overview_window.show()
    
    def show_detailed_preview(self):
        """显示带有详细分割预览的窗口"""
        if not self.grid_result or not self.current_image_path:
            QMessageBox.warning(None, "错误", "没有可用的分割结果")
            return
        
        # 如果已有预览窗口，先关闭
        if hasattr(self, 'preview_window') and self.preview_window and self.preview_window.isVisible():
            self.preview_window.close()
        
        # 创建并显示详细预览窗口
        self.preview_window = GridPreviewWindow(self.current_image_path, self.grid_result, self.fishnet_model)
        self.preview_window.show()
    
    def export_result(self):
        """导出分割结果"""
        if not self.current_image_path:
            QMessageBox.warning(None, "错误", "请先导入并处理遥感影像")
            return False
        
        # 让用户选择保存文件夹
        base_dir = QFileDialog.getExistingDirectory(
            None,
            "选择保存结果的父目录",
            ""
        )
        
        if base_dir:
            # 使用模型层导出结果
            success, export_info = self.fishnet_model.export_result(base_dir, create_subfolders=True)
            
            if success:
                QMessageBox.information(
                    None, 
                    "导出成功", 
                    f"渔网分割结果已保存至：{export_info.get('save_dir')}\n"
                    f"共导出 {export_info.get('files_count')} 个文件"
                )
                return True
            else:
                error_msg = export_info.get('error', '未知错误') if isinstance(export_info, dict) else "未知错误"
                QMessageBox.critical(
                    None, 
                    "导出失败", 
                    f"导出分割结果失败: {error_msg}"
                )
        
        return False 