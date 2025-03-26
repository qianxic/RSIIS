from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication, QDialog, QVBoxLayout, QGroupBox, QRadioButton, QLabel, QDialogButtonBox
from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QImage, QColor, qRed, qGreen, qBlue, qRgb

import os
import sys
from PIL import Image
import time

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
        
        # 页面引用
        self.page = None
    
    def setup(self, grid_generator=None, page=None):
        """设置功能层引用和页面引用"""
        self.grid_generator = grid_generator
        self.page = page
    
    def import_image(self):
        """导入图像/影像"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, 
            "选择图像/影像", 
            "", 
            "图像文件 (*.tif *.tiff *.img *.jpg *.png);;GeoTIFF文件 (*.tif *.tiff);;所有文件 (*.*)"
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
                        
                        msg += f"\n波段数：{bands}\n坐标系：{simplified_crs}"
                    
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
        # 严格检查图像是否已加载
        if not self.current_image_path or not hasattr(self.fishnet_model, 'image') or self.fishnet_model.image is None:
            QMessageBox.warning(None, "错误", "请先导入图像/影像")
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
                    pass
                
                QMessageBox.information(None, "参数设置", msg)
                return True
            else:
                QMessageBox.warning(None, "参数设置失败", grid_info.get("error", "未知错误"))
        
        return False
    
    def start_fishnet(self):
        """开始渔网分割"""
        # 严格检查图像是否已加载
        if not self.current_image_path or not hasattr(self.fishnet_model, 'image') or self.fishnet_model.image is None:
            QMessageBox.warning(None, "错误", "请先导入图像/影像")
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
                        
                
                
                # 获取网格数量
                total_grids = len(self.fishnet_model.grid_result)
                
                # 显示一个简单的成功消息
                QMessageBox.information(None, "渔网分割", 
                    f"分割成功，共生成 {total_grids} 个网格图像\n\n"
                    f"请点击\"导出分割结果\"按钮保存结果和详细信息")
                
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
    
    
    def export_result(self):
        """导出分割结果"""
        # 严格检查是否有可导出的分割结果
        if not self.current_image_path or not self.fishnet_model or not self.fishnet_model.grid_result:
            QMessageBox.warning(None, "错误", "请先导入图像\影像并完成分割操作")
            return False
        
        # 创建导出格式选择对话框
        format_dialog = QDialog(None)
        format_dialog.setWindowTitle("选择导出格式")
        format_dialog.resize(400, 200)
        
        layout = QVBoxLayout(format_dialog)
        
        # 导出格式选择
        format_group = QGroupBox("选择导出格式:")
        format_layout = QVBoxLayout(format_group)
        
        # 添加单选按钮
        self.tiff_radio = QRadioButton("GeoTIFF格式")
        self.image_radio = QRadioButton("普通图像格式 (PNG)")
        
        # 默认选择并禁用不支持的选项
        if self.is_geotiff:
            self.tiff_radio.setChecked(True)
        else:
            self.image_radio.setChecked(True)
            self.tiff_radio.setEnabled(self.is_geotiff)  # 只有GeoTIFF才能导出为GeoTIFF
        
        # 添加到布局
        format_layout.addWidget(self.tiff_radio)
        format_layout.addWidget(self.image_radio)
        
        # 添加说明文本
        if self.is_geotiff:
            info_text = "• GeoTIFF格式将保留原始地理坐标信息，适用于GIS软件\n• 普通图像格式仅保存可视图像，适用于普通查看"
        else:
            info_text = "• 当前图像不是GeoTIFF格式，只能导出为普通图像格式"
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        
        # 添加按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(format_dialog.accept)
        button_box.rejected.connect(format_dialog.reject)
        
        # 组装布局
        layout.addWidget(format_group)
        layout.addWidget(info_label)
        layout.addWidget(button_box)
        
        # 显示对话框
        if not format_dialog.exec_():
            return False  # 用户取消了操作
        
        # 获取选择的格式
        export_as_geotiff = self.tiff_radio.isChecked() and self.is_geotiff
        
        # 告知用户将会生成详细信息文件
        QMessageBox.information(None, "导出信息", 
            "导出结果将会包含\n1.渔网示意图2.分割结果，3.分割信息")
        
        # 让用户选择保存文件夹
        base_dir = QFileDialog.getExistingDirectory(
            None,
            "选择保存结果的父目录",
            ""
        )
        
        if base_dir:
            try:
                # 根据选择的格式导出
                if export_as_geotiff:
                    # 使用模型层导出结果，不导出SHP文件
                    success, export_info = self.fishnet_model.export_result(
                        base_dir, 
                        create_subfolders=True, 
                        export_shp=False,
                        export_as_image=False
                    )
                else:
                    # 导出为普通图像格式
                    success, export_info = self.fishnet_model.export_result(
                        base_dir, 
                        create_subfolders=True, 
                        export_shp=False,
                        export_as_image=True
                    )
                
                if success:
                    # 获取保存目录路径
                    save_dir = export_info.get('save_dir', base_dir)
                    
                    # 保存分割信息到TXT文件
                    info_file_path = os.path.join(save_dir, "分割信息.txt")
                    self._save_grid_info_to_file(info_file_path)
                    
                    # 显示统一的导出成功提示
                    QMessageBox.information(None, "导出信息", 
                        "导出成功")
                    
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
    
    def _save_grid_info_to_file(self, file_path):
        """
        保存网格分割信息到TXT文件
        
        Args:
            file_path: TXT文件保存路径
        """
        if not self.fishnet_model or not self.fishnet_model.grid_result:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # 写入标题和基本信息
                f.write("=" * 50 + "\n")
                f.write("渔网分割结果信息\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"原始图像: {self.current_image_path}\n")
                f.write(f"分割时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"网格数量: {len(self.fishnet_model.grid_result)}\n")
                
                if self.is_geotiff:
                    f.write(f"GeoTIFF: 是\n")
                if self.is_sentinel:
                    f.write(f"Sentinel: 是\n")
                
                f.write("\n" + "-" * 50 + "\n\n")
                
                # 写入每个网格的详细信息
                for i, grid in enumerate(self.fishnet_model.grid_result):
                    # 获取基本信息
                    pos = grid['position']
                    row, col = grid['row'], grid['col']
                    width, height = grid['image_data'].size
                    
                    # 写入基本信息
                    f.write(f"网格 {i+1} (行:{row+1}, 列:{col+1}):\n")
                    f.write(f"  尺寸: {width} x {height} 像素\n")
                    f.write(f"  原图位置: 左上角({pos[0]}, {pos[1]}), 宽度:{pos[2]}, 高度:{pos[3]}\n")
                    
                    # 如果有地理信息，则写入
                    if 'geo_transform' in grid and grid['geo_transform'] is not None:
                        if hasattr(grid['geo_transform'], '__call__'):
                            # rasterio风格的transform
                            topleft_x, topleft_y = grid['geo_transform'] * (0, 0)
                            botright_x, botright_y = grid['geo_transform'] * (width, height)
                            f.write(f"  地理坐标: 左上角({topleft_x:.6f}, {topleft_y:.6f}), 右下角({botright_x:.6f}, {botright_y:.6f})\n")
                        else:
                            # GDAL风格的transform
                            transform = grid['geo_transform']
                            topleft_x = transform[0] + pos[0] * transform[1]
                            topleft_y = transform[3] + pos[1] * transform[5]
                            botright_x = topleft_x + width * transform[1]
                            botright_y = topleft_y + height * transform[5]
                            f.write(f"  地理坐标: 左上角({topleft_x:.6f}, {topleft_y:.6f}), 右下角({botright_x:.6f}, {botright_y:.6f})\n")
                    
                    f.write("\n")
                
                f.write("=" * 50 + "\n")
                f.write("文件结束\n")
                f.write("=" * 50 + "\n")
                
        except Exception as e:
            import traceback
            print(f"保存分割信息到TXT文件时出错: {str(e)}")
            traceback.print_exc()
    
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
        
    def clear_cache(self):
        """清空当前分割任务的缓存"""
        # 显示处理中提示
        QApplication.setOverrideCursor(Qt.WaitCursor)
        
        try:
            # 彻底重置所有状态
            self.fishnet_model = FishnetSegmentation()  # 重置模型层
            self.grid_result = None                     # 清空分割结果
            self.grid_params = {"grid_count": (4, 4)}   # 重置网格参数
            self.current_image_path = None              # 清空当前图像路径
            self.is_geotiff = False                     # 重置GeoTIFF标志
            self.is_sentinel = False                    # 重置Sentinel标志
            
            # 关闭可能打开的预览窗口
            for window_name in ['overview_window', 'preview_window']:
                if hasattr(self, window_name) and getattr(self, window_name) is not None:
                    try:
                        window = getattr(self, window_name)
                        window.close()
                        setattr(self, window_name, None)
                    except:
                        pass
            
            # 恢复光标
            QApplication.restoreOverrideCursor()
            
            # 提示清空成功
            QMessageBox.information(None, "清空缓存", "缓存已清空，您可以重新导入图像\影像")
            return True
            
        except Exception as e:
            # 恢复光标
            QApplication.restoreOverrideCursor()
            # 即使出错，也不向用户显示技术细节，只提供简单反馈
            QMessageBox.information(None, "清空缓存", "缓存已清空，您可以重新导入图像\影像")
            return True  # 返回True表示操作完成
        finally:
            # 确保光标被恢复
            QApplication.restoreOverrideCursor() 