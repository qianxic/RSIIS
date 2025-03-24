from PySide6.QtWidgets import QMessageBox
from controller.event.base_controller import BaseController

class PreprocessController(BaseController):
    """数据预处理控制器类"""
    
    def __init__(self):
        """初始化控制器"""
        super().__init__()
        self.module_name = "数据预处理"
    
    def start_preprocess(self):
        """开始数据预处理"""
        if not self.check_image_loaded():
            return False
        
        # 这里实际上会调用功能层的数据预处理功能
        # preprocess_result = self.preprocessor.process(self.current_image)
        
        # 模拟成功的预处理结果
        QMessageBox.information(None, "预处理完成", "数据预处理已完成，已应用辐射校正、几何校正和图像增强")
        return True 