from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication
from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QImage, QColor, qRed, qGreen, qBlue, qRgb

import os
import sys
from PIL import Image

# 导入Function层的渔网分割模型
from Function.data.fishnet_seg import FishnetSegmentation
from utils.geo import GDAL_AVAILABLE, RASTERIO_AVAILABLE  # 导入GDAL可用性标志

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
        
        # GeoTIFF标志
        self.is_geotiff = False
        self.is_sentinel = False
    
    def setup(self, grid_generator=None):
        """设置功能层引用"""
        self.grid_generator = grid_generator
    
    def import_image(self):
        """导入遥感影像"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, 
            "选择遥感影像", 
            "", 
            "遥感影像文件 (*.tif *.tiff *.img *.jpg *.png);;GeoTIFF文件 (*.tif *.tiff);;所有文件 (*.*)"
        )
        
        if file_path:
            # 显示加载中提示，避免用户误认为程序无响应
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            try:
                self.current_image_path = file_path
                
                # 使用模型层加载图像
                success, image_info = self.fishnet_model.load_image(file_path)
                
                # 恢复正常光标
                QApplication.restoreOverrideCursor()
                
                if success:
                    # 更新GeoTIFF标志
                    self.is_geotiff = image_info.get("is_geotiff", False)
                    self.is_sentinel = image_info.get("is_sentinel", False)
                    
                    # 准备图像信息消息
                    image_format = image_info.get("format", "未知")
                    width = image_info.get("width", "未知")
                    height = image_info.get("height", "未知")
                    
                    msg = f"成功导入图像：{file_path}\n尺寸：{width}×{height}像素"
                    
                    # 如果是GeoTIFF，添加地理信息
                    if self.is_geotiff:
                        bands = image_info.get("bands", "未知")
                        crs = image_info.get("crs", "未知")
                        
                        # 简化坐标系显示
                        simplified_crs = self._simplify_crs_display(crs)
                        
                        if self.is_sentinel:
                            band_combo = image_info.get("band_combination", "")
                            msg += f"\n格式：Sentinel-2 GeoTIFF\n波段数：{bands}\n坐标系：{simplified_crs}\n使用波段组合：{band_combo}"
                            msg += "\n\n注意：已应用基本图像处理"
                        else:
                            msg += f"\n格式：GeoTIFF\n波段数：{bands}\n坐标系：{simplified_crs}"
                    else:
                        msg += f"\n格式：{image_format}"
                    
                    QMessageBox.information(None, "导入成功", msg)
                    return True
                else:
                    # 获取详细错误信息
                    error_msg = image_info.get('error', '未知错误')
                    detailed_error = image_info.get('detailed_error', '')
                    
                    # 创建错误消息框
                    error_box = QMessageBox(None)
                    error_box.setWindowTitle("导入失败")
                    error_box.setIcon(QMessageBox.Critical)
                    error_box.setText(f"无法加载图像：{error_msg}")
                    
                    # 如果有详细错误，添加到详细信息中
                    if detailed_error:
                        error_box.setDetailedText(detailed_error)
                    
                    # 添加可能的解决方案提示
                    error_box.setInformativeText(
                        "可能的解决方案：\n"
                        "1. 确认文件格式是否支持\n"
                        "2. 检查文件是否损坏\n"
                        "3. 尝试使用其他格式保存文件后再导入\n"
                        "4. 确保GDAL和rasterio库正确安装"
                    )
                    
                    # 添加诊断按钮，用于显示系统诊断信息
                    error_box.addButton("诊断信息", QMessageBox.HelpRole)
                    error_box.addButton(QMessageBox.Close)
                    
                    # 显示错误消息框
                    result = error_box.exec_()
                    
                    # 如果用户点击了诊断信息按钮
                    if result == 0:  # HelpRole按钮
                        self._show_diagnostic_info()
                    
                    return False
            except Exception as e:
                # 恢复正常光标
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(None, "导入异常", f"发生未预期的错误：{str(e)}")
                return False
            finally:
                # 确保光标被恢复
                QApplication.restoreOverrideCursor()
        
        return False
    
    def _show_diagnostic_info(self):
        """显示系统诊断信息，帮助用户排查问题"""
        try:
            # 收集系统信息
            import platform
            import PIL
            import numpy
            
            # GDAL版本信息
            gdal_version = "未安装"
            try:
                from osgeo import gdal
                gdal_version = gdal.VersionInfo()
            except:
                pass
            
            # rasterio版本信息
            rasterio_version = "未安装"
            try:
                import rasterio
                rasterio_version = rasterio.__version__
            except:
                pass
            
            # 收集环境变量信息
            env_vars = {
                'GDAL_DATA': os.environ.get('GDAL_DATA', '未设置'),
                'PROJ_LIB': os.environ.get('PROJ_LIB', '未设置'),
                'PATH': os.environ.get('PATH', '未设置')
            }
            
            # 构建诊断信息
            diag_info = f"""系统诊断信息：
操作系统: {platform.platform()}
Python版本: {platform.python_version()}
PIL版本: {PIL.__version__}
NumPy版本: {numpy.__version__}
GDAL版本: {gdal_version}
rasterio版本: {rasterio_version}

环境变量:
GDAL_DATA = {env_vars['GDAL_DATA']}
PROJ_LIB = {env_vars['PROJ_LIB']}

最后一次错误信息:
{self.fishnet_model.last_error if hasattr(self.fishnet_model, 'last_error') else '无错误记录'}
"""
            
            # 显示诊断信息
            diag_box = QMessageBox()
            diag_box.setWindowTitle("系统诊断信息")
            diag_box.setText("以下是系统诊断信息，可用于排查问题：")
            diag_box.setDetailedText(diag_info)
            diag_box.exec_()
            
        except Exception as e:
            QMessageBox.warning(None, "诊断失败", f"收集诊断信息时出错：{str(e)}")
    
    def set_grid_params(self):
        """设置网格参数 - 使用对话框让用户以网格数量方式输入参数"""
        # 确保已导入图像
        if not self.current_image_path:
            QMessageBox.warning(None, "错误", "请先导入遥感影像")
            return False
            
        # 获取当前图像尺寸
        image_size = (0, 0)
        if hasattr(self.fishnet_model, 'image') and self.fishnet_model.image:
            image_size = self.fishnet_model.image.size
        else:
            QMessageBox.warning(None, "警告", "无法获取图像尺寸，将使用默认参数")
        
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
                
                msg = f"网格数量: {grid_count[0]}×{grid_count[1]}, 每格尺寸约: {grid_width}×{grid_height}像素"
                
                # 如果是GeoTIFF，添加提示
                if self.is_geotiff:
                    msg += "\n\n注意：检测到GeoTIFF格式，分割结果将保留地理参考信息"
                
                QMessageBox.information(None, "参数设置", msg)
                return True
            else:
                QMessageBox.warning(None, "参数设置失败", grid_info.get("error", "未知错误"))
        
        return False
    
    def start_fishnet(self):
        """开始渔网分割"""
        if not self.current_image_path:
            QMessageBox.warning(None, "错误", "请先导入遥感影像")
            return False
        
        # 显示加载中提示
        QApplication.setOverrideCursor(Qt.WaitCursor)
        
        try:
            # 使用模型层生成网格
            success, result = self.fishnet_model.generate_grid()
            
            # 恢复光标
            QApplication.restoreOverrideCursor()
            
            if success:
                # 将模型层的结果转换为UI层可用的格式
                self.grid_result = []
                ui_compatible_results = self.fishnet_model.get_ui_compatible_results()
                
                # 检查是否有有效图像
                has_valid_image = False
                
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
                        qimg = QImage(
                            image_data['data'],
                            image_data['width'],
                            image_data['height'],
                            image_data['bytes_per_line'],
                            QImage.Format_RGB888  # 使用RGB格式，不是BGR
                        )
                        
                        # 检查图像是否全黑或接近全黑（1%的非黑色像素）
                        is_black = self._is_image_too_dark(qimg)
                        
                        if is_black:
                            # 尝试进行亮度调整
                            qimg = self._enhance_qimage(qimg)
                        else:
                            has_valid_image = True
                        
                        ui_grid['image'] = qimg
                    else:
                        # 创建红色的错误指示图像
                        error_img = QImage(100, 100, QImage.Format_RGB888)
                        error_img.fill(QColor(255, 0, 0))  # 纯红色
                        ui_grid['image'] = error_img
                    
                    self.grid_result.append(ui_grid)
                
                # 如果所有图像都是全黑的，给出警告但仍然继续
                if not has_valid_image:
                    QMessageBox.warning(None, "渔网分割提示", 
                        "分割成功，但所有网格图像似乎都是黑色的。这可能是因为：\n"
                        "1. 原始图像数据特殊或缺少可见光波段\n"
                        "2. 需要特殊的图像增强或处理\n"
                        "您仍然可以查看和导出分割结果。")
                    
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
        except Exception as e:
            # 确保光标被恢复
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(None, "分割异常", f"渔网分割过程中发生错误: {str(e)}")
            return False
        finally:
            # 确保光标被恢复
            QApplication.restoreOverrideCursor()
    
    def _is_image_too_dark(self, qimage, threshold=10):
        """
        检查图像是否过暗或全黑
        更高效的采样检测
        """
        try:
            width = qimage.width()
            height = qimage.height()
            
            if width <= 0 or height <= 0:
                return True
                
            # 使用间隔采样，提高性能
            dark_count = 0
            sample_count = 0
            
            # 每10个像素采样一次，最多采样1000个点
            step = max(1, int(width * height / 1000))
            
            for y in range(0, height, step):
                for x in range(0, width, step):
                    color = qimage.pixelColor(x, y)
                    brightness = (color.red() + color.green() + color.blue()) / 3
                    if brightness < threshold:
                        dark_count += 1
                    sample_count += 1
            
            dark_ratio = dark_count / max(1, sample_count)
            return dark_ratio > 0.9  # 如果90%以上的像素是暗的，认为图像太暗
        except Exception:
            return False
            
    def _enhance_qimage(self, qimage):
        """尝试增强过暗的QImage，使用更高效的处理方式"""
        try:
            # 转换为QImage.Format_RGB32以便像素操作
            if qimage.format() != QImage.Format_RGB32:
                qimage = qimage.convertToFormat(QImage.Format_RGB32)
                
            width = qimage.width()
            height = qimage.height()
            
            # 创建一个新图像
            result = QImage(width, height, QImage.Format_RGB32)
            
            # 固定亮度因子，避免每个像素都计算
            brightness_factor = 2.5  # 适度增强亮度
            
            # 使用更高效的方式增强亮度
            for y in range(height):
                for x in range(width):
                    pixel = qimage.pixel(x, y)
                    r = min(255, int(qRed(pixel) * brightness_factor))
                    g = min(255, int(qGreen(pixel) * brightness_factor))
                    b = min(255, int(qBlue(pixel) * brightness_factor))
                    result.setPixel(x, y, qRgb(r, g, b))
            
            return result
        except Exception:
            return qimage  # 返回原始图像
    
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
            try:
                # 使用模型层导出结果，不导出SHP文件
                success, export_info = self.fishnet_model.export_result(base_dir, create_subfolders=True, export_shp=False)
                
                if success:
                    msg = f"渔网分割结果已保存至：{export_info.get('save_dir')}\n共导出 {export_info.get('files_count')} 个文件"
                    
                    # 如果是GeoTIFF，添加提示
                    if self.is_geotiff:
                        msg += "\n\n注意：分割结果已保存为TIFF格式并保留了原始GeoTIFF的地理参考信息"
                        if GDAL_AVAILABLE:
                            msg += "\n已使用GDAL高精度方法保存地理信息"
                    
                    QMessageBox.information(None, "导出成功", msg)
                    return True
                else:
                    error_msg = export_info.get('error', '未知错误') if isinstance(export_info, dict) else "未知错误"
                    QMessageBox.critical(
                        None, 
                        "导出失败", 
                        f"导出分割结果失败: {error_msg}"
                    )
            except Exception as e:
                QMessageBox.critical(
                    None,
                    "导出错误",
                    f"导出过程中发生错误:\n{str(e)}\n\n可能原因：\n"
                    "1. 图像没有有效的地理坐标信息\n"
                    "2. GDAL或rasterio库工作异常\n"
                    "3. 权限不足或磁盘空间不足"
                )
        
        return False
    
    def _simplify_crs_display(self, crs_string):
        """
        简化坐标系信息显示
        
        Args:
            crs_string: 原始坐标系信息字符串
            
        Returns:
            str: 简化后的坐标系描述
        """
        if not crs_string or crs_string == "未知":
            return "未知坐标系"
            
        # 如果是WGS 84坐标系
        if "WGS 84" in crs_string or "WGS84" in crs_string:
            # 提取EPSG代码
            if "EPSG" in crs_string:
                import re
                match = re.search(r'EPSG[":](\d+)', crs_string)
                if match:
                    return f"WGS 84 (EPSG:{match.group(1)})"
            return "WGS 84"
            
        # 如果包含EPSG代码
        if "EPSG" in crs_string:
            import re
            match = re.search(r'EPSG[":](\d+)', crs_string)
            if match:
                return f"EPSG:{match.group(1)}"
                
        # 如果是UTM投影
        if "UTM" in crs_string:
            # 尝试提取UTM区域
            import re
            match = re.search(r'UTM zone (\d+)([NS])?', crs_string)
            if match:
                zone = match.group(1)
                hemisphere = match.group(2) if match.group(2) else ""
                return f"UTM区域 {zone}{hemisphere}"
            return "UTM投影"
            
        # 截断过长的坐标系字符串
        if len(crs_string) > 30:
            return crs_string[:27] + "..."
            
        return crs_string 