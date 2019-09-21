import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets

import lib.pip_api

from .info_widget import info_widget
from .install_widget import install_widget
from .output_widget import output_widget
from .table import table


class main_widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent

    def build(self):
        """Build widget"""
        self.layout = QtWidgets.QGridLayout()

        self.install_icon = QtGui.QIcon("icons/install_icon.png")
        self.install_button = QtWidgets.QPushButton(self.install_icon, "Install", self)
        self.layout.addWidget(self.install_button, 0, 0)

        self.uninstall_icon = QtGui.QIcon("icons/uninstall_icon.png")
        self.uninstall_button = QtWidgets.QPushButton(
            self.uninstall_icon, "Uninstall", self
        )
        self.layout.addWidget(self.uninstall_button, 0, 1)

        self.update_icon = QtGui.QIcon("icons/update_icon.png")
        self.update_button = QtWidgets.QPushButton(self.update_icon, "Update", self)
        self.layout.addWidget(self.update_button, 0, 4)

        self.update_all_icon = QtGui.QIcon("icons/update_icon.png")
        self.update_all_button = QtWidgets.QPushButton(
            self.update_icon, "Update All", self
        )
        self.layout.addWidget(self.update_all_button, 0, 5)

        self.info_icon = QtGui.QIcon("icons/info_icon.png")
        self.info_button = QtWidgets.QPushButton(self.info_icon, "Info", self)
        self.layout.addWidget(self.info_button, 0, 8)

        self.refresh_icon = QtGui.QIcon("icons/refresh_icon.png")
        self.refresh_button = QtWidgets.QPushButton(self.refresh_icon, "Refresh", self)
        self.layout.addWidget(self.refresh_button, 0, 9)

        self.table = table(self)
        self.layout.addWidget(self.table, 1, 0, 1, 10)

        self.setLayout(self.layout)

        self.install_button.clicked.connect(self.install)
        self.uninstall_button.clicked.connect(self.uninstall)
        self.update_button.clicked.connect(self.update)
        self.update_all_button.clicked.connect(self.update_all)
        self.refresh_button.clicked.connect(self.refresh)
        self.info_button.clicked.connect(self.info)
        self.table.doubleClicked.connect(self.info)

        self.pip_api = lib.pip_api.api()

        self.show()

    def get_selected_rows(self):
        """Returns a list of row indexes that are currently selected"""
        return list(set(index.row() for index in self.table.selectedIndexes()))

    def info(self):
        """Open dialog to view package info"""
        self.info_button.setEnabled(False)

        rows = self.get_selected_rows()
        if rows:
            global diag
            # prevents the garbage collector from immediatley destroying it
            diag = info_widget(self)
            diag.build()

            name = self.table.get_package_status(rows[0])["name"]

            package_info = self.pip_api.get_package_information(name)
            diag.set_data(package_info)

        self.info_button.setEnabled(True)

    def install(self):
        """Open dialog to install new packages"""
        self.install_button.setEnabled(False)

        global diag

        diag = install_widget(self.pip_api, self.parent)
        diag.build()

        self.install_button.setEnabled(True)

    def uninstall(self):
        """Uninstalls selected packages"""
        self.uninstall_button.setEnabled(False)

        global diag

        diag = output_widget(self)
        diag.build()

        packages = []
        rows = self.get_selected_rows()

        # get the currently selected packages and make sure the user
        # does not try to uninstall pip
        for row in rows:
            name = self.table.get_package_status(row)["name"]
            if name == "pip":
                raise Exception
            else:
                packages.append(name)

        if packages:
            self.pip_api.uninstall_packages(packages, diag.data_ready)
            self.refresh()

        diag.close()
        self.uninstall_button.setEnabled(True)

    def update(self):
        """Update selected packages"""
        self.update_button.setEnabled(False)

        global diag

        diag = output_widget(self)
        diag.build()

        packages = []
        rows = self.get_selected_rows()

        # get the currently selected packages that are outdated
        for row in rows:
            package_data = self.table.get_package_status(row)
            if not package_data["status"]:
                packages.append(package_data["name"])

        if packages:
            self.pip_api.update_packages(packages, diag.data_ready)
            self.refresh()

        diag.close()
        self.update_button.setEnabled(True)

    def update_all(self):
        """Update all outdated packages"""
        self.update_all_button.setEnabled(False)

        global diag

        diag = output_widget(self)
        diag.build()

        # get outdated packages from cache
        packages = self.pip_api.get_package_list_from_json(
            self.pip_api.get_outdated_packages(output=diag.data_ready)
        )

        # if we have packages, update them
        if packages:
            self.pip_api.update_packages(packages, diag.data_ready)
            self.refresh()

        diag.close()
        self.update_all_button.setEnabled(True)

    def refresh(self):
        """Refresh all table data"""
        self.refresh_button.setEnabled(False)
        self.parent.statusBar().showMessage("Getting installed pip packages")
        # QtWidgets.QApplication.processEvents()

        global diag

        diag = output_widget(self)
        diag.build()

        # refresh data and ignore cache
        self.table.set_data(self.pip_api.get_packages(True, diag.data_ready))

        diag.close()
        self.parent.statusBar().showMessage("")
        self.refresh_button.setEnabled(True)

    def contextMenuEvent(self, event):
        """Override default context menu event to provide right-click menu"""
        self.right_click_menu = QtWidgets.QMenu(self)

        update_action = QtWidgets.QAction("Update", self)
        update_action.triggered.connect(self.update)
        self.right_click_menu.addAction(update_action)

        uninstall_action = QtWidgets.QAction("Uninstall", self)
        uninstall_action.triggered.connect(self.uninstall)
        self.right_click_menu.addAction(uninstall_action)

        info_action = QtWidgets.QAction("Info", self)
        info_action.triggered.connect(self.info)
        self.right_click_menu.addAction(info_action)

        # popup at cursor position
        self.right_click_menu.popup(self.mapToGlobal(event.pos()))
