from PySide6.QtWidgets import QFileDialog, QMessageBox
# 注释掉API导入，避免启动错误
# from Function.api.api_classification import ApiClassificationModel

class SceneController:
    """场景分类控制器类"""
    
    def __init__(self):
        """初始化控制器"""
        self.current_image = None
        # 注释掉API初始化，避免启动错误
        # self.api_model = ApiClassificationModel()
        self.page = None
    
    def setup(self, page=None):
        """设置控制器
        
        Args:
            page: 页面实例
        """
        self.page = page
    
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
    
    def start_classification(self):
        """开始场景分类"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像")
            return False
        
        # API暂不可用的提示
        QMessageBox.information(None, "API未连接", "API服务暂未连接，无法执行场景分类。")
        return False
    
    def export_result(self):
        """导出分类结果"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像")
            return False
        
        # API暂不可用的提示
        QMessageBox.information(None, "API未连接", "API服务暂未连接，无法导出分类结果。")
        return False 