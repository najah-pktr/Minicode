from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QUrl, Qt

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False

class PreviewWindow(QMainWindow):
    def __init__(self, parent=None):
        """Initialize the preview window."""
        super().__init__(parent)
        self.setWindowTitle("Web Preview")
        self.resize(1024, 768)
        
        if WEBENGINE_AVAILABLE:
            self.browser = QWebEngineView()
            self.setCentralWidget(self.browser)
        else:
            self.label = QLabel("Preview not available.\nPlease install PyQt6-WebEngine.")
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setCentralWidget(self.label)

    def load_file(self, file_path):
        """Load a local file into the previewer."""
        if WEBENGINE_AVAILABLE:
            self.browser.setUrl(QUrl.fromLocalFile(file_path))

    def load_url(self, url):
        """Load a URL into the previewer."""
        if WEBENGINE_AVAILABLE:
            self.browser.setUrl(QUrl(url))

