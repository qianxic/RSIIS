from PySide6.QtWidgets import QFileDialog, QMessageBox
# 注释掉API导入，避免启动错误
# from Function.api.api_detection import ApiDetectionModel

class ObjectDetectionController:
    """目标检测控制器类"""
    
    def __init__(self):
        """初始化控制器"""
        self.current_image = None
        # 注释掉API初始化，避免启动错误
        # self.api_model = ApiDetectionModel()
        self.page = None
        self.last_error = None
    
    def setup(self, page=None):
        """设置控制器
        
        Args:
            page: 页面实例
        """
        self.page = page
        # API暂不初始化
        # try:
        #     self.api_model = ApiDetectionModel()
        # except Exception as e:
        #     self.last_error = str(e)
    
    def import_image(self):
        """导入遥感影像"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, 
            "选择遥感影像", 
            "", 
            "图像文件 (*.tif *.jpg *.png *.bmp);;所有文件 (*)"
        )
        
        if file_path:
            # 直接保存图像路径，不调用API
            self.current_image = file_path
            QMessageBox.information(None, "导入成功", f"成功导入遥感影像: {file_path}")
            return True
        return False
    
    def start_detection(self):
        """开始目标检测"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像")
            return False
        
        try:
            # API暂不可用的提示
            QMessageBox.information(None, "API未连接", "API服务暂未连接，无法执行目标检测。")
            return False
        except Exception as e:
            QMessageBox.critical(None, "操作失败", f"目标检测失败: {str(e)}")
            return False
    
    def export_result(self):
        """导出检测结果"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像")
            return False
        
        # API暂不可用的提示
        QMessageBox.information(None, "API未连接", "API服务暂未连接，无法导出检测结果。")
        return False 