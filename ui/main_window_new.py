from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QLabel, QFrame, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPalette, QCursor

# 导入样式表
from ui.styles.themes import LIGHT_STYLE, DARK_STYLE

# 导入页面组件
from ui.pages.home_page import HomePage
from ui.pages.data_page import DataPage
from ui.pages.fishnet_page import FishnetPage
from ui.pages.scene_page import ScenePage
from ui.pages.segment_page import SegmentPage
from ui.pages.detection_page import DetectionPage
from ui.pages.sample_making_page import SampleMakingPage
from ui.pages.help_page import HelpPage
from ui.pages.setting_page import SettingPage

# 其他页面在实现后也可以导入
# from ui.pages.home_page import HomePage
# from ui.pages.data_page import DataPage
# from ui.pages.scene_page import ScenePage
# ...

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
        
        # 应用主题样式
        self.light_style = LIGHT_STYLE
        self.dark_style = DARK_STYLE
        self.setStyleSheet(self.light_style)
        
        # 设置窗口背景色为白色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#FFFFFF"))
        self.setPalette(palette)
        
        # 创建主界面布局
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        main_layout = QHBoxLayout()
        main_layout.setSpacing(8)  # 增加组件间距
        main_layout.setContentsMargins(8, 8, 8, 8)  # 设置边距
        
        # 创建左侧功能区
        self.create_sidebar(main_layout)
        
        # 创建堆叠部件容器，用于显示不同的内容页面
        self.content_stack = QStackedWidget()
        
        # 创建各个功能区页面 - 使用我们的模块化页面
        self.create_pages()
        
        # 将各部分添加到主布局
        main_layout.addWidget(self.content_stack, 1)  # 内容区占据剩余空间
        
        # 创建中央部件并设置布局
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # 连接按钮信号
        self.connect_signals()
        
        # 连接设置页面主题变更信号
        self.setting_page.theme_changed.connect(self.change_theme)
        
        # 设置默认选中按钮
        self.home_btn.setChecked(True)
        self.content_stack.setCurrentIndex(0)
    
    def create_sidebar(self, main_layout):
        """创建左侧侧边栏"""
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
        self.fishnet_btn = self.create_menu_button("渔网分割")
        
        sidebar_layout.addWidget(self.data_btn)
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
        
        # 批量解译
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
        sidebar_layout.addWidget(self.help_btn)
        
        # 添加操作按钮 (设置按钮)
        self.settings_btn = self.create_menu_button("设置")
        sidebar_layout.addWidget(self.settings_btn)
        sidebar_layout.addSpacing(10)
        
        main_layout.addWidget(self.sidebar)
    
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
    
    def create_pages(self):
        """创建所有页面并添加到堆叠部件中"""
        # 使用模块化的页面组件
        self.home_page = HomePage()
        self.data_page = DataPage()
        self.fishnet_page = FishnetPage()
        self.scene_page = ScenePage()
        self.segment_page = SegmentPage()
        self.detection_page = DetectionPage()
        self.sample_making_page = SampleMakingPage()
        self.help_page = HelpPage()
        self.setting_page = SettingPage()
        
        # 将页面添加到堆叠部件
        self.content_stack.addWidget(self.home_page)
        self.content_stack.addWidget(self.data_page)
        self.content_stack.addWidget(self.fishnet_page)
        self.content_stack.addWidget(self.scene_page)
        self.content_stack.addWidget(self.segment_page)
        self.content_stack.addWidget(self.detection_page)
        self.content_stack.addWidget(self.sample_making_page)
        self.content_stack.addWidget(self.help_page)
        self.content_stack.addWidget(self.setting_page)
    
    def connect_signals(self):
        """连接所有信号槽"""
        self.home_btn.clicked.connect(lambda: self.select_button(self.home_btn, 0))
        self.data_btn.clicked.connect(lambda: self.select_button(self.data_btn, 1))
        self.fishnet_btn.clicked.connect(lambda: self.select_button(self.fishnet_btn, 2))
        self.scene_btn.clicked.connect(lambda: self.select_button(self.scene_btn, 3))
        self.segment_btn.clicked.connect(lambda: self.select_button(self.segment_btn, 4))
        self.detection_btn.clicked.connect(lambda: self.select_button(self.detection_btn, 5))
        self.sample_making_btn.clicked.connect(lambda: self.select_button(self.sample_making_btn, 6))
        self.help_btn.clicked.connect(lambda: self.select_button(self.help_btn, 7))
        self.settings_btn.clicked.connect(lambda: self.select_button(self.settings_btn, 8))
    
    def select_button(self, button, page_index):
        """选择按钮，并切换对应的功能页面"""
        # 重置所有按钮状态
        for btn in [self.home_btn, self.data_btn, self.fishnet_btn,
                   self.scene_btn, self.segment_btn, self.detection_btn, self.sample_making_btn,
                   self.help_btn, self.settings_btn]:
            btn.setChecked(False)
        
        # 设置当前按钮为选中状态（如果不是None）
        if button:
            button.setChecked(True)
        
        # 切换到对应的内容页面
        self.content_stack.setCurrentIndex(page_index)
    
    def change_theme(self, is_dark):
        """切换主题样式"""
        self.is_dark_theme = is_dark
        
        if self.is_dark_theme:
            # 切换到暗色主题
            self.setStyleSheet(self.dark_style)
            # 更新窗口背景
            palette = self.palette()
            palette.setColor(QPalette.Window, QColor("#1B1B22"))
            self.setPalette(palette)
        else:
            # 切换到亮色主题
            self.setStyleSheet(self.light_style)
            # 更新窗口背景
            palette = self.palette()
            palette.setColor(QPalette.Window, QColor("#FFFFFF"))
            self.setPalette(palette) 