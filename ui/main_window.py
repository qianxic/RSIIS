from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QLabel, QFrame, QStackedWidget, QTextEdit, QScrollArea)
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QFont, QIcon, QLinearGradient, QBrush, QPalette, QColor, QTextCursor, QPixmap, QCursor, QDesktopServices

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
                background-color: transparent;
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
                padding: 0px;
                margin-top: 0px;
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
                background-color: transparent;
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
                background-color: #1B1B22;
                color: #E4E4E7;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QWidget {
                background-color: #1B1B22;
                color: #E4E4E7;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QFrame#sidebar {
                background-color: #27272F;
                border: none;
                border-radius: 12px;
                margin: 4px;
            }
            QPushButton {
                background-color: transparent;
                color: #CCCCDC;
                border: none;
                padding: 12px;
                text-align: left;
                border-radius: 8px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 110, 0.6);
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: rgba(66, 133, 244, 0.18);
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
                background-color: #27272F;
                border: 1px solid #33333C;
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
                color: #CCCCDC;
                padding: 0px 10px 10px 10px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
            }
            QLabel#section_title {
                font-size: 14pt;
                font-weight: bold;
                color: #FFFFFF;
                padding: 5px;
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                background-color: transparent;
            }
            QLabel {
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 11pt;
                color: #ACACBE;
            }
            QTextEdit {
                font-family: "Microsoft YaHei", "微软雅黑", "SimHei", "黑体", Arial, sans-serif;
                font-size: 11pt;
                background-color: transparent;
                border: none;
                selection-background-color: rgba(66, 133, 244, 0.3);
                selection-color: #FFFFFF;
                border-radius: 8px;
                color: #ACACBE;
            }
            QMenuBar {
                background-color: #1B1B22;
                color: #FFFFFF;
                border-radius: 8px;
            }
            QStatusBar {
                background-color: #1B1B22;
                color: #ACACBE;
                border-radius: 8px;
            }
            QToolBar {
                background-color: #27272F;
                border: none;
                border-radius: 8px;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                color: #ACACBE;
            }
            QToolButton:hover {
                background-color: rgba(80, 80, 110, 0.6);
                border-radius: 8px;
            }
            QStackedWidget {
                background-color: #1B1B22;
                border-radius: 12px;
            }
            QFrame#about_frame {
                background-color: #2A2A33;
                border-radius: 8px;
                padding: 5px;
                border: 1px solid #33333C;
            }
            QLabel#about_text {
                padding: 10px;
                color: #ACACBE;
                font-size: 11pt;
            }
            QFrame#usage_frame {
                background-color: #2A2A33;
                border-radius: 8px;
                padding: 0px;
                border: 1px solid #33333C;
                margin-top: 0px;
            }
            QLabel#usage_text {
                padding: 10px;
                color: #ACACBE;
                font-size: 11pt;
            }
            QFrame#separator {
                background-color: #33333C;
                height: 1px;
                margin: 0px 10px;
            }
            QFrame#settings_area {
                background-color: #2A2A33;
                border: 1px solid #33333C;
                border-radius: 8px;
                padding: 5px;
            }
            /* 操作区样式 */
            QLabel[text="操作区"] {
                font-size: 14pt;
                font-weight: bold;
                color: #FFFFFF;
                background-color: transparent;
            }
            QFrame#operation_container {
                background-color: transparent;
            }
            QLabel#desc_text {
                color: #ACACBE;
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
            /* 滚动条样式 */
            QScrollBar:vertical {
                border: none;
                background: #27272F;
                width: 8px;
                margin: 0px 0px 0px 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #42424F;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #4D4D5C;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #27272F;
                height: 8px;
                margin: 0px 0px 0px 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: #42424F;
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #4D4D5C;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
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
        title_label.setMinimumHeight(80)  # 减小标题高度
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
        
        sidebar_layout.addWidget(self.scene_btn)
        sidebar_layout.addWidget(self.segment_btn)
        sidebar_layout.addWidget(self.detection_btn)
        
        # 添加分隔线
        separator4 = QFrame()
        separator4.setFrameShape(QFrame.HLine)
        separator4.setFrameShadow(QFrame.Sunken)
        separator4.setObjectName("separator")
        sidebar_layout.addWidget(separator4)
        
        # 样本制作按钮
        self.sample_making_btn = self.create_menu_button("批量影像解译")
        sidebar_layout.addWidget(self.sample_making_btn)
        
        # 添加分隔线
        separator5 = QFrame()
        separator5.setFrameShape(QFrame.HLine)
        separator5.setFrameShadow(QFrame.Sunken)
        separator5.setObjectName("separator")
        sidebar_layout.addWidget(separator5)
        
        # 添加弹性空间
        sidebar_layout.addStretch()
        
        # 添加帮助按钮
        self.help_btn = self.create_menu_button("帮助")
        self.help_btn.clicked.connect(lambda: self.select_button(self.help_btn, 8))
        sidebar_layout.addWidget(self.help_btn)
        
        # 添加操作按钮 (设置按钮)
        self.settings_btn = self.create_menu_button("设置")
        self.settings_btn.clicked.connect(lambda: self.select_button(self.settings_btn, 9))
        sidebar_layout.addWidget(self.settings_btn)
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
        self.sample_making_page = self.create_sample_making_page()
        self.help_page = self.create_help_page()
        self.setting_page = self.create_setting_page()
        
        # 将页面添加到堆叠部件
        self.content_stack.addWidget(self.home_page)
        self.content_stack.addWidget(self.data_page)
        self.content_stack.addWidget(self.preprocess_page)
        self.content_stack.addWidget(self.fishnet_page)
        self.content_stack.addWidget(self.scene_page)
        self.content_stack.addWidget(self.segment_page)
        self.content_stack.addWidget(self.detection_page)
        self.content_stack.addWidget(self.sample_making_page)
        self.content_stack.addWidget(self.help_page)
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
        self.sample_making_btn.clicked.connect(lambda: self.select_button(self.sample_making_btn, 7))
        
        # 设置默认选中按钮
        self.home_btn.setChecked(True)
        self.content_stack.setCurrentIndex(0)
    
    def create_menu_button(self, text):
        """创建侧边栏菜单按钮"""
        button = QPushButton(text)
        button.setCheckable(True)
        button.setMinimumHeight(40)
        button.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        
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
                   self.scene_btn, self.segment_btn, self.detection_btn, self.sample_making_btn,
                   self.help_btn, self.settings_btn]:
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
        layout.setContentsMargins(10, 10, 10, 10)  # 减少边距，让内容占据更多空间
        layout.setSpacing(5)  # 减少垂直间距
        
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
        content_layout.setSpacing(0)  # 完全移除内部元素间的间距
        content_layout.setContentsMargins(10, 5, 10, 5)  # 减少内边距
        
        # 系统功能介绍区域
        intro_container = QFrame()
        intro_container.setStyleSheet("background-color: transparent;")  # 设置为透明背景，继承父容器颜色
        intro_container.setFixedHeight(80)  # 设置固定高度，控制区域大小
        intro_layout = QVBoxLayout(intro_container)
        intro_layout.setContentsMargins(0, 0, 0, 0)
        intro_layout.setSpacing(2)
        
        section_title = QLabel("系统功能介绍")
        section_title.setObjectName("section_title")
        intro_layout.addWidget(section_title)
        
        desc = SelectableLabel("本系统提供遥感影像智能解译功能，包含数据获取、预处理、渔网分割、场景分类、语义分割、目标检测和批量化解译等多种功能模块。")
        desc.setWordWrap(True)
        desc.setObjectName("desc_text")
        desc.setContentsMargins(0, 0, 0, 0)  # 移除文本内边距
        intro_layout.addWidget(desc)
        
        content_layout.addWidget(intro_container, 0)  # 设置伸缩因子为0，防止自动扩展
        
        # 使用说明区域
        section_title2 = QLabel("使用说明")
        section_title2.setObjectName("section_title")
        section_title2.setContentsMargins(0, 5, 0, 0)  # 只保留上边距，与上面元素稍微分开
        content_layout.addWidget(section_title2)
        
        usage_frame = QFrame()
        usage_frame.setObjectName("usage_frame")
        usage_layout = QVBoxLayout(usage_frame)
        usage_layout.setContentsMargins(0, 0, 0, 0)  # 完全移除内边距
        usage_layout.setSpacing(0)  # 移除内部间距
        
        usage_text = """1. 如何导入遥感影像数据
   选择"数据获取"模块，点击"本地导入"按钮，选择遥感影像文件。

2. 如何进行数据预处理
   选择"数据处理"模块，导入影像后，选择预处理参数，点击"开始预处理"。

3. 如何使用渔网分割功能
   选择"渔网分割"模块，导入影像，设置网格参数，点击"开始分割"。

4. 如何进行场景分类
   选择"场景分类"模块，导入影像，点击"开始场景分类"。

5. 如何进行语义分割
   选择"语义分割"模块，导入影像，点击"开始语义分割"。

6. 如何进行目标检测
   选择"目标检测"模块，导入影像，点击"开始目标检测"。

7. 如何进行批量化解译
   选择"批量解译"模块，导入影像数据集，点击"开始批量解译"。"""
        
        usage = SelectableLabel(usage_text)
        usage.setWordWrap(True)
        usage.setObjectName("usage_text")
        usage.setContentsMargins(0, 0, 0, 0)  # 移除文本内边距
        usage_layout.addWidget(usage)
        
        content_layout.addWidget(usage_frame, 1)  # 让usage_frame占据所有可用空间
        
        layout.addWidget(content_frame, 1)  # 让content_frame占据布局中的所有可用空间
        
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
        import_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始场景分类")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        process_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出分类结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        export_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
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
        import_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始语义分割")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        process_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出分割结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        export_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
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
        import_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始目标检测")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        process_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出检测结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        export_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
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
        self.theme_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        self.theme_btn.clicked.connect(self.toggle_theme)
        button_layout.addWidget(self.theme_btn)
        
        auth_btn = QPushButton("账户与授权")
        auth_btn.setObjectName("operation_btn")
        auth_btn.setFixedWidth(180)
        auth_btn.setFixedHeight(40)
        auth_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
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
        import_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(import_btn)
        
        download_btn = QPushButton("在线下载")
        download_btn.setObjectName("operation_btn")
        download_btn.setFixedWidth(180)
        download_btn.setFixedHeight(40)
        download_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(download_btn)
        
        manage_btn = QPushButton("数据管理")
        manage_btn.setObjectName("operation_btn")
        manage_btn.setFixedWidth(180)
        manage_btn.setFixedHeight(40)
        manage_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
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
        import_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始预处理")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        process_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出处理结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        export_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
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
        import_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(import_btn)
        
        grid_btn = QPushButton("设置网格参数")
        grid_btn.setObjectName("operation_btn")
        grid_btn.setFixedWidth(180)
        grid_btn.setFixedHeight(40)
        grid_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(grid_btn)
        
        process_btn = QPushButton("开始分割")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        process_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出分割结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        export_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page
    
    def create_sample_making_page(self):
        """创建样本制作页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("样本制作")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("进行小批量样本制作，便于您的后续实验")
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
        
        import_btn = QPushButton("导入遥感影像数据集")
        import_btn.setObjectName("operation_btn")
        import_btn.setFixedWidth(180)
        import_btn.setFixedHeight(40)
        import_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(import_btn)
        
        process_btn = QPushButton("开始批量影像解译")
        process_btn.setObjectName("operation_btn")
        process_btn.setFixedWidth(180)
        process_btn.setFixedHeight(40)
        process_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("导出解译结果")
        export_btn.setObjectName("operation_btn")
        export_btn.setFixedWidth(180)
        export_btn.setFixedHeight(40)
        export_btn.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标悬停时为手型指针
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()  # 添加弹性空间
        content_layout.addWidget(button_container)
        
        layout.addWidget(content_frame)
        layout.addStretch()
        
        return page
    
    def create_help_page(self):
        """创建帮助页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(10, 10, 10, 10)  # 减少边距，让内容占据更多空间
        
        title = QLabel("帮助中心")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        subtitle = QLabel("系统功能图解")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # 允许滚动区域内的内容随窗口调整大小
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.NoFrame)  # 去除边框
        
        # 创建滚动区域的内容容器
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)  # 增加图片之间的间距
        
        # 1. 场景分类图片及说明
        section_title1 = QLabel("场景分类功能")
        section_title1.setObjectName("section_title")
        scroll_layout.addWidget(section_title1)
        
        # 添加可点击的场景分类图片
        image_path1 = "D:/VS_WORKBASE/PySide6/遥感影像智能解译系统V1.0/demo_image/scene_classification_process.png"
        img_label1 = self.add_clickable_image(scroll_layout, image_path1, width=700)
        
        # 添加场景分类说明 (使用SelectableLabel使文本可选)
        class_desc_text = "场景分类功能对遥感影像进行整体分类，识别影像所属场景类别。本系统采用深度学习模型进行特征提取和分类，支持多达45种常见地物场景类型的识别，可应用于地理国情监测、城市规划等领域。"
        class_desc = SelectableLabel(class_desc_text)
        class_desc.setWordWrap(True)
        class_desc.setObjectName("desc_text")
        class_desc.setStyleSheet("background-color: transparent;")
        scroll_layout.addWidget(class_desc)
        
        # 添加分隔线
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setFrameShadow(QFrame.Sunken)
        separator1.setObjectName("separator")
        scroll_layout.addWidget(separator1)
        
        # 2. 语义分割图片及说明
        section_title2 = QLabel("语义分割功能")
        section_title2.setObjectName("section_title")
        scroll_layout.addWidget(section_title2)
        
        # 添加可点击的语义分割图片
        image_path2 = "D:/VS_WORKBASE/PySide6/遥感影像智能解译系统V1.0/demo_image/DeepLab_segmentation_process.png"
        img_label2 = self.add_clickable_image(scroll_layout, image_path2, width=700)
        
        # 添加语义分割说明 (使用SelectableLabel使文本可选)
        seg_desc_text = "语义分割功能基于DeepLab模型，对遥感影像进行像素级分类，可识别地物类型并生成分类图。该功能适用于土地覆盖分类、变化检测等应用场景。系统支持多种预训练模型和自定义训练。"
        seg_desc = SelectableLabel(seg_desc_text)
        seg_desc.setWordWrap(True)
        seg_desc.setObjectName("desc_text")
        seg_desc.setStyleSheet("background-color: transparent;")
        scroll_layout.addWidget(seg_desc)
        
        # 添加分隔线
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setObjectName("separator")
        scroll_layout.addWidget(separator2)
        
        # 3. 目标检测图片及说明
        section_title3 = QLabel("目标检测功能")
        section_title3.setObjectName("section_title")
        scroll_layout.addWidget(section_title3)
        
        # 添加可点击的目标检测图片
        image_path3 = "D:/VS_WORKBASE/PySide6/遥感影像智能解译系统V1.0/demo_image/yolo_detection_process.png"
        img_label3 = self.add_clickable_image(scroll_layout, image_path3, width=700)
        
        # 添加目标检测说明 (使用SelectableLabel使文本可选)
        det_desc_text = "目标检测功能基于YOLO系列模型，能够识别并定位遥感影像中的特定目标，如建筑物、车辆、飞机等，并提供位置信息和置信度。系统支持多尺度目标检测和实时推理，适用于军事侦察、灾害评估等应用场景。"
        det_desc = SelectableLabel(det_desc_text)
        det_desc.setWordWrap(True)
        det_desc.setObjectName("desc_text")
        det_desc.setStyleSheet("background-color: transparent;")
        scroll_layout.addWidget(det_desc)
        
        # 添加一些底部间距
        scroll_layout.addStretch()
        
        # 设置滚动区域内容
        scroll_area.setWidget(scroll_content)
        
        # 将滚动区域添加到主布局
        layout.addWidget(scroll_area, 1)  # 让scroll_area占据布局中的所有可用空间
        
        # 联系与支持 - 浅灰色小字体放在底部，可选中的文本
        contact_text = "技术支持邮箱: support@rsiis.com | 官方网站: www.rsiis.com | 文档中心: docs.rsiis.com"
        contact_label = SelectableLabel(contact_text)
        contact_label.setAlignment(Qt.AlignCenter)
        contact_label.setStyleSheet("color: #999999; font-size: 9pt; background-color: transparent; border: none;")
        contact_label.setMaximumHeight(30)  # 限制高度
        layout.addWidget(contact_label)
        
        return page
    
    def add_clickable_image(self, layout, image_path, width=None, height=None):
        """
        添加可点击图片，点击后可在系统默认图片查看器中打开
        :param layout: 要添加图片的布局
        :param image_path: 图片路径
        :param width: 图片宽度（可选）
        :param height: 图片高度（可选）
        :return: 添加的图片标签
        """
        # 创建图片标签
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        
        # 如果指定了尺寸，则调整图片大小
        if width and height:
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        elif width:
            pixmap = pixmap.scaledToWidth(width, Qt.SmoothTransformation)
        elif height:
            pixmap = pixmap.scaledToHeight(height, Qt.SmoothTransformation)
        
        # 设置图片
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        
        # 使图片可点击
        image_label.setCursor(QCursor(Qt.PointingHandCursor))  # 设置鼠标形状为手型
        image_label.setToolTip("点击查看原始图片")
        
        # 存储图片路径
        image_label.setProperty("image_path", image_path)
        
        # 添加点击事件
        def open_image(event):
            path = image_label.property("image_path")
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        
        # 设置鼠标点击事件
        image_label.mousePressEvent = open_image
        
        # 添加到布局
        layout.addWidget(image_label)
        
        return image_label
        
    # 使用示例：如何在首页中添加图片
    def create_home_page_with_image(self):
        """创建带有图片的首页示例"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("遥感影像智能解译系统")
        title.setObjectName("page_title")
        layout.addWidget(title)
        
        # 添加一个图片（假设有一个图片文件位于 ./images/logo.png）
        # self.add_image_to_widget(layout, "./images/logo.png", width=300)
        
        content_frame = QFrame()
        content_frame.setObjectName("content_frame")
        content_layout = QVBoxLayout(content_frame)
        
        # 在内容框架中也可以添加图片
        # self.add_image_to_widget(content_layout, "./images/sample_image.jpg", width=500)
        
        section_title = QLabel("系统功能介绍")
        section_title.setObjectName("section_title")
        content_layout.addWidget(section_title)
        
        desc = QLabel("本系统提供遥感影像智能解译功能，包含数据获取、数据处理、渔网分割、批量影像解译等功能。")
        desc.setWordWrap(True)
        desc.setObjectName("desc_text")
        content_layout.addWidget(desc)
        
        layout.addWidget(content_frame, 1)
        
        return page 