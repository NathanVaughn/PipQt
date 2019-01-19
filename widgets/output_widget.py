import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets

import lib.functions


class output_widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent

    def build(self):
        """Build widget"""
        self.setWindowTitle("Output")
        self.setWindowIcon(QtGui.QIcon("icons/main_icon.png"))
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        self.layout = QtWidgets.QGridLayout()

        self.output = QtWidgets.QTextBrowser()
        self.output.setTextColor(QtGui.QColor(0, 255, 0))
        self.output.setStyleSheet("background-color: black;")

        self.layout.addWidget(self.output)

        self.setLayout(self.layout)

        self.show()
        self.raise_()
        lib.functions.center_widget(self.parent.parent, self)

    def data_ready(self, data):
        """Process incoming data"""
        self.output.append(data)
        QtWidgets.QApplication.processEvents()
