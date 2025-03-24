from PySide6.QtWidgets import QFileDialog, QMessageBox

class SampleMakingController:
    """批量影像解译控制器类"""
    
    def __init__(self):
        """初始化控制器"""
        self.dataset = None
    
    def import_dataset(self):
        """导入遥感影像数据集"""
        folder_path = QFileDialog.getExistingDirectory(
            None, 
            "选择遥感影像数据集文件夹", 
            ""
        )
        
        if folder_path:
            self.dataset = folder_path
            QMessageBox.information(None, "导入成功", f"成功导入数据集: {folder_path}")
            return True
        return False
    
    def start_batch_processing(self):
        """开始批量影像解译"""
        if not self.dataset:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像数据集")
            return False
        
        # 这里实际上会调用功能层的批量解译功能
        # batch_result = self.batch_processor.process(self.dataset)
        
        # 模拟成功的批量解译结果
        QMessageBox.information(None, "批量解译完成", "批量影像解译已完成，共处理47张影像")
        return True
    
    def export_results(self):
        """导出解译结果"""
        if not self.dataset:
            QMessageBox.warning(None, "操作失败", "没有可导出的解译结果")
            return False
        
        save_path = QFileDialog.getExistingDirectory(
            None,
            "选择导出结果保存位置",
            ""
        )
        
        if save_path:
            # 这里实际上会将批量解译结果导出到指定路径
            # self.batch_processor.export_results(save_path)
            
            # 模拟导出成功
            QMessageBox.information(None, "导出成功", f"批量解译结果已成功导出到: {save_path}")
            return True
        return False 