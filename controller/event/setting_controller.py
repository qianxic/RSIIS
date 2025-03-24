from PySide6.QtWidgets import QMessageBox

class SettingController:
    """设置控制器类"""
    
    def __init__(self):
        """初始化控制器"""
        self.is_logged_in = False
    
    def manage_account(self):
        """管理账户"""
        if not self.is_logged_in:
            # 模拟登录
            QMessageBox.information(None, "账户管理", "请先登录您的账户")
            self.is_logged_in = True
            return True
        else:
            # 模拟账户管理
            QMessageBox.information(None, "账户管理", "当前已登录，用户: admin@rsiis.com")
            return True 