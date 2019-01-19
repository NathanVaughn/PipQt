import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets

import lib.functions

from .output_widget import output_widget


class HistoryLineEdit(QtWidgets.QLineEdit):
    """This is a version of the standard QLineEdit widget which handles it's
    own history with the up and down arrow keys. If a entry can be submitted
    any other way than returnPressed, the function submission will also need
    to be called on that event"""

    def __init__(self, parent=None):
        QtWidgets.QLineEdit.__init__(self)
        self.parent = parent

        self.returnPressed.connect(self.submission)
        self.history = [""]
        self.history_place = 0

    def keyPressEvent(self, event):
        """Override key press event to handle history"""
        # moving up in history, so to the left in the list
        if event.key() == QtCore.Qt.Key_Up:
            # check if it's currently greater than 0
            if self.history_place > 0:
                self.history_place -= 1

            # set text as relevant item
            self.setText(self.history[self.history_place])
        # down history, so right in the list
        elif event.key() == QtCore.Qt.Key_Down:
            # check if it's currently greater than the length of the history
            if self.history_place < len(self.history) - 1:
                self.history_place += 1

            # set text as relevant item
            self.setText(self.history[self.history_place])

        QtWidgets.QLineEdit.keyPressEvent(self, event)

    def submission(self):
        """Adds new submission to history and resets place"""
        # whenever enter is pressed, add item to history. A blank will always be
        # the last item
        self.history.insert(len(self.history) - 1, self.text())
        # reset current place in history
        self.history_place = len(self.history) - 1


class install_widget(QtWidgets.QWidget):
    def __init__(self, pip_api, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent
        self.pip_api = pip_api

    def build(self):
        """Build widget"""
        self.setWindowTitle("Add Packages")
        self.setWindowIcon(QtGui.QIcon("icons/main_icon.png"))
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.layout = QtWidgets.QVBoxLayout()

        self.package_list = QtWidgets.QListWidget()
        self.package_list.setSortingEnabled(True)
        self.layout.addWidget(self.package_list)

        self.entry = HistoryLineEdit(self)
        self.layout.addWidget(self.entry)

        self.sub_layout = QtWidgets.QHBoxLayout()

        self.add_button = QtWidgets.QPushButton("Add")
        self.sub_layout.addWidget(self.add_button)

        self.remove_button = QtWidgets.QPushButton("Remove")
        self.sub_layout.addWidget(self.remove_button)

        self.layout.addLayout(self.sub_layout)

        self.submit_button = QtWidgets.QPushButton("Submit")
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

        self.add_button.clicked.connect(self.add_package)
        self.remove_button.clicked.connect(self.remove_selected_packages)
        self.submit_button.clicked.connect(self.submit)
        self.entry.textEdited.connect(self.entry_edited)
        self.entry.returnPressed.connect(self.add_package)

        self.show()
        self.raise_()
        self.entry.setFocus()
        lib.functions.center_widget(self.parent, self)

    def add_package(self):
        """Add new package to list"""
        name = self.entry.text()

        if name and name not in self.get_packages():
            item = QtWidgets.QListWidgetItem(name)
            item.setFlags(
                item.flags() | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled
            )

            self.package_list.addItem(item)
            self.entry.clear()

    def remove_selected_packages(self):
        """Removes currently selected packages"""
        for item in self.package_list.selectedItems():
            self.package_list.takeItem(self.package_list.row(item))

    def get_packages(self):
        """Returns list of package names from list widget"""
        packages = []

        for i in range(self.package_list.count()):
            packages.append(self.package_list.item(i).text())

        return packages

    def submit(self):
        """Installs the packages in the list"""
        self.submit_button.setEnabled(False)

        global diag

        diag = output_widget(self)
        diag.build()

        try:
            self.pip_api.install_packages(self.get_packages(), diag.data_ready)
        except (OSError, TimeoutError):
            diag.close()
            self.close()
        else:
            diag.close()
            self.close()
            self.parent.main_widget.refresh()

    def entry_edited(self):
        """Tries to sanitize text on lineedit"""
        self.entry.setText(lib.functions.sanitize_text(self.entry.text()))

    def keyPressEvent(self, event):
        """Deletes selected packages with the delete key"""
        if event.key() == QtCore.Qt.Key_Delete:
            self.remove_selected_packages()
        else:
            QtWidgets.QWidget.keyPressEvent(self, event)
