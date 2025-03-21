import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt
from ui.main_window import MainWindow

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 