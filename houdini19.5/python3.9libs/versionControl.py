import os
import re

from PySide2 import QtCore, QtGui, QtWidgets
import incrementSave

class VersionControlUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(VersionControlUI, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName('VersionControlUI')
        self.setWindowTitle('Version Control')
        self.resize(500, 500)
        
        self.path = self.get_file_path()
        
        self.dirmodel = QtWidgets.QFileSystemModel()
        self.dirmodel.setRootPath(QtCore.QDir.rootPath())
        self.dirmodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files)
        self.filter = self.get_filter()
        self.dirmodel.setNameFilters([self.filter])
        self.dirmodel.setNameFilterDisables(False)

        self.view = QtWidgets.QTreeView(parent=self)
        self.view.setModel(self.dirmodel)
        self.view.hideColumn(1)
        self.view.hideColumn(2)
        self.view.setRootIndex(self.dirmodel.index(self.path))
        self.font = QtGui.QFont()
        self.font.setPointSize(10)
        self.view.setFont(self.font)
        self.view.header().resizeSection(0, 325)
        
        button_layout = QtWidgets.QHBoxLayout()
        self.open_button = QtWidgets.QPushButton('Open File', self)
        self.open_button.adjustSize()
        self.open_button.clicked.connect()
        self.explorer_button = QtWidgets.QPushButton('Open File Explorer', self)
        self.explorer_button.clicked.connect(self.open_explorer)
        self.save_button = QtWidgets.QPushButton('Save New Version', self)
        self.save_button.clicked.connect(self.save_version)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.explorer_button)
        button_layout.addWidget(self.open_button)

        outer_layout = QtWidgets.QVBoxLayout()
        outer_layout.addWidget(self.view)
        outer_layout.addLayout(button_layout)
        outer_layout.setSpacing(15)
        self.setLayout(outer_layout)

    def get_file_path(self):
        current_path = hou.hipFile.path()
        dir_path = os.path.split(current_path)[0]
        return dir_path
    
    def get_filter(self):
        str_match = r"_v[0-9]"
        current_path = hou.hipFile.path()
        file = os.path.splitext(os.path.basename(current_path))[0]
        filename = re.split(f"{str_match}+", file, flags=re.I)
        filter = fr"*{filename[0]}_[vV]*"
        return filter
    
    def open_explorer(self):
        hou.ui.selectFile()

    # def open_file(self, file):
    #     hou.hipFile.load(file)

    def save_version(self):
        incrementSave.main()

main = VersionControlUI()
main.show()
