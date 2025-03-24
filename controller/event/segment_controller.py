from PySide6.QtWidgets import QFileDialog, QMessageBox

class SegmentController:
    """语义分割控制器类"""
    
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
    
    def start_segmentation(self):
        """开始语义分割"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像")
            return False
        
        # 这里实际上会调用功能层的语义分割功能
        # segmentation_result = self.segmenter.segment(self.current_image)
        
        # 模拟成功的分割结果
        QMessageBox.information(None, "分割完成", "语义分割已完成，已识别建筑物、道路、植被等类别")
        return True
    
    def export_result(self):
        """导出分割结果"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "没有可导出的分割结果")
            return False
        
        save_path, _ = QFileDialog.getSaveFileName(
            None,
            "保存分割结果",
            "",
            "图像文件 (*.png *.jpg *.tif);;所有文件 (*)"
        )
        
        if save_path:
            # 这里实际上会将分割结果导出到指定路径
            # self.segmenter.export_result(save_path)
            
            # 模拟导出成功
            QMessageBox.information(None, "导出成功", f"分割结果已成功导出到: {save_path}")
            return True
        return False 