import sys
import os
import warnings

# 忽略所有警告
warnings.filterwarnings("ignore")

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt

# 导入主窗口
from ui.main_window_new import MainWindow

# 导入控制器
from controller.event.fishnet_controller import FishnetController
from controller.event.scene_controller import SceneController
from controller.event.segment_controller import SegmentController
from controller.event.object_detection_controller import ObjectDetectionController
from controller.event.setting_controller import SettingController
from controller.event.change_detection_controller import ChangeDetectionController
from controller.event.batch_controller import BatchController


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
    app.setStyle('Fusion')
    
    # 应用程序工作目录
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(app_dir)
    
    # 创建主窗口
    main_window = MainWindow()
    
    # 创建控制器实例
    fishnet_controller = FishnetController()
    scene_controller = SceneController()
    segment_controller = SegmentController()
    detection_controller = ObjectDetectionController()
    setting_controller = SettingController()
    change_detection_controller = ChangeDetectionController()
    batch_controller = BatchController()
    
    # 初始化控制器
    fishnet_controller.setup(page=main_window.fishnet_page)
    scene_controller.setup(page=main_window.scene_page)
    segment_controller.setup(page=main_window.segment_page)
    detection_controller.setup(page=main_window.detection_page)
    setting_controller.setup(page=main_window.setting_page)
    change_detection_controller.setup(page=main_window.change_detection_page)
    batch_controller.setup(page=main_window.batch_page)
    
    # 连接控制器和对应的UI页面
    main_window.fishnet_page.connect_signals(fishnet_controller)
    main_window.scene_page.connect_signals(scene_controller)
    main_window.segment_page.connect_signals(segment_controller)
    main_window.detection_page.connect_signals(detection_controller)
    main_window.setting_page.connect_signals(setting_controller)
    main_window.change_detection_page.connect_signals(change_detection_controller)
    main_window.batch_page.connect_signals(batch_controller)
    
    # 显示主窗口
    main_window.show()
    
    # 启动应用程序事件循环
    sys.exit(app.exec())


if __name__ == "__main__":
    sys.exit(main()) 