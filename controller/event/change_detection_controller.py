from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication
from PySide6.QtCore import QObject, Qt

import os
import sys
import time

# 注释掉API的导入
# from Function.api.api_change_detection import ApiChangeDetectionModel


class ChangeDetectionController(QObject):
    """变化检测页面的控制器类，处理UI与功能逻辑之间的交互"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # 注释掉API模型初始化
        # self.api_model = ApiChangeDetectionModel()
        
        # 当前加载的前后期影像路径
        self.before_image_path = None
        self.after_image_path = None
        
        # 页面引用
        self.page = None
    
    def setup(self, page=None):
        """设置页面引用"""
        self.page = page
    
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
                # 直接保存文件路径，不调用API
                self.before_image_path = file_path
                
                # 恢复正常光标
                QApplication.restoreOverrideCursor()
                
                # 准备图像信息消息
                filename = os.path.basename(file_path)
                
                msg = f"成功导入前期影像：{filename}"
                QMessageBox.information(None, "导入成功", msg)
                
                return True
                    
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
                # 直接保存文件路径，不调用API
                self.after_image_path = file_path
                
                # 恢复正常光标
                QApplication.restoreOverrideCursor()
                
                # 准备图像信息消息
                filename = os.path.basename(file_path)
                
                msg = f"成功导入后期影像：{filename}"
                QMessageBox.information(None, "导入成功", msg)
                
                return True
                    
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
        if not self.before_image_path or not self.after_image_path:
            QMessageBox.warning(None, "警告", "请先导入前期和后期影像")
            return False
        
        # API暂不可用的提示
        QMessageBox.information(None, "API未连接", "API服务暂未连接，无法执行变化检测。")
        return False
    
    def export_result(self):
        """导出变化检测结果"""
        # 检查是否有前后期影像
        if not self.before_image_path or not self.after_image_path:
            QMessageBox.warning(None, "警告", "请先导入前期和后期影像并进行变化检测")
            return False
        
        # API暂不可用的提示
        QMessageBox.information(None, "API未连接", "API服务暂未连接，无法导出变化检测结果。")
        return False 