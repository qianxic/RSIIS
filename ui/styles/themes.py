"""
主题样式模块
存储系统的亮色主题和暗色主题样式表
"""

# 亮色主题样式表
LIGHT_STYLE = """
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
DARK_STYLE = """
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