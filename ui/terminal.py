import sys
import os
import subprocess
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit
from PyQt6.QtCore import QProcess, Qt

class TerminalWindow(QMainWindow):
    def __init__(self, parent=None, cwd=None):
        """Initialize the terminal window."""
        super().__init__(parent)
        self.setWindowTitle("MiniCode Terminal")
        self.resize(800, 400)
        self.cwd = cwd or os.getcwd()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        
        self.display = QPlainTextEdit()
        self.display.setReadOnly(True)
        self.display.setStyleSheet("background-color: #000000; color: #ffffff; font-family: 'Consolas'; font-size: 12px;")
        self.layout.addWidget(self.display)
        
        self.input_line = QPlainTextEdit()
        self.input_line.setFixedHeight(35)
        self.input_line.setPlaceholderText("Enter command here...")
        self.input_line.setToolTip("Type a command and press Enter to execute")
        self.input_line.setStyleSheet("background-color: #000000; color: #ffffff; font-family: 'Consolas'; border: 1px solid #333; border-radius: 4px;")
        self.layout.addWidget(self.input_line)
        
        self.input_line.installEventFilter(self)
        
        # Start the shell
        shell = "cmd.exe" if sys.platform == "win32" else "bash"
        if self.cwd:
            self.process.setWorkingDirectory(self.cwd)
        self.process.start(shell)

    def handle_stdout(self):
        """Handle standard output from the process."""
        data = self.process.readAllStandardOutput().data().decode(errors='replace')
        self.display.appendPlainText(data)
        self.scroll_to_bottom()

    def handle_stderr(self):
        """Handle standard error from the process."""
        data = self.process.readAllStandardError().data().decode(errors='replace')
        self.display.appendPlainText(data)
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """Scroll the terminal display to the bottom."""
        cursor = self.display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.display.setTextCursor(cursor)

    def eventFilter(self, obj, event):
        """Filter events to handle the Enter key in the input line."""
        if obj == self.input_line and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return:
                command = self.input_line.toPlainText().strip()
                if command.lower() == "clear":
                    self.display.clear()
                else:
                    self.process.write((command + "\n").encode())
                self.input_line.clear()
                return True
        return super().eventFilter(obj, event)

