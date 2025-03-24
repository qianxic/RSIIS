from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Qt

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