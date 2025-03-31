from PySide6.QtWidgets import QFileDialog, QMessageBox

# 移除对API的依赖
# from .api_base_controller import ApiBaseController


class SegmentController:
    """语义分割控制器类"""
    
    def __init__(self, parent=None):
        """初始化控制器"""
        self.current_image = None
        self.page = None
    
    def setup(self, page=None):
        """设置控制器
        
        Args:
            page: 页面实例
        """
        self.page = page
        
        # 暂时不初始化API客户端
        # self.setup_api(page)
    
    def import_image(self):
        """导入遥感影像"""
        file_path, _ = QFileDialog.getOpenFileName(
            None, 
            "选择遥感影像", 
            "", 
            "图像文件 (*.tif *.jpg *.png *.bmp);;所有文件 (*)"
        )
        
        if file_path:
            self.current_image = file_path
            QMessageBox.information(None, "导入成功", f"成功导入遥感影像: {file_path}")
            return True
        return False
    
    def start_segmentation(self):
        """开始语义分割"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像")
            return False
        
        # API暂不可用提示
        QMessageBox.information(None, "API未连接", "API服务暂未连接，无法执行语义分割。")
        return False
    
    def export_result(self):
        """导出分割结果"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "没有可导出的分割结果")
            return False
        
        # API暂不可用提示
        QMessageBox.information(None, "API未连接", "API服务暂未连接，无法导出分割结果。")
        return False 