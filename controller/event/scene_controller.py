from PySide6.QtWidgets import QFileDialog, QMessageBox

class SceneController:
    """场景分类控制器类"""
    
    def __init__(self):
        """初始化控制器"""
        self.current_image = None
    
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
    
    def start_classification(self):
        """开始场景分类"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像")
            return False
        
        # 这里实际上会调用功能层的场景分类功能
        # classification_result = self.classifier.classify(self.current_image)
        
        # 模拟成功的分类结果
        QMessageBox.information(None, "分类完成", "场景分类已完成，结果为: 城市区域")
        return True
    
    def export_result(self):
        """导出分类结果"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "没有可导出的分类结果")
            return False
        
        save_path, _ = QFileDialog.getSaveFileName(
            None,
            "保存分类结果",
            "",
            "图像文件 (*.png *.jpg *.tif);;文本文件 (*.txt *.csv);;所有文件 (*)"
        )
        
        if save_path:
            # 这里实际上会将分类结果导出到指定路径
            # self.classifier.export_result(save_path)
            
            # 模拟导出成功
            QMessageBox.information(None, "导出成功", f"分类结果已成功导出到: {save_path}")
            return True
        return False 