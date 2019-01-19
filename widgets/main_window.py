import sys

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets

from .main_widget import main_widget


class main_window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.parent = parent

    def build(self):
        """Build widget"""
        self.setWindowTitle("PipQt")
        self.setWindowIcon(QtGui.QIcon("icons/main_icon.png"))

        self.main_widget = main_widget(self)
        self.main_widget.build()

        self.setCentralWidget(self.main_widget)

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("File")

        menu_action = QtWidgets.QAction("Exit", self)
        menu_action.triggered.connect(self.parent.quit)
        file_menu.addAction(menu_action)

        edit_menu = main_menu.addMenu("Edit")

        menu_action = QtWidgets.QAction("Add Packages", self)
        menu_action.triggered.connect(self.main_widget.install)
        edit_menu.addAction(menu_action)

        menu_action = QtWidgets.QAction("Uninstall Selected Packages", self)
        menu_action.triggered.connect(self.main_widget.uninstall)
        edit_menu.addAction(menu_action)

        edit_menu.addSeparator()

        menu_action = QtWidgets.QAction("Update Selected Packages", self)
        menu_action.triggered.connect(self.main_widget.update)
        edit_menu.addAction(menu_action)

        menu_action = QtWidgets.QAction("Update All Packages", self)
        menu_action.triggered.connect(self.main_widget.update_all)
        edit_menu.addAction(menu_action)

        edit_menu.addSeparator()

        menu_action = QtWidgets.QAction("Refresh Packages", self)
        menu_action.triggered.connect(self.main_widget.refresh)
        edit_menu.addAction(menu_action)

        menu_action = QtWidgets.QAction("Package Info", self)
        menu_action.triggered.connect(self.main_widget.info)
        edit_menu.addAction(menu_action)

        self.show()
        self.resize(self.width(), 500)
