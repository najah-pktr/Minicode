import sys
import os
import json
import hashlib
import urllib.request
import re
import ssl
import threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSplitter, QTabWidget, 
                             QVBoxLayout, QWidget, QFileDialog, QMessageBox, 
                             QToolBar, QStatusBar, QStyle, QInputDialog, QDockWidget)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal

from ui.styles import DARK_STYLE
from ui.editor import CodeEditor
from ui.explorer import FileExplorer
from ui.terminal import TerminalWindow
from ui.preview import PreviewWindow
from ui.super_ui import SuperUIDialog

class MiniCode(QMainWindow):
    style_processed = pyqtSignal(str)

    def __init__(self):
        """Initialize the MiniCode IDE."""
        super().__init__()
        self.setWindowTitle("MiniCode IDE")
        self.resize(1200, 800)
        self.current_style = DARK_STYLE
        self.setStyleSheet(self.current_style)

        self.setup_ui()
        self.setup_menus()
        self.setup_toolbar()
        self.setup_statusbar()
        
        self.style_processed.connect(self._finish_apply_style)
        
        self.load_session()

    def get_config_path(self, filename):
        """Get the absolute path for a configuration file, ensuring portability."""
        base_dir = os.path.join(os.path.expanduser("~"), ".minicode")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        return os.path.join(base_dir, filename)

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def setup_ui(self):
        """Set up the modular user interface using DockWidgets."""
        # Main Tab Widget for Editors
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Dockable File Explorer
        self.explorer_dock = QDockWidget("Explorer", self)
        self.explorer_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.explorer = FileExplorer()
        self.explorer.tree.doubleClicked.connect(self.on_file_double_clicked)
        self.explorer_dock.setWidget(self.explorer)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.explorer_dock)

        # Dockable Terminal
        self.terminal_dock = QDockWidget("Terminal", self)
        self.terminal_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea | Qt.DockWidgetArea.TopDockWidgetArea)
        self.terminal_window = TerminalWindow(self)
        self.terminal_dock.setWidget(self.terminal_window)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal_dock)
        self.terminal_dock.hide() # Hidden by default

        # Dockable Preview
        self.preview_dock = QDockWidget("Web Preview", self)
        self.preview_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)
        self.preview_window = PreviewWindow(self)
        self.preview_dock.setWidget(self.preview_window)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.preview_dock)
        self.preview_dock.hide() # Hidden by default

        self.setup_dock_menu()

    def setup_dock_menu(self):
        """Add a menu to toggle dock visibility."""
        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction(self.explorer_dock.toggleViewAction())
        view_menu.addAction(self.terminal_dock.toggleViewAction())
        view_menu.addAction(self.preview_dock.toggleViewAction())
        return view_menu

    def setup_menus(self):
        """Configure the menu bar and its actions."""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New File", self)
        new_action.setShortcut("Ctrl+N")
        new_action.setToolTip("Create a new code file")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open File", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setToolTip("Open an existing file from disk")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.setToolTip("Open a directory in the file explorer")
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setToolTip("Save the current file")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.setToolTip("Save the current file with a new name")
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View Menu (Updated in setup_ui via setup_dock_menu)
        pass

        # Run Menu
        run_menu = menubar.addMenu("Run")
        run_action = QAction("Run Python", self)
        run_action.setShortcut("F5")
        run_action.setToolTip("Run the current file with the Python interpreter")
        run_action.triggered.connect(self.run_python)
        run_menu.addAction(run_action)

        help_menu = menubar.addMenu("Help")
        
        super_ui_action = QAction("SuperUI™", self)
        super_ui_action.setToolTip("Customize the IDE interface with CSS")
        super_ui_action.triggered.connect(self.open_super_ui)
        help_menu.addAction(super_ui_action)

        help_menu.addSeparator()
        
        about_action = QAction("About MiniCode", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_toolbar(self):
        """Initialize the minimalist toolbar with icons only."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(22, 22))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        toolbar.setMovable(False) # Remove dotted drag handle
        toolbar.setFloatable(False)
        self.addToolBar(toolbar)
        
        # New File
        new_btn = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon), "New", self)
        new_btn.setObjectName("actionNew")
        new_btn.setToolTip("New File (Ctrl+N)")
        new_btn.triggered.connect(self.new_file)
        toolbar.addAction(new_btn)
        
        # Save
        save_btn = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), "Save", self)
        save_btn.setObjectName("actionSave")
        save_btn.setToolTip("Save (Ctrl+S)")
        save_btn.triggered.connect(self.save_file)
        toolbar.addAction(save_btn)
        
        # Open Folder
        open_folder_btn = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon), "Folder", self)
        open_folder_btn.setObjectName("actionFolder")
        open_folder_btn.setToolTip("Open Folder")
        open_folder_btn.triggered.connect(self.open_folder)
        toolbar.addAction(open_folder_btn)
        
        toolbar.addSeparator()

        # Terminal
        terminal_btn = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon), "Terminal", self)
        terminal_btn.setObjectName("actionTerminal")
        terminal_btn.setToolTip("Toggle Terminal")
        terminal_btn.triggered.connect(self.toggle_terminal)
        toolbar.addAction(terminal_btn)
        
        # Preview
        preview_btn = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload), "Preview", self)
        preview_btn.setObjectName("actionPreview")
        preview_btn.setToolTip("Toggle Preview")
        preview_btn.triggered.connect(self.toggle_preview)
        toolbar.addAction(preview_btn)

        # Run
        run_btn = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay), "Run", self)
        run_btn.setObjectName("actionRun")
        run_btn.setToolTip("Run Code (F5)")
        run_btn.triggered.connect(self.run_python)
        toolbar.addAction(run_btn)

        # Map action names to toolbar buttons for CSS targeting
        for action in toolbar.actions():
            button = toolbar.widgetForAction(action)
            if button:
                button.setObjectName(action.objectName())

    def setup_statusbar(self):
        """Initialize the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def update_status(self):
        """Update the status bar with cursor position."""
        editor = self.tabs.currentWidget()
        if editor:
            cursor = editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            self.status_bar.showMessage(f"Line: {line}, Col: {col}")

    def new_file(self):
        """Create a new file, prompt for a name, and save it to disk immediately."""
        file_name, ok = QInputDialog.getText(self, "New File", "Enter file name (e.g., script.py):", text="Untitled.py")
        if ok and file_name:
            # Determine where to save the file
            # If a folder is open in explorer, use that. Otherwise, use current directory.
            root_index = self.explorer.tree.rootIndex()
            if root_index.isValid():
                base_dir = self.explorer.model.filePath(root_index)
            else:
                base_dir = os.getcwd()
            
            file_path = os.path.join(base_dir, file_name)
            
            # Check if file already exists
            if os.path.exists(file_path):
                QMessageBox.warning(self, "New File", f"File '{file_name}' already exists.")
                return

            try:
                # Create the file on disk
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("") # Empty file
                
                # Open it in the editor
                self.open_file(file_path)
                self.status_bar.showMessage(f"Created and opened: {file_name}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create file: {str(e)}")

    def open_file(self, file_path=None):
        """Open a file and load its content into a new tab."""
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open File")
        
        if file_path:
            try:
                # Try UTF-8 first, fallback to latin-1 if it fails (common for some binary/legacy files)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                
                editor = CodeEditor()
                editor.setPlainText(content)
                editor.setProperty("file_path", file_path)
                editor.cursorPositionChanged.connect(self.update_status)
                editor.textChanged.connect(self.update_live_preview)
                
                self.tabs.addTab(editor, os.path.basename(file_path))
                self.tabs.setCurrentWidget(editor)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

    def open_folder(self):
        """Open a directory and update the file explorer."""
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder")
        if folder_path:
            self.explorer.set_root(folder_path)
            os.chdir(folder_path)

    def run_python(self):
        """Run the current Python file in the integrated terminal."""
        current_tab = self.tabs.currentWidget()
        if not current_tab:
            return
            
        file_path = current_tab.property("file_path")
        if not file_path:
            QMessageBox.warning(self, "Run", "Please save the file first.")
            return

        self.terminal_dock.show()
        # Handle path with spaces
        self.terminal_window.process.write(f'python "{file_path}"\n'.encode())

    def save_file(self):
        """Save the current tab's content."""
        current_tab = self.tabs.currentWidget()
        if not current_tab:
            return
            
        file_path = current_tab.property("file_path")
        if not file_path:
            return self.save_file_as()
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(current_tab.toPlainText())
            self.status_bar.showMessage(f"Saved {file_path}", 2000)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Could not save file: {str(e)}")

    def save_file_as(self):
        """Save the current tab's content with a new name."""
        current_tab = self.tabs.currentWidget()
        if not current_tab:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(current_tab.toPlainText())
                
                current_tab.setProperty("file_path", file_path)
                self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(file_path))
                self.status_bar.showMessage(f"Saved as {file_path}", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Could not save file: {str(e)}")

    def close_tab(self, index):
        """Close the tab at the specified index."""
        self.tabs.removeTab(index)

    def on_file_double_clicked(self, index):
        """Handle double-click events in the file explorer."""
        file_path = self.explorer.model.filePath(index)
        if os.path.isfile(file_path):
            self.open_file(file_path)

    def save_session(self):
        """Save the current session (open files) to a JSON file."""
        session = []
        for i in range(self.tabs.count()):
            editor = self.tabs.widget(i)
            path = editor.property("file_path")
            if path:
                session.append(path)
        
        try:
            with open(self.get_config_path("session.json"), "w") as f:
                json.dump(session, f)
        except:
            pass

    def load_session(self):
        """Load the previous session if it exists."""
        session_path = self.get_config_path("session.json")
        if os.path.exists(session_path):
            try:
                with open(session_path, "r") as f:
                    session = json.load(f)
                for path in session:
                    if os.path.exists(path):
                        self.open_file(path)
            except:
                pass

    def closeEvent(self, event):
        """Handle the application close event."""
        self.save_session()
        event.accept()

    def toggle_terminal(self):
        """Toggle the visibility of the terminal dock."""
        if self.terminal_dock.isVisible():
            self.terminal_dock.hide()
        else:
            self.terminal_dock.show()

    def toggle_preview(self):
        """Toggle the visibility of the web preview dock."""
        current_tab = self.tabs.currentWidget()
        if not current_tab:
            return
            
        self.preview_window.set_html(current_tab.toPlainText())
        self.preview_dock.show()

    def update_live_preview(self):
        """Update the live preview if the dock is visible."""
        if self.preview_dock.isVisible():
            current_tab = self.tabs.currentWidget()
            if current_tab:
                self.preview_window.set_html(current_tab.toPlainText())

    def show_about(self):
        """Show the expanded About dialog with more information."""
        about_text = (
            "<b>MiniCode IDE</b><br><br>"
            "<i>A Lightweight, Portable, and Powerful Python IDE</i><br><br>"
            "<b>Version:</b> 1.1.0<br>"
            "<b>Developer:</b> Antigravity AI<br><br>"
            "<b>Key Features:</b><br>"
            "• Advanced Syntax Highlighting<br>"
            "• Integrated Python Terminal<br>"
            "• Real-time Web Preview<br>"
            "• Session Persistence<br>"
            "• Modern Dark Aesthetics<br>"
            "• Auto-save on Creation<br>"
            "• <b>SuperUI™ Customization</b><br><br>"
            "Built with Python and PyQt6 for maximum performance and flexibility."
        )
        QMessageBox.about(self, "About MiniCode", about_text)

    def open_super_ui(self):
        """Open the SuperUI customization dialog."""
        dialog = SuperUIDialog(self.current_style, self)
        dialog.style_applied.connect(self.apply_custom_style)
        dialog.exec()

    def apply_custom_style(self, style):
        """Apply the custom style to the application."""
        self.current_style = style
        self.status_bar.showMessage("Downloading theme assets...", 5000)
        
        def apply_task():
            processed_style = self.process_style_urls(style)
            self.style_processed.emit(processed_style)
            
        threading.Thread(target=apply_task, daemon=True).start()

    def _finish_apply_style(self, processed_style):
        self.setStyleSheet(processed_style)
        
        # Force refresh of all widgets to apply new properties (like icons)
        for widget in self.findChildren(QWidget):
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()
            
        self.status_bar.showMessage("SuperUI™ Style Applied!", 3000)

    def process_style_urls(self, style):
        """Find and download web URLs in the style sheet."""
        cache_dir = self.get_config_path("cache")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            
        # Create an unverified SSL context to avoid certificate errors
        ssl_context = ssl._create_unverified_context()
            
        def download_url(match):
            url_content = match.group(1).strip("'\"")
            if url_content.startswith("http"):
                # Clean up URL to get extension
                base_url = url_content.split('?')[0].split('#')[0]
                ext = os.path.splitext(base_url)[1].lower()
                if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']:
                    ext = ".png" # Default
                
                file_hash = hashlib.md5(url_content.encode()).hexdigest()
                local_path = os.path.join(cache_dir, f"{file_hash}{ext}").replace("\\", "/")
                
                if not os.path.exists(local_path):
                    try:
                        # Use a proper User-Agent to avoid being blocked
                        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
                        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')]
                        
                        with opener.open(url_content, timeout=5) as response:
                            if response.status == 200:
                                with open(local_path, 'wb') as f:
                                    f.write(response.read())
                            else:
                                print(f"Failed to download {url_content}: Status {response.status}")
                                return f"url({url_content})"
                    except Exception as e:
                        print(f"Failed to download {url_content}: {e}")
                        return f"url({url_content})"
                return f"url({local_path})"
            return match.group(0)

        # Regex for url(...)
        return re.sub(r"url\((.*?)\)", download_url, style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiniCode()
    window.show()
    sys.exit(app.exec())
