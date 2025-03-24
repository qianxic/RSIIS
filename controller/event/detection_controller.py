from PySide6.QtWidgets import QFileDialog, QMessageBox

class DetectionController:
    """目标检测控制器类"""
    
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
    
    def start_detection(self):
        """开始目标检测"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像")
            return False
        
        # 这里实际上会调用功能层的目标检测功能
        # detection_result = self.detector.detect(self.current_image)
        
        # 模拟成功的检测结果
        QMessageBox.information(None, "检测完成", "目标检测已完成，共识别建筑物23个，车辆45辆，飞机2架")
        return True
    
    def export_result(self):
        """导出检测结果"""
        if not self.current_image:
            QMessageBox.warning(None, "操作失败", "没有可导出的检测结果")
            return False
        
        save_path, _ = QFileDialog.getSaveFileName(
            None,
            "保存检测结果",
            "",
            "图像文件 (*.png *.jpg *.tif);;所有文件 (*)"
        )
        
        if save_path:
            # 这里实际上会将检测结果导出到指定路径
            # self.detector.export_result(save_path)
            
            # 模拟导出成功
            QMessageBox.information(None, "导出成功", f"检测结果已成功导出到: {save_path}")
            return True
        return False 