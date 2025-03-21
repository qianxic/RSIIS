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
        
        # 主题标志
        self.is_dark_theme = False
        
        # 亮色主题样式表
        self.light_style = """
            QMainWindow {
                background-color: #FFFFFF;
                color: #333333;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QWidget {
                background-color: #FFFFFF;
                color: #333333;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QFrame#sidebar {
                background-color: #F5F5F7;
                border: none;
                border-radius: 12px;
                margin: 4px;
            }
            QPushButton {
                background-color: transparent;
                color: #333333;
                border: none;
                padding: 12px;
                text-align: left;
                border-radius: 8px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(230, 230, 235, 0.8);
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: rgba(66, 133, 244, 0.1);
                color: #4285F4;
                font-weight: bold;
            }
            QLabel#title {
                font-size: 18pt;
                font-weight: bold;
                color: #4285F4;
                padding: 12px 8px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                background-color: transparent;
                border-radius: 10px;
                margin: 4px 4px;
                letter-spacing: 1px;
            }
            QPushButton#operation_btn {
                background-color: #4285F4;
                color: #FFFFFF;
                padding: 10px 15px;
                font-weight: bold;
                border-radius: 8px;
                text-align: center;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 11pt;
            }
            QPushButton#operation_btn:hover {
                background-color: #5294FF;
            }
            QPushButton#operation_btn:pressed {
                background-color: #3A76E3;
            }
            QFrame#content_frame {
                background-color: #FFFFFF;
                border: 1px solid #EBEBEB;
                border-radius: 12px;
                margin: 10px;
                padding: 5px;
            }
            QLabel#page_title {
                font-size: 18pt;
                font-weight: bold;
                color: #333333;
                padding: 10px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QLabel#subtitle {
                font-size: 12pt;
                color: #555555;
                padding: 0px 10px 10px 10px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QLabel#section_title {
                font-size: 14pt;
                font-weight: bold;
                color: #333333;
                padding: 5px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QLabel {
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 11pt;
                color: #333333;
            }
            QTextEdit {
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 11pt;
                background-color: transparent;
                border: none;
                selection-background-color: rgba(66, 133, 244, 0.2);
                selection-color: #333333;
                border-radius: 8px;
                color: #333333;
            }
            QMenuBar {
                background-color: #FFFFFF;
                color: #333333;
                border-radius: 8px;
            }
            QStatusBar {
                background-color: #FFFFFF;
                color: #333333;
                border-radius: 8px;
            }
            QToolBar {
                background-color: #F5F5F7;
                border: none;
                border-radius: 8px;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                color: #333333;
            }
            QToolButton:hover {
                background-color: rgba(230, 230, 235, 0.8);
                border-radius: 8px;
            }
            QStackedWidget {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
            QFrame#about_frame {
                background-color: #F8F9FA;
                border-radius: 8px;
                padding: 5px;
            }
            QLabel#about_text {
                padding: 10px;
                color: #333333;
                font-size: 11pt;
            }
            QFrame#usage_frame {
                background-color: #F8F9FA;
                border-radius: 8px;
                padding: 5px;
            }
            QLabel#usage_text {
                padding: 10px;
                color: #333333;
                font-size: 11pt;
            }
            QFrame#separator {
                background-color: #E5E5E5;
                height: 1px;
                margin: 0px 10px;
            }
            QFrame#settings_area {
                background-color: #F8F9FA;
                border: 1px solid #E5E5E5;
                border-radius: 8px;
                padding: 5px;
            }
            /* 操作区样式 */
            QLabel[text="操作区"] {
                font-size: 14pt;
                font-weight: bold;
                color: #333333;
            }
            QFrame#operation_container {
                background-color: transparent;
            }
            QLabel#desc_text {
                color: #333333;
                font-size: 11pt;
                padding: 5px;
            }
            QLabel#group_title {
                color: #4285F4;
                font-weight: bold;
                font-size: 12pt;
                padding: 10px 5px 5px 5px;
                background-color: transparent;
            }
        """
        
        # 暗色主题样式表
        self.dark_style = """
            QMainWindow {
                background-color: #1E1E2E;
                color: #FFFFFF;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QWidget {
                background-color: #1E1E2E;
                color: #FFFFFF;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QFrame#sidebar {
                background-color: #2D2D3F;
                border: none;
                border-radius: 12px;
                margin: 4px;
            }
            QPushButton {
                background-color: transparent;
                color: #CCCCCC;
                border: none;
                padding: 12px;
                text-align: left;
                border-radius: 8px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 100, 0.6);
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: rgba(66, 133, 244, 0.2);
                color: #4285F4;
                font-weight: bold;
            }
            QLabel#title {
                font-size: 18pt;
                font-weight: bold;
                color: #4285F4;
                padding: 12px 8px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                background-color: transparent;
                border-radius: 10px;
                margin: 4px 4px;
                letter-spacing: 1px;
            }
            QPushButton#operation_btn {
                background-color: #4285F4;
                color: #FFFFFF;
                padding: 10px 15px;
                font-weight: bold;
                border-radius: 8px;
                text-align: center;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 11pt;
            }
            QPushButton#operation_btn:hover {
                background-color: #5294FF;
            }
            QPushButton#operation_btn:pressed {
                background-color: #3A76E3;
            }
            QFrame#content_frame {
                background-color: #2D2D3F;
                border: 1px solid #3F3F5F;
                border-radius: 12px;
                margin: 10px;
                padding: 5px;
            }
            QLabel#page_title {
                font-size: 18pt;
                font-weight: bold;
                color: #FFFFFF;
                padding: 10px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QLabel#subtitle {
                font-size: 12pt;
                color: #CCCCCC;
                padding: 0px 10px 10px 10px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QLabel#section_title {
                font-size: 14pt;
                font-weight: bold;
                color: #FFFFFF;
                padding: 5px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QLabel {
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 11pt;
                color: #AAAAAA;
            }
            QTextEdit {
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 11pt;
                background-color: transparent;
                border: none;
                selection-background-color: rgba(66, 133, 244, 0.3);
                selection-color: #FFFFFF;
                border-radius: 8px;
                color: #AAAAAA;
            }
            QMenuBar {
                background-color: #1E1E2E;
                color: #FFFFFF;
                border-radius: 8px;
            }
            QStatusBar {
                background-color: #1E1E2E;
                color: #AAAAAA;
                border-radius: 8px;
            }
            QToolBar {
                background-color: #2D2D3F;
                border: none;
                border-radius: 8px;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                color: #AAAAAA;
            }
            QToolButton:hover {
                background-color: rgba(80, 80, 100, 0.6);
                border-radius: 8px;
            }
            QStackedWidget {
                background-color: #1E1E2E;
                border-radius: 12px;
            }
            QFrame#about_frame {
                background-color: #2A2A3C;
                border-radius: 8px;
                padding: 5px;
                border: 1px solid #3F3F5F;
            }
            QLabel#about_text {
                padding: 10px;
                color: #AAAAAA;
                font-size: 11pt;
            }
            QFrame#usage_frame {
                background-color: #2A2A3C;
                border-radius: 8px;
                padding: 5px;
                border: 1px solid #3F3F5F;
            }
            QLabel#usage_text {
                padding: 10px;
                color: #AAAAAA;
                font-size: 11pt;
            }
            QFrame#separator {
                background-color: #3F3F5F;
                height: 1px;
                margin: 0px 10px;
            }
            QFrame#settings_area {
                background-color: #2A2A3C;
                border: 1px solid #3F3F5F;
                border-radius: 8px;
                padding: 5px;
            }
            /* 操作区样式 */
            QLabel[text="操作区"] {
                font-size: 14pt;
                font-weight: bold;
                color: #FFFFFF;
            }
            QFrame#operation_container {
                background-color: transparent;
            }
            QLabel#desc_text {
                color: #AAAAAA;
                font-size: 11pt;
                padding: 5px;
            }
            QLabel#group_title {
                color: #4285F4;
                font-weight: bold;
                font-size: 12pt;
                padding: 10px 5px 5px 5px;
                background-color: transparent;
            }
        """
        
        # 应用主题样式
        self.setStyleSheet(self.light_style)
        
        # 设置窗口背景色为白色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#FFFFFF"))
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
        
        title_label = QLabel("RSIIS")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setMinimumHeight(60)  # 减小标题高度
        title_layout.addWidget(title_label)
        
        sidebar_layout.addWidget(title_container)
        sidebar_layout.addSpacing(10)  # 增加间距
        
        # 添加分隔线
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setObjectName("separator")  # 添加对象名以便于样式表选择
        sidebar_layout.addWidget(self.separator)
        sidebar_layout.addSpacing(10)  # 增加间距
        
        # 创建功能按钮 - 首页组
        self.home_btn = self.create_menu_button("首页")
        sidebar_layout.addWidget(self.home_btn)
        
        # 添加分隔线
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setObjectName("separator")
        sidebar_layout.addWidget(separator2)
        
        # 数据处理组按钮
        self.data_btn = self.create_menu_button("数据获取")
        self.preprocess_btn = self.create_menu_button("数据处理")
        self.fishnet_btn = self.create_menu_button("渔网分割")
        
        sidebar_layout.addWidget(self.data_btn)
        sidebar_layout.addWidget(self.preprocess_btn)
        sidebar_layout.addWidget(self.fishnet_btn)
        
        # 添加分隔线
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.HLine)
        separator3.setFrameShadow(QFrame.Sunken)
        separator3.setObjectName("separator")
        sidebar_layout.addWidget(separator3)
        
        # 分析解译组按钮
        self.scene_btn = self.create_menu_button("场景分类")
        self.segment_btn = self.create_menu_button("语义分割")
        self.detection_btn = self.create_menu_button("目标检测")
        self.change_detection_btn = self.create_menu_button("变化检测")
        
        sidebar_layout.addWidget(self.scene_btn)
        sidebar_layout.addWidget(self.segment_btn)
        sidebar_layout.addWidget(self.detection_btn)
        sidebar_layout.addWidget(self.change_detection_btn)
        
        # 添加弹性空间
        sidebar_layout.addStretch()
        
        # 添加操作按钮 (设置按钮)
        settings_btn = QPushButton("设置")
        settings_btn.setObjectName("operation_btn")
        settings_btn.clicked.connect(lambda: self.select_button(None, 8))
        sidebar_layout.addWidget(settings_btn)
        sidebar_layout.addSpacing(10)
        
        # 创建堆叠部件容器，用于显示不同的内容页面
        self.content_stack = QStackedWidget()
        
        # 创建各个功能区页面
        self.home_page = self.create_home_page()
        self.data_page = self.create_data_page()
        self.preprocess_page = self.create_preprocess_page()
        self.fishnet_page = self.create_fishnet_page()
        self.scene_page = self.create_scene_page()
        self.segment_page = self.create_segment_page()
        self.detection_page = self.create_detection_page()
        self.change_detection_page = self.create_change_detection_page()
        self.setting_page = self.create_setting_page()
        
        # 将页面添加到堆叠部件
        self.content_stack.addWidget(self.home_page)
        self.content_stack.addWidget(self.data_page)
        self.content_stack.addWidget(self.preprocess_page)
        self.content_stack.addWidget(self.fishnet_page)
        self.content_stack.addWidget(self.scene_page)
        self.content_stack.addWidget(self.segment_page)
        self.content_stack.addWidget(self.detection_page)
        self.content_stack.addWidget(self.change_detection_page)
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
        self.data_btn.clicked.connect(lambda: self.select_button(self.data_btn, 1))
        self.preprocess_btn.clicked.connect(lambda: self.select_button(self.preprocess_btn, 2))
        self.fishnet_btn.clicked.connect(lambda: self.select_button(self.fishnet_btn, 3))
        self.scene_btn.clicked.connect(lambda: self.select_button(self.scene_btn, 4))
        self.segment_btn.clicked.connect(lambda: self.select_button(self.segment_btn, 5))
        self.detection_btn.clicked.connect(lambda: self.select_button(self.detection_btn, 6))
        self.change_detection_btn.clicked.connect(lambda: self.select_button(self.change_detection_btn, 7))
        
        # 设置默认选中按钮
        self.home_btn.setChecked(True)
        self.content_stack.setCurrentIndex(0)
    
    def create_menu_button(self, text):
        """创建侧边栏菜单按钮"""
        button = QPushButton(text)
        button.setCheckable(True)
        button.setMinimumHeight(40)
        
        # 设置更大更粗的字体
        font = QFont()
        font.setPointSize(12)  # 增加字体大小，原来可能是11pt
        font.setBold(True)     # 设置字体为粗体
        button.setFont(font)
        
        return button
    
    def select_button(self, button, page_index):
        """选择按钮，并切换对应的功能页面"""
        # 重置所有按钮状态
        for btn in [self.home_btn, self.data_btn, self.preprocess_btn, self.fishnet_btn,
                   self.scene_btn, self.segment_btn, self.detection_btn, self.change_detection_btn]:
            btn.setChecked(False)
        
        # 设置当前按钮为选中状态（如果不是None）
        if button:
            button.setChecked(True)
        
        # 切换到对应的内容页面
        self.content_stack.setCurrentIndex(page_index)
    
    def create_home_page(self):
        """创建首页"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("遥感影像智能解译系统")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("专业的遥感影像处理与分析平台")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("系统功能介绍")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        desc = QLabel("本系统提供遥感影像智能解译功能，包含数据获取、预处理、渔网分割、场景分类、语义分割、目标检测和变化检测等多种功能模块。")
        desc.setWordWrap(True)
        desc.setObjectName("desc_text")
        content_layout.addWidget(desc)
        
        section_title2 = QLabel("使用说明")
        section_title2.setObjectName("section_title")
        content_layout.addWidget(section_title2)
        
        usage_frame = QFrame()
        usage_frame.setObjectName("usage_frame")
        usage_layout = QVBoxLayout(usage_frame)
        
        usage = QLabel("1. 点击左侧菜单选择功能\n2. 导入或获取遥感影像数据\n3. 进行数据预处理和格式调整\n4. 选择合适的分析功能并设置参数\n5. 执行解译任务\n6. 查看和导出结果")
        usage.setWordWrap(True)
        usage.setObjectName("usage_text")
        usage_layout.addWidget(usage)
        
        content_layout.addWidget(usage_frame)
        
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
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        import_btn = QPushButton("导入遥感影像")
        import_btn.setObjectName("operation_btn")
        import_btn.setFixedWidth(180)
        import_btn.setFixedHeight(40)
        button_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始场景分类")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出分类结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
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
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        import_btn = QPushButton("导入遥感影像")
        import_btn.setObjectName("operation_btn")
        import_btn.setFixedWidth(180)
        import_btn.setFixedHeight(40)
        button_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始语义分割")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出分割结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
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
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        import_btn = QPushButton("导入遥感影像")
        import_btn.setObjectName("operation_btn")
        import_btn.setFixedWidth(180)
        import_btn.setFixedHeight(40)
        button_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始目标检测")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出检测结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
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
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("常规设置")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 常规设置内容区域
        settings_area = QFrame()
        settings_area.setObjectName("settings_area")
        settings_layout = QVBoxLayout(settings_area)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        self.theme_btn = QPushButton("切换到暗色主题")  # 保存引用以便更新文本
        self.theme_btn.setObjectName("operation_btn")
        self.theme_btn.setFixedWidth(180)
        self.theme_btn.setFixedHeight(40)
        self.theme_btn.clicked.connect(self.toggle_theme)
        button_layout.addWidget(self.theme_btn)
        
        auth_btn = QPushButton("账户与授权")
        auth_btn.setObjectName("operation_btn")
        auth_btn.setFixedWidth(180)
        auth_btn.setFixedHeight(40)
        button_layout.addWidget(auth_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        settings_layout.addWidget(button_container)
        
        content_layout.addWidget(settings_area)
        
        # 添加关于部分
        section_title2 = QLabel("关于系统")
        section_title2.setObjectName("section_title")
        content_layout.addWidget(section_title2)
        
        about_frame = QFrame()
        about_frame.setObjectName("about_frame")  # 添加对象名称以便于样式表选择
        content_layout.addWidget(about_frame)
        
        about_layout = QVBoxLayout(about_frame)
        
        self.about_text = QLabel("遥感影像智能解译系统 V1.0\n© 2023-2024 RSIIS团队 版权所有")
        self.about_text.setWordWrap(True)
        self.about_text.setObjectName("about_text")  # 添加对象名称以便于样式表选择
        about_layout.addWidget(self.about_text)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page
    
    def toggle_theme(self):
        """切换主题样式"""
        # 切换主题标志
        self.is_dark_theme = not self.is_dark_theme
        
        if self.is_dark_theme:
            # 切换到暗色主题
            self.setStyleSheet(self.dark_style)
            # 更新窗口背景
            palette = self.palette()
            palette.setColor(QPalette.Window, QColor("#1E1E2E"))
            self.setPalette(palette)
            # 更新按钮文本
            if hasattr(self, 'theme_btn'):
                self.theme_btn.setText("切换到亮色主题")
        else:
            # 切换到亮色主题
            self.setStyleSheet(self.light_style)
            # 更新窗口背景
            palette = self.palette()
            palette.setColor(QPalette.Window, QColor("#FFFFFF"))
            self.setPalette(palette)
            # 更新按钮文本
            if hasattr(self, 'theme_btn'):
                self.theme_btn.setText("切换到暗色主题")
    
    def create_data_page(self):
        """创建数据获取页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("数据获取")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("获取遥感影像数据，支持多种来源和格式")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        import_btn = QPushButton("本地导入")
        import_btn.setObjectName("operation_btn")
        import_btn.setFixedWidth(180)
        import_btn.setFixedHeight(40)
        button_layout.addWidget(import_btn)
        
        download_btn = QPushButton("在线下载")
        download_btn.setObjectName("operation_btn")
        download_btn.setFixedWidth(180)
        download_btn.setFixedHeight(40)
        button_layout.addWidget(download_btn)
        
        manage_btn = QPushButton("数据管理")
        manage_btn.setObjectName("operation_btn")
        manage_btn.setFixedWidth(180)
        manage_btn.setFixedHeight(40)
        button_layout.addWidget(manage_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page
    
    def create_preprocess_page(self):
        """创建数据预处理页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("数据预处理")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("对遥感影像进行预处理，提高数据质量")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        import_btn = QPushButton("导入遥感影像")
        import_btn.setObjectName("operation_btn")
        import_btn.setFixedWidth(180)
        import_btn.setFixedHeight(40)
        button_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始预处理")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出处理结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page
    
    def create_fishnet_page(self):
        """创建渔网分割页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("渔网分割")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("对遥感影像进行网格化处理，便于精确分析")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        import_btn = QPushButton("导入遥感影像")
        import_btn.setObjectName("operation_btn")
        import_btn.setFixedWidth(180)
        import_btn.setFixedHeight(40)
        button_layout.addWidget(import_btn)
        
        grid_btn = QPushButton("设置网格参数")
        grid_btn.setObjectName("operation_btn")
        grid_btn.setFixedWidth(180)
        grid_btn.setFixedHeight(40)
        button_layout.addWidget(grid_btn)
        
        process_btn = QPushButton("开始分割")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出分割结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page
    
    def create_change_detection_page(self):
        """创建变化检测页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("变化检测")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("对多时相遥感影像进行变化检测，分析地物变化情况")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        section_title = QLabel("操作区")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        # 创建按钮容器，水平布局
        button_container = QFrame()
        button_container.setObjectName("operation_container")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        
        import_btn1 = QPushButton("导入前时相影像")
        import_btn1.setObjectName("operation_btn")
        import_btn1.setFixedWidth(180)
        import_btn1.setFixedHeight(40)
        button_layout.addWidget(import_btn1)
        
        import_btn2 = QPushButton("导入后时相影像")
        import_btn2.setObjectName("operation_btn")
        import_btn2.setFixedWidth(180)
        import_btn2.setFixedHeight(40)
        button_layout.addWidget(import_btn2)
        
        process_btn = QPushButton("开始变化检测")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出检测结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page 