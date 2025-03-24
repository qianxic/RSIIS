from PySide6.QtWidgets import QFileDialog, QMessageBox

class BaseController:
    """基础控制器类，提供常用的方法"""
    
    def __init__(self):
        """初始化控制器"""
        self.current_image = None
        self.module_name = "通用"  # 子类应该覆盖这个属性
    
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
    
    def export_result(self):
        """导出处理结果"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", f"没有可导出的{self.module_name}结果")
            return False
        
        save_path, _ = QFileDialog.getSaveFileName(
            None,
            f"保存{self.module_name}结果",
            "",
            "图像文件 (*.png *.jpg *.tif);;所有文件 (*)"
        )
        
        if save_path:
            # 模拟导出成功
            QMessageBox.information(None, "导出成功", f"{self.module_name}结果已成功导出到: {save_path}")
            return True
        return False
    
    def check_image_loaded(self):
        """检查是否已加载影像"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像")
            return False
        return True 