import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets


class table(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(table, self).__init__(parent)
        self.parent = parent

        self.headers = ["Package", "Installed Version", "Latest Version", "Status"]

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

    def packages_data_to_array(self, packages_data):
        """Convert ditionary of package data to an array for the table"""
        packages_list = []

        for package in packages_data:
            # allocate empty list
            temp_package = [None] * 4
            # put in name and version
            temp_package[0] = package["name"]
            temp_package[1] = package["version"]

            # check if there is a latest version key
            if "latest_version" in package:
                # out of date
                temp_package[2] = package["latest_version"]
                temp_package[3] = "Out of date"
            else:
                # up to date
                temp_package[2] = package["version"]
                temp_package[3] = "Up to date"

            packages_list.append(temp_package)

        return packages_list

    def get_package_status(self, row):
        """Takes a row index and returns a package name and status.
        1 is updated, 0 is outdated"""

        status = 0
        name = self.item(row, 0).text()

        if self.item(row, 1).text() == self.item(row, 2).text():
            status = 1

        return {"name": name, "status": status}

    def set_data(self, packages_data):
        """Take dictionary of package data and put into table"""
        # turn the dictionaries into a list
        data = self.packages_data_to_array(packages_data)

        # workaround for data disappearing
        self.setSortingEnabled(False)
        # clear all data
        self.clear()

        # the row and column count based on the data size
        self.setColumnCount(len(data[0]))
        self.setRowCount(len(data))

        # create each item
        for r, row in enumerate(data):
            for c, col in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(col))
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                self.setItem(r, c, item)

        self.set_colors()

        # set the horizontal headers
        self.setHorizontalHeaderLabels(self.headers)

        # resize rows and columns
        self.resizeRowsToContents()
        self.resizeColumnsToContents()

        # sort packages alphabetically
        self.sortItems(0)

        # 63 is a magic number
        self.parent.setMinimumWidth(self.horizontalHeader().length() + 63)

        # reenable sorting
        self.setSortingEnabled(True)

    def set_colors(self):
        """Change the text colors for packages depending on status"""
        for row in range(self.rowCount()):
            # check if the two version numbers match
            if self.get_package_status(row)["status"]:
                self.item(row, 1).setForeground(QtGui.QColor("green"))
            else:
                self.item(row, 1).setForeground(QtGui.QColor("red"))
