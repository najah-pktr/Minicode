import os
from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QWidget
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir

class FileExplorer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.getcwd()))
        
        # Hide unnecessary columns
        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)
        
        self.tree.setHeaderHidden(True)
        self.layout.addWidget(self.tree)

    def set_root(self, path):
        self.tree.setRootIndex(self.model.index(path))
