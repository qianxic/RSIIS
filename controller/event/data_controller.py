from PySide6.QtWidgets import QFileDialog, QMessageBox

class DataController:
    """数据获取控制器类"""
    
    def __init__(self):
        """初始化控制器"""
        self.data_list = []
    
    def import_local(self):
        """本地导入遥感影像"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            None, 
            "选择遥感影像", 
            "", 
            "图像文件 (*.tif *.jpg *.png *.bmp);;所有文件 (*)"
        )
        
        if file_paths:
            self.data_list.extend(file_paths)
            QMessageBox.information(None, "导入成功", f"成功导入{len(file_paths)}个遥感影像文件")
            return True
        return False
    
    def download_data(self):
        """在线下载遥感数据"""
        # 这里实际上会连接到数据下载功能
        # 模拟下载行为
        QMessageBox.information(None, "下载中", "正在连接遥感数据服务器，准备下载数据...")
        
        # 模拟下载成功
        QMessageBox.information(None, "下载完成", "已成功下载3景遥感影像")
        return True
    
    def manage_data(self):
        """管理数据"""
        if not self.data_list:
            QMessageBox.warning(None, "操作失败", "当前没有可管理的数据")
            return False
        
        QMessageBox.information(None, "数据管理", f"当前共有{len(self.data_list)}个数据文件")
        return True 