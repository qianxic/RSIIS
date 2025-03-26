from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication
from PySide6.QtCore import QObject, Qt

import os
import sys
from PIL import Image
import time

# 导入变化检测模型
from Function.analysis.change_detection import ChangeDetectionModel


class ChangeDetectionController(QObject):
    """变化检测页面的控制器类，处理UI与功能逻辑之间的交互"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # 功能层引用
        self.model = None
        
        # 当前加载的前后期影像路径
        self.before_image_path = None
        self.after_image_path = None
        
        # 检测结果
        self.detection_result = None
        
        # 页面引用
        self.page = None
    
    def setup(self, page=None):
        """设置页面引用"""
        self.page = page
        # 初始化模型
        self.model = ChangeDetectionModel()
    
    def import_before_image(self):
        """导入前期影像数据集"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, 
            "选择前期影像", 
            "", 
            "图像文件 (*.tif *.tiff *.img *.jpg *.png);;GeoTIFF文件 (*.tif *.tiff);;所有文件 (*.*)"
        )
        
        if file_path:
            # 显示加载中提示
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            try:
                self.before_image_path = file_path
                
                # 调用模型层加载图像
                success, image_info = self.model.load_before_image(file_path)
                
                # 恢复正常光标
                QApplication.restoreOverrideCursor()
                
                if success:
                    # 准备图像信息消息
                    image_format = image_info.get("format", "未知")
                    width = image_info.get("width", "未知")
                    height = image_info.get("height", "未知")
                    
                    msg = f"成功导入前期影像：{os.path.basename(file_path)}\n尺寸：{width}×{height}像素"
                    QMessageBox.information(None, "导入成功", msg)
                    
                    # 更新UI状态 - 未来可以在这里添加
                    
                    return True
                else:
                    error_msg = image_info.get("error", "未知错误")
                    detailed_error = image_info.get("detailed_error", "")
                    
                    QMessageBox.critical(None, "导入失败", 
                                       f"无法加载前期影像：{error_msg}\n{detailed_error}")
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
    
    def import_after_image(self):
        """导入后期影像数据集"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, 
            "选择后期影像", 
            "", 
            "图像文件 (*.tif *.tiff *.img *.jpg *.png);;GeoTIFF文件 (*.tif *.tiff);;所有文件 (*.*)"
        )
        
        if file_path:
            # 显示加载中提示
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            try:
                self.after_image_path = file_path
                
                # 调用模型层加载图像
                success, image_info = self.model.load_after_image(file_path)
                
                # 恢复正常光标
                QApplication.restoreOverrideCursor()
                
                if success:
                    # 准备图像信息消息
                    image_format = image_info.get("format", "未知")
                    width = image_info.get("width", "未知")
                    height = image_info.get("height", "未知")
                    
                    msg = f"成功导入后期影像：{os.path.basename(file_path)}\n尺寸：{width}×{height}像素"
                    QMessageBox.information(None, "导入成功", msg)
                    
                    # 更新UI状态 - 未来可以在这里添加
                    
                    return True
                else:
                    error_msg = image_info.get("error", "未知错误")
                    detailed_error = image_info.get("detailed_error", "")
                    
                    QMessageBox.critical(None, "导入失败", 
                                       f"无法加载后期影像：{error_msg}\n{detailed_error}")
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
    
    def start_change_detection(self):
        """开始变化检测处理"""
        # 检查是否已导入前后期影像
        if not self.model.before_image or not self.model.after_image:
            QMessageBox.warning(None, "警告", "请先导入前期和后期影像")
            return False
        
        # 显示加载中提示
        QApplication.setOverrideCursor(Qt.WaitCursor)
        
        try:
            # 调用模型层进行变化检测
            success, result = self.model.detect_changes()
            
            # 恢复正常光标
            QApplication.restoreOverrideCursor()
            
            if success:
                # 更新控制器中的结果
                self.detection_result = result
                
                # 显示结果信息
                changes_count = result.get("changes_count", 0)
                change_area = result.get("change_area", "未知")
                
                msg = f"变化检测完成！\n\n检测到变化区域：{changes_count} 处\n变化面积：{change_area}"
                QMessageBox.information(None, "处理完成", msg)
                return True
            else:
                error_msg = result.get("error", "未知错误")
                QMessageBox.critical(None, "处理失败", f"变化检测处理失败：{error_msg}")
                return False
                
        except Exception as e:
            # 恢复正常光标
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(None, "处理异常", f"发生未预期的错误：{str(e)}")
            return False
        finally:
            # 确保光标被恢复
            QApplication.restoreOverrideCursor()
    
    def export_result(self):
        """导出变化检测结果"""
        # 检查是否已完成检测
        if not self.model.detection_result:
            QMessageBox.warning(None, "警告", "请先进行变化检测")
            return
        
        # 让用户选择保存路径
        save_path, _ = QFileDialog.getSaveFileName(
            None,
            "保存变化检测结果",
            "",
            "GeoTIFF文件 (*.tif);;PNG图像 (*.png);;JPEG图像 (*.jpg);;所有文件 (*.*)"
        )
        
        if save_path:
            # 显示加载中提示
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            try:
                # 调用模型层导出结果
                success = self.model.export_result(save_path)
                
                # 恢复正常光标
                QApplication.restoreOverrideCursor()
                
                if success:
                    QMessageBox.information(None, "导出成功", f"变化检测结果已成功导出到：\n{save_path}")
                else:
                    QMessageBox.critical(None, "导出失败", 
                                       f"导出变化检测结果失败：{self.model.last_error}")
                    
            except Exception as e:
                # 恢复正常光标
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(None, "导出异常", f"发生未预期的错误：{str(e)}")
            finally:
                # 确保光标被恢复
                QApplication.restoreOverrideCursor() 