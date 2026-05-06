import re
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QSplitter)
from PyQt6.QtGui import (QSyntaxHighlighter, QTextCharFormat, QColor, QFont, 
                         QIcon, QPainter)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.editor import CodeEditor

class CSSHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Selector format
        selector_format = QTextCharFormat()
        selector_format.setForeground(QColor("#d7ba7d"))
        selector_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((re.compile(r"^[A-Za-z0-9_#\.*:]+\s*\{"), selector_format))
        self.highlighting_rules.append((re.compile(r"\s*[A-Za-z0-9_#\.*:]+\s*\{"), selector_format))

        # Property format
        property_format = QTextCharFormat()
        property_format.setForeground(QColor("#9cdcfe"))
        self.highlighting_rules.append((re.compile(r"\b[a-z-]+\b(?=\s*:)"), property_format))

        # Value format
        value_format = QTextCharFormat()
        value_format.setForeground(QColor("#ce9178"))
        self.highlighting_rules.append((re.compile(r"(?<=:)\s*[^;{}]+"), value_format))

        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6a9955"))
        self.highlighting_rules.append((re.compile(r"/\*.*?\*/"), comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), format)

class SuperUIEditor(CodeEditor):
    def __init__(self):
        # Pass CSSHighlighter to the base class
        super().__init__(highlighter_class=CSSHighlighter)

class SuperUIDialog(QDialog):
    style_applied = pyqtSignal(str)

    def __init__(self, current_style, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SuperUI(TM) - Advanced UI Customization")
        self.resize(800, 600)
        
        self.setup_ui(current_style)

    def setup_ui(self, current_style):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #252526; border-bottom: 1px solid #333333;")
        header_layout = QHBoxLayout(header)
        
        title_label = QLabel("SuperUI™ Customizer")
        title_label.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: bold; padding-left: 10px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        apply_btn = QPushButton("Apply Changes")
        apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        apply_btn.clicked.connect(self.apply_style)
        header_layout.addWidget(apply_btn)
        
        layout.addWidget(header)

        # Editor
        self.editor = SuperUIEditor()
        self.editor.setPlainText(current_style)
        layout.addWidget(self.editor)

        # Footer / Info
        footer = QFrame()
        footer.setFixedHeight(30)
        footer.setStyleSheet("background-color: #007acc;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(10, 0, 10, 0)
        
        info_label = QLabel("Edit the QSS (Qt Style Sheets) above to customize your workspace in real-time.")
        info_label.setStyleSheet("color: #ffffff; font-size: 11px;")
        footer_layout.addWidget(info_label)
        
        layout.addWidget(footer)

    def apply_style(self):
        new_style = self.editor.toPlainText()
        self.style_applied.emit(new_style)
