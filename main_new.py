import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt

# 导入主窗口
from ui.main_window_new import MainWindow

# 导入控制器
from controller.event.fishnet_controller import FishnetController
from controller.event.scene_controller import SceneController
from controller.event.segment_controller import SegmentController
from controller.event.detection_controller import DetectionController
from controller.event.data_controller import DataController
from controller.event.sample_making_controller import SampleMakingController
from controller.event.setting_controller import SettingController


# 设置Qt插件路径
if hasattr(Qt, 'AA_ShareOpenGLContexts'):
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# 获取Python环境中的Qt插件路径
if getattr(sys, 'frozen', False):
    # 如果是打包后的可执行文件
    qt_plugin_path = os.path.join(os.path.dirname(sys.executable), 'plugins')
else:
    # 如果是源码运行
    import PySide6
    qt_plugin_path = os.path.join(os.path.dirname(PySide6.__file__), 'plugins')

# 设置环境变量
os.environ['QT_PLUGIN_PATH'] = qt_plugin_path
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(qt_plugin_path, 'platforms')

def main():
    """主程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    main_window = MainWindow()
    
    # 创建各个页面的控制器实例
    fishnet_controller = FishnetController()
    scene_controller = SceneController()
    segment_controller = SegmentController()
    detection_controller = DetectionController()
    data_controller = DataController()
    sample_making_controller = SampleMakingController()
    setting_controller = SettingController()
    
    # 先设置控制器的页面引用，再连接信号
    fishnet_controller.setup(page=main_window.fishnet_page)
    
    # 连接控制器和对应的UI页面
    main_window.fishnet_page.connect_signals(fishnet_controller)
    main_window.scene_page.connect_signals(scene_controller)
    main_window.segment_page.connect_signals(segment_controller)
    main_window.detection_page.connect_signals(detection_controller)
    main_window.data_page.connect_signals(data_controller)
    main_window.sample_making_page.connect_signals(sample_making_controller)
    main_window.setting_page.connect_signals(setting_controller)
    
    # 显示主窗口
    main_window.show()
    
    # 启动应用程序事件循环
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 