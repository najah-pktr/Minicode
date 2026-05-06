DARK_STYLE = """
/* 
    MiniCode IDE - SuperUI™ Customization 
    Edit these QSS (Qt Style Sheets) properties to change the look of your workspace.
    
    NEW: Web Icon Support! 
    You can now use web URLs in url(), e.g.:
    qproperty-icon: url(https://example.com/icon.png);
    background-image: url(https://example.com/bg.jpg);
*/

QMainWindow {
    background-color: #1a1a1a; /* Main window background */
    color: #d4d4d4;            /* Default text color */
}

/* Side Docks (Explorer, Terminal, Preview) */
QDockWidget {
    color: #888888;
    font-weight: bold;
    font-size: 11px;
    border: 1px solid #333333;
}

QDockWidget::title {
    background: #252526;
    padding-top: 6px;
    padding-left: 10px;
    border-bottom: 1px solid #333333;
}

/* Tabs and Editor Pane */
QTabWidget::pane {
    border: none;
    background: #1a1a1a;
}

QTabBar::tab {
    background: #252526;
    color: #858585;
    padding: 10px 20px;
    border-right: 1px solid #1a1a1a;
    font-size: 12px;
}

QTabBar::tab:selected {
    background: #1a1a1a;
    color: #ffffff;
    border-bottom: 2px solid #007acc; /* Selection underline */
}

QTabBar::tab:hover {
    background: #2d2d2d;
    color: #cccccc;
}

/* File Explorer Tree */
QTreeView {
    background-color: #1a1a1a;
    color: #cccccc;
    border: none;
    font-size: 13px;
    outline: none; /* Focus outline */
}

QTreeView::item:hover {
    background-color: #2a2d2e;
}

QTreeView::item:selected {
    background-color: #094771;
    color: #ffffff;
}

/* Code Editor */
QPlainTextEdit {
    background-color: #1a1a1a;
    color: #d4d4d4;
    border: none;
    font-family: 'Consolas', 'Fira Code', 'Courier New', monospace;
    font-size: 14px;
    selection-background-color: #264f78;
}

/* Toolbar */
QToolBar {
    background-color: #2d2d2d;
    border-bottom: 1px solid #333333;
    spacing: 8px;
    padding: 4px;
}

QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 6px;
}

QToolButton:hover {
    background-color: #404040;
    border: 1px solid #505050;
}

QToolButton:pressed {
    background-color: #505050;
}

/* Status Bar */
QStatusBar {
    background-color: #007acc;
    color: #ffffff;
    font-size: 11px;
}

QStatusBar::item {
    border: none;
}

/* Menu Bar */
QMenuBar {
    background-color: #2d2d2d;
    color: #cccccc;
    border-bottom: 1px solid #333333;
}

QMenuBar::item {
    padding: 6px 12px;
}

QMenuBar::item:selected {
    background-color: #404040;
}

QMenu {
    background-color: #252526;
    color: #ffffff;
    border: 1px solid #454545;
    padding: 4px;
}

QMenu::item {
    padding: 6px 24px;
    border-radius: 2px;
}

QMenu::item:selected {
    background-color: #094771;
}

QMenu::separator {
    height: 1px;
    background: #454545;
    margin: 4px 8px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #1a1a1a;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #333333;
    min-height: 20px;
    border-radius: 6px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: #444444;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""


