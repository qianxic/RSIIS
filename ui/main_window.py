from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QLabel, QFrame, QStackedWidget, QTextEdit)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QLinearGradient, QBrush, QPalette, QColor, QTextCursor

class SelectableLabel(QTextEdit):
    """可选择的标签类，提供文本选择功能"""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFrameShape(QTextEdit.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.setText(text)
        # 解决高度自适应问题
        self.document().contentsChanged.connect(self.adjustHeight)
        self.adjustHeight()
    
    def adjustHeight(self):
        """根据内容调整高度"""
        self.setMinimumHeight(self.document().size().height())
    
    def setWordWrap(self, wrap):
        """设置是否自动换行"""
        self.setLineWrapMode(QTextEdit.WidgetWidth if wrap else QTextEdit.NoWrap)
    
    def setText(self, text):
        """设置文本内容"""
        super().setText(text)
        self.adjustHeight()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口标题和初始大小
        self.setWindowTitle("遥感影像智能解译系统 V1.0")
        self.resize(1200, 800)
        
        # 设置窗口样式
        self.setWindowFlags(Qt.Window)
        
        # 应用主题样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f7f7f7;
                color: #4a4a4a;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QWidget {
                background-color: #f7f7f7;
                color: #4a4a4a;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QFrame#sidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #e1e4e8, stop:0.3 #b5bdc4, stop:0.7 #b5bdc4, stop:1 #939ca3);
                border: none;
                border-radius: 12px;
                margin: 4px;
            }
            QPushButton {
                background-color: rgba(180, 180, 180, 0.2);
                color: #4a4a4a;
                border: none;
                padding: 10px;
                text-align: left;
                border-radius: 8px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: rgba(180, 180, 180, 0.4);
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: rgba(150, 150, 150, 0.6);
                color: #333333;
                font-weight: bold;
            }
            QLabel#title {
                font-size: 12pt;
                font-weight: bold;
                color: #333333;
                padding: 12px 8px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #e1e4e8, stop:1 #b5bdc4);
                border-radius: 10px;
                margin: 4px 4px;
                text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.9);
                letter-spacing: 1px;
            }
            QPushButton#operation_btn {
                background-color: #b0b0b0;
                color: #333333;
                padding: 8px 15px;
                font-weight: bold;
                border-radius: 8px;
                text-align: center;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 11pt;
            }
            QPushButton#operation_btn:hover {
                background-color: #c0c0c0;
                border: 1px solid #a0a0a0;
            }
            QFrame#content_frame {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                margin: 10px;
            }
            QLabel#page_title {
                font-size: 16pt;
                font-weight: bold;
                color: #4a4a4a;
                padding: 10px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QLabel#section_title {
                font-size: 13pt;
                font-weight: bold;
                color: #4a4a4a;
                padding: 5px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QLabel {
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 10pt;
                color: #4a4a4a;
            }
            QTextEdit {
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 10pt;
                background-color: transparent;
                border: none;
                selection-background-color: rgba(180, 180, 180, 0.4);
                selection-color: #333333;
                border-radius: 8px;
                color: #4a4a4a;
            }
            QMenuBar {
                background-color: #f7f7f7;
                color: #4a4a4a;
                border-radius: 8px;
            }
            QStatusBar {
                background-color: #f7f7f7;
                color: #4a4a4a;
                border-radius: 8px;
            }
            QToolBar {
                background-color: #e0e0e0;
                border: none;
                border-radius: 8px;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                color: #4a4a4a;
            }
            QToolButton:hover {
                background-color: rgba(180, 180, 180, 0.3);
                border-radius: 8px;
            }
            QStackedWidget {
                background-color: #f7f7f7;
                border-radius: 12px;
            }
        """)
        
        # 设置窗口背景色为淡灰色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f7f7f7"))
        self.setPalette(palette)
        
        # 创建主界面布局
        main_layout = QHBoxLayout()
        main_layout.setSpacing(8)  # 增加组件间距
        main_layout.setContentsMargins(8, 8, 8, 8)  # 设置边距
        
        # 创建左侧功能区
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(8, 8, 8, 8)  # 增加内边距
        sidebar_layout.setSpacing(8)  # 增加间距
        
        # 系统标题
        title_container = QFrame()
        title_container.setObjectName("title_container")
        title_container.setStyleSheet("background: transparent;")
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("遥感影像智能解译系统")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setMinimumHeight(80)  # 减小标题高度
        title_layout.addWidget(title_label)
        
        sidebar_layout.addWidget(title_container)
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: rgba(160, 160, 160, 0.5); border-radius: 4px;")
        sidebar_layout.addWidget(separator)
        
        # 创建功能按钮
        self.home_btn = self.create_menu_button("主界面")
        self.scene_btn = self.create_menu_button("场景分类")
        self.segment_btn = self.create_menu_button("语义分割")
        self.detection_btn = self.create_menu_button("目标检测")
        
        sidebar_layout.addWidget(self.home_btn)
        sidebar_layout.addWidget(self.scene_btn)
        sidebar_layout.addWidget(self.segment_btn)
        sidebar_layout.addWidget(self.detection_btn)
        
        # 添加弹性空间
        sidebar_layout.addStretch()
        
        # 添加操作按钮 (设置按钮)
        settings_btn = QPushButton("设置")
        settings_btn.setObjectName("operation_btn")
        settings_btn.clicked.connect(lambda: self.select_button(None, 4))
        sidebar_layout.addWidget(settings_btn)
        sidebar_layout.addSpacing(10)
        
        # 创建堆叠部件容器，用于显示不同的内容页面
        self.content_stack = QStackedWidget()
        
        # 创建各个功能区页面
        self.home_page = self.create_home_page()
        self.scene_page = self.create_scene_page()
        self.segment_page = self.create_segment_page()
        self.detection_page = self.create_detection_page()
        self.setting_page = self.create_setting_page()
        
        # 将页面添加到堆叠部件
        self.content_stack.addWidget(self.home_page)
        self.content_stack.addWidget(self.scene_page)
        self.content_stack.addWidget(self.segment_page)
        self.content_stack.addWidget(self.detection_page)
        self.content_stack.addWidget(self.setting_page)
        
        # 将各部分添加到主布局
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack, 1)  # 内容区占据剩余空间
        
        # 创建中央部件并设置布局
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # 连接按钮信号
        self.home_btn.clicked.connect(lambda: self.select_button(self.home_btn, 0))
        self.scene_btn.clicked.connect(lambda: self.select_button(self.scene_btn, 1))
        self.segment_btn.clicked.connect(lambda: self.select_button(self.segment_btn, 2))
        self.detection_btn.clicked.connect(lambda: self.select_button(self.detection_btn, 3))
        
        # 设置默认选中按钮
        self.home_btn.setChecked(True)
        self.content_stack.setCurrentIndex(0)
    
    def create_menu_button(self, text):
        """创建侧边栏菜单按钮"""
        button = QPushButton(text)
        button.setCheckable(True)
        button.setMinimumHeight(40)
        return button
    
    def select_button(self, button, page_index):
        """选择按钮，并切换对应的功能页面"""
        # 重置所有按钮状态
        for btn in [self.home_btn, self.scene_btn, self.segment_btn, self.detection_btn]:
            btn.setChecked(False)
        
        # 设置当前按钮为选中状态（如果不是None）
        if button:
            button.setChecked(True)
        
        # 切换到对应的内容页面
        self.content_stack.setCurrentIndex(page_index)
    
    def create_home_page(self):
        """创建主界面页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("主界面")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("欢迎使用遥感影像智能解译系统")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("系统功能介绍")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        desc = QLabel("本系统提供遥感影像智能解译功能，包括场景分类、语义分割和目标检测三大功能。")
        desc.setWordWrap(True)
        content_layout.addWidget(desc)
        
        section_title2 = QLabel("使用说明")
        section_title2.setObjectName("section_title")
        content_layout.addWidget(section_title2)
        
        usage = QLabel("1. 点击左侧菜单选择功能\n2. 导入遥感影像数据\n3. 设置处理参数\n4. 执行解译任务\n5. 查看和导出结果")
        usage.setWordWrap(True)
        content_layout.addWidget(usage)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page
    
    def create_scene_page(self):
        """创建场景分类页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("场景分类")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("对遥感影像进行场景分类，识别不同地物类型")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        import_btn = QPushButton("导入遥感影像")
        import_btn.setObjectName("operation_btn")
        import_btn.setFixedWidth(200)
        content_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始场景分类")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(200)
        content_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出分类结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(200)
        content_layout.addWidget(export_btn)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page
    
    def create_segment_page(self):
        """创建语义分割页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("语义分割")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("对遥感影像进行语义分割，像素级别区分不同地物类型")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        import_btn = QPushButton("导入遥感影像")
        import_btn.setObjectName("operation_btn")
        import_btn.setFixedWidth(200)
        content_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始语义分割")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(200)
        content_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出分割结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(200)
        content_layout.addWidget(export_btn)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page
    
    def create_detection_page(self):
        """创建目标检测页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("目标检测")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("对遥感影像进行目标检测，识别并定位特定目标")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        import_btn = QPushButton("导入遥感影像")
        import_btn.setObjectName("operation_btn")
        import_btn.setFixedWidth(200)
        content_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始目标检测")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(200)
        content_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出检测结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(200)
        content_layout.addWidget(export_btn)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page
    
    def create_setting_page(self):
        """创建设置页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("设置")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("系统设置和参数配置")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("常规设置")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        theme_btn = QPushButton("切换主题")
        theme_btn.setObjectName("operation_btn")
        theme_btn.setFixedWidth(200)
        content_layout.addWidget(theme_btn)
        
        auth_btn = QPushButton("账户与授权")
        auth_btn.setObjectName("operation_btn")
        auth_btn.setFixedWidth(200)
        content_layout.addWidget(auth_btn)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page 