# Version 1.2

import sys
import webbrowser
import PyQt4.QtGui as Gui
import PyQt4.QtCore as Core


class pip_data():
    def get_outdated_packages(self):
        self.process = Core.QProcess()
        self.process.start("pip", ["list", "-o"])
        self.process.waitForFinished()

        self.outdated_packages = []

        self.out = bytes(self.process.readAllStandardOutput()).decode()
        self.out = self.out.split("\n")

        for item in self.out:
            if item is not "":
                package = []
                item.replace("\r", "")
                package.append(item[0:item.index("(") - 1])
                package.append(find_between(item, "(", ")"))
                package.append(find_between(item, "Latest: ", " ["))
                self.outdated_packages.append(package)

        return self.outdated_packages

    def get_uptodate_packages(self):
        self.process = Core.QProcess()
        self.process.start("pip", ["list", "-u"])
        self.process.waitForFinished()

        self.uptodate_packages = []

        self.out = bytes(self.process.readAllStandardOutput()).decode()
        self.out = self.out.split("\n")

        for item in self.out:
            if item is not "":
                package = []
                item.replace("\r", "")
                package.append(item[0:item.index("(") - 1])
                package.append(find_between(item, "(", ")"))
                package.append(find_between(item, "(", ")"))
                self.uptodate_packages.append(package)

        return self.uptodate_packages

    def get_all_packages(self):
        self.wait = wait_widget()
        self.wait.build()

        Gui.QApplication.processEvents()

        out = self.get_outdated_packages()
        up = self.get_uptodate_packages()

        self.wait.close()

        return out + up

    def update_packages(self, packages):
        command = ["install", "--upgrade"]

        for package in packages:
            command.append(package)

        self.output = output_widget(self)
        self.output.build()

        Gui.QApplication.processEvents()

        self.process = Core.QProcess()
        self.process.setProcessChannelMode(Core.QProcess.MergedChannels)
        self.process.readyRead.connect(self.output.data_ready)
        self.process.start("pip", command)

        self.process.waitForFinished()

        self.output.close()

    def install_packages(self, packages):
        command = ["install"]

        for package in packages:
            command.append(package)

        self.output = output_widget(self)
        self.output.build()

        Gui.QApplication.processEvents()

        self.process = Core.QProcess()
        self.process.setProcessChannelMode(Core.QProcess.MergedChannels)
        self.process.readyRead.connect(self.output.data_ready)
        self.process.start("pip", command)

        self.process.waitForFinished()

        self.output.close()

    def delete_packages(self, packages):
        command = ["uninstall"]

        for package in packages:
            command.append(package)

        command.append("-y")

        self.output = output_widget(self)
        self.output.build()

        Gui.QApplication.processEvents()

        self.process = Core.QProcess()
        self.process.setProcessChannelMode(Core.QProcess.MergedChannels)
        self.process.readyRead.connect(self.output.data_ready)
        self.process.start("pip", command)

        self.process.waitForFinished()

        self.output.close()


class info_widget(Gui.QWidget):
    def __init__(self, parent=None):
        Gui.QWidget.__init__(self)
        self.parent = parent

    def build(self):
        self.setWindowTitle("Info")
        self.setWindowIcon(Gui.QIcon("icons/main_icon.png"))
        self.setWindowModality(Core.Qt.ApplicationModal)

        self.layout = Gui.QGridLayout()

        self.name_label = Gui.QLabel("Name:")
        self.layout.addWidget(self.name_label, 0, 0)

        self.name = Gui.QLineEdit()
        self.name.setReadOnly(True)
        self.layout.addWidget(self.name, 0, 1)

        self.version_label = Gui.QLabel("Version:")
        self.layout.addWidget(self.version_label, 1, 0)

        self.version = Gui.QLineEdit()
        self.version.setReadOnly(True)
        self.layout.addWidget(self.version, 1, 1)

        self.summary_label = Gui.QLabel("Summary:")
        self.layout.addWidget(self.summary_label, 2, 0)

        self.summary = Gui.QLineEdit()
        self.summary.setReadOnly(True)
        self.layout.addWidget(self.summary, 2, 1)

        self.homepage_label = Gui.QLabel("Homepage:")
        self.layout.addWidget(self.homepage_label, 3, 0)

        self.homepage = Gui.QLineEdit()
        self.homepage.setReadOnly(True)
        self.layout.addWidget(self.homepage, 3, 1)

        self.sub_layout = Gui.QHBoxLayout()

        self.homepage_button = Gui.QPushButton("Open Homepage")
        self.sub_layout.addWidget(self.homepage_button)

        self.pypi_button = Gui.QPushButton("Open on PyPi")
        self.sub_layout.addWidget(self.pypi_button)
        self.layout.addLayout(self.sub_layout, 4, 0, 2, 2)

        self.author_label = Gui.QLabel("Author(s):")
        self.layout.addWidget(self.author_label, 6, 0)

        self.author = Gui.QLineEdit()
        self.author.setReadOnly(True)
        self.layout.addWidget(self.author, 6, 1)

        self.author_email_label = Gui.QLabel("Author Email:")
        self.layout.addWidget(self.author_email_label, 7, 0)

        self.author_email = Gui.QLineEdit()
        self.author_email.setReadOnly(True)
        self.layout.addWidget(self.author_email, 7, 1)

        self.license_label = Gui.QLabel("License:")
        self.layout.addWidget(self.license_label, 8, 0)

        self.license = Gui.QLineEdit()
        self.license.setReadOnly(True)
        self.layout.addWidget(self.license, 8, 1)

        self.requirements_label = Gui.QLabel("Requirements:")
        self.layout.addWidget(self.requirements_label, 9, 0)

        self.requirements = Gui.QLineEdit()
        self.requirements.setReadOnly(True)
        self.layout.addWidget(self.requirements, 9, 1)

        self.location_label = Gui.QLabel("Location:")
        self.layout.addWidget(self.location_label, 10, 0)

        self.location = Gui.QLineEdit()
        self.location.setReadOnly(True)
        self.layout.addWidget(self.location, 10, 1)

        self.homepage_button.clicked.connect(self.open_homepage)
        self.pypi_button.clicked.connect(self.open_pypi)

        self.setLayout(self.layout)

        self.show()

        center_widget(self)

    def set_data(self, package):
        self.process = Core.QProcess()
        self.process.start("pip", ["show", package])
        self.process.waitForFinished()

        self.out = bytes(self.process.readAllStandardOutput()).decode()

        name = find_between(self.out, "Name: ", "\n")
        version = find_between(self.out, "Version: ", "\n")
        summary = find_between(self.out, "Summary: ", "\n")
        homepage = find_between(self.out, "Home-page: ", "\n")
        author = find_between(self.out, "Author: ", "\n")
        author_email = find_between(self.out, "Author-email: ", "\n")
        license = find_between(self.out, "License: ", "\n")
        location = find_between(self.out, "Location: ", "\n")
        requirements = find_between(self.out, "Requires: ", "\n")

        self.name.setText(name)
        self.version.setText(version)
        self.summary.setText(summary)
        self.homepage.setText(homepage)
        self.author.setText(author)
        self.author_email.setText(author_email)
        self.license.setText(license)
        self.location.setText(location)
        self.requirements.setText(requirements)

        data = []
        lineedits = [self.name, self.version, self.summary, self.homepage, self.author, self.author_email, self.license, self.location, self.requirements]

        for lineedit in lineedits:
            data.append(self.get_string_width(lineedit))

        length = max(data) + 10

        for lineedit in lineedits:
            lineedit.setMinimumWidth(length)

        self.setWindowTitle(name + " Info")

    def open_homepage(self):
        webbrowser.open(self.homepage.text())

    def open_pypi(self):
        webbrowser.open("https://pypi.python.org/pypi/" + self.name.text())

    def get_string_width(self, lineedit):
        return lineedit.fontMetrics().boundingRect(lineedit.text()).width()


class wait_widget(Gui.QWidget):
    def build(self):
        self.setWindowTitle("Please wait...")
        self.setWindowIcon(Gui.QIcon("icons/main_icon.png"))

        self.layout = Gui.QVBoxLayout()

        self.label = Gui.QLabel("Getting installed pip packages")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        self.show()

        center_widget(self)

        Gui.QApplication.processEvents()


class output_widget(Gui.QWidget):
    def __init__(self, parent=None):
        Gui.QWidget.__init__(self)
        self.parent = parent

    def build(self):
        self.setWindowTitle("Output")
        self.setWindowIcon(Gui.QIcon("icons/main_icon.png"))

        self.layout = Gui.QGridLayout()

        self.output = Gui.QTextBrowser()
        self.output.setTextColor(Gui.QColor("green"))
        self.output.setStyleSheet("background-color: black;")

        self.layout.addWidget(self.output)

        self.setLayout(self.layout)

        self.show()

        center_widget(self)

    def data_ready(self):
        text = bytes(self.parent.process.readAll()).decode()
        self.output.append(text)
        Gui.QApplication.processEvents()


class entry(Gui.QLineEdit):
    def __init__(self, parent=None):
        Gui.QLineEdit.__init__(self)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.key() == Core.Qt.Key_Up:
            if self.parent.count < len(self.parent.past_items) - 1:
                self.parent.count += 1
            if self.parent.past_items != []:
                self.setText(self.parent.past_items[self.parent.count])
        elif event.key() == Core.Qt.Key_Down:
            if self.parent.count > 0:
                self.parent.count -= 1
            if self.parent.past_items != [] and self.parent.count > -1:
                self.setText(self.parent.past_items[self.parent.count])
        else:
            Gui.QLineEdit.keyPressEvent(self, event)


class add_widget(Gui.QWidget):
    def __init__(self, parent=None):
        Gui.QWidget.__init__(self)
        self.parent = parent

    def build(self):
        self.pip = pip_data()
        self.items = []
        self.correct_text = ""
        self.past_items = []
        self.count = -1

        self.setWindowTitle("Add Packages")
        self.setWindowIcon(Gui.QIcon("icons/main_icon.png"))
        self.setWindowModality(Core.Qt.ApplicationModal)

        self.layout = Gui.QVBoxLayout()

        self.list = Gui.QListWidget()
        self.layout.addWidget(self.list)

        self.entry = entry(self)
        self.layout.addWidget(self.entry)

        # for some reason works
        Core.QTimer.singleShot(0, self.entry.setFocus)

        self.sub_layout = Gui.QHBoxLayout()

        self.add_button = Gui.QPushButton("Add")
        self.sub_layout.addWidget(self.add_button)

        self.remove_button = Gui.QPushButton("Remove")
        self.sub_layout.addWidget(self.remove_button)

        self.layout.addLayout(self.sub_layout)

        self.submit_button = Gui.QPushButton("Submit")
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

        self.add_button.clicked.connect(self.add)
        self.remove_button.clicked.connect(self.remove)
        self.submit_button.clicked.connect(self.submit)
        self.entry.textEdited.connect(self.entry_edited)
        self.entry.returnPressed.connect(self.add)
        self.list.itemChanged.connect(self.list_edited)

        self.show()

        center_widget(self)

    def add(self):
        self.update_items()

        if self.entry.text() != "":
            if self.entry.text() not in self.items:
                item = Gui.QListWidgetItem(self.entry.text())
                item.setFlags(item.flags() | Core.Qt.ItemIsEditable | Core.Qt.ItemIsSelectable | Core.Qt.ItemIsDragEnabled)

                self.list.addItem(item)
                self.items.append(self.entry.text())
                self.past_items.insert(0, self.entry.text())
                self.entry.setText("")

    def remove(self):
        self.update_items()

        for item in self.list.selectedItems():
            self.list.takeItem(self.list.row(item))
            self.items.remove(item.text())

    def update_items(self):
        self.items = []

        for item in range(self.list.count()):
            self.items.append(self.list.item(item).text())

    def submit(self):
        self.submit_button.setEnabled(False)

        self.update_items()
        self.pip.install_packages(self.items)
        self.close()

        self.parent.refresh()

    def entry_edited(self):
        if "|" in self.entry.text() or "&" in self.entry.text() or ";" in self.entry.text():
            self.entry.setText(self.correct_text)
        else:
            self.correct_text = self.entry.text()

    def list_edited(self, item):
        text = item.text()
        text = text.replace("|", " ")
        text = text.replace(";", " ")
        text = text.replace("&", " ")
        item.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Core.Qt.Key_Delete:
            self.remove()
        else:
            Gui.QWidget.keyPressEvent(self, event)


class table(Gui.QTableWidget):
    def __init__(self, parent=None):
        super(table, self).__init__(parent)
        self.parent = parent
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

    def set_data(self, data):
        self.setColumnCount(4)
        self.setRowCount(len(data))

        for r, row in enumerate(data):
            for c, col in enumerate(row):
                item = Gui.QTableWidgetItem(str(col))
                item.setFlags(Core.Qt.ItemIsEnabled | Core.Qt.ItemIsSelectable)
                self.setItem(r, c, item)

        self.setHorizontalHeaderLabels(["Package", "Installed Version", "Latest Version", "Status"])
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.setColumnWidth(0, 150)

        self.parent.setMinimumWidth(self.horizontalHeader().length() + 63)

    def set_status(self):
        for row in range(self.rowCount()):
            if self.item(row, 1).text() != self.item(row, 2).text():
                self.item(row, 1).setForeground(Gui.QColor("red"))
                self.setItem(row, 3, Gui.QTableWidgetItem("Out of date"))
            else:
                self.item(row, 1).setForeground(Gui.QColor("green"))
                self.setItem(row, 3, Gui.QTableWidgetItem("Up to date"))


class main_widget(Gui.QWidget):
    def build(self):
        self.pip = pip_data()

        self.layout = Gui.QGridLayout()

        self.add_icon = Gui.QIcon("icons/add_icon.png")
        self.add_button = Gui.QPushButton(self.add_icon, "Add", self)
        self.layout.addWidget(self.add_button, 0, 0)

        self.delete_icon = Gui.QIcon("icons/delete_icon.png")
        self.delete_button = Gui.QPushButton(self.delete_icon, "Delete", self)
        self.layout.addWidget(self.delete_button, 0, 1)

        self.update_icon = Gui.QIcon("icons/update_icon.png")
        self.update_button = Gui.QPushButton(self.update_icon, "Update", self)
        self.layout.addWidget(self.update_button, 0, 3)

        self.update_all_icon = Gui.QIcon("icons/update_icon.png")
        self.update_all_button = Gui.QPushButton(self.update_icon, "Update All", self)
        self.layout.addWidget(self.update_all_button, 0, 4)

        self.info_icon = Gui.QIcon("icons/info_icon.png")
        self.info_button = Gui.QPushButton(self.info_icon, "Info", self)
        self.layout.addWidget(self.info_button, 0, 8)

        self.refresh_icon = Gui.QIcon("icons/refresh_icon.png")
        self.refresh_button = Gui.QPushButton(self.refresh_icon, "Refresh", self)
        self.layout.addWidget(self.refresh_button, 0, 9)

        self.table = table(self)
        self.layout.addWidget(self.table, 1, 0, 1, 10)

        self.setLayout(self.layout)

        self.add_button.clicked.connect(self.add)
        self.delete_button.clicked.connect(self.delete)
        self.update_button.clicked.connect(self.update)
        self.update_all_button.clicked.connect(self.update_all)
        self.refresh_button.clicked.connect(self.refresh)
        self.info_button.clicked.connect(self.info)
        self.table.doubleClicked.connect(self.info)

        self.show()
        self.refresh()

    def get_selected_rows(self):
        rows = []
        for item in self.table.selectedIndexes():
            if item.row() not in rows:
                rows.append(item.row())

        return rows

    def add(self):
        self.add_button.setEnabled(False)

        global wid
        # prevents the garbage collector from immediatley destroying it
        wid = add_widget(self)
        wid.build()

        self.add_button.setEnabled(True)

    def delete(self):
        self.delete_button.setEnabled(False)

        packages = []

        rows = self.get_selected_rows()

        if rows == []:
            return
        for row in rows:
            if "pip" == self.table.item(row, 0).text():
                return
            else:
                packages.append(self.table.item(row, 0).text())

        self.pip.delete_packages(packages)

        self.refresh()

        self.delete_button.setEnabled(True)

    def update(self):
        self.update_button.setEnabled(False)

        packages = []

        rows = self.get_selected_rows()
        if rows == []:
            return

        for row in rows:
            if self.table.item(row, 3).text() == "Out of date":
                packages.append(self.table.item(row, 0).text())

        if packages != []:
            self.pip.update_packages(packages)
            self.refresh()

        self.update_button.setEnabled(True)

    def update_all(self):
        self.update_all_button.setEnabled(False)

        packages = []

        for row in range(self.table.rowCount()):
            if self.table.item(row, 3).text() == "Out of date":
                packages.append(self.table.item(row, 0).text())

        if packages != []:
            self.pip.update_packages(packages)
            self.refresh()

        self.update_all_button.setEnabled(True)

    def refresh(self):
        self.refresh_button.setEnabled(False)

        self.table.set_data(self.pip.get_all_packages())
        self.table.set_status()

        self.refresh_button.setEnabled(True)

    def contextMenuEvent(self, event):
        self.right_click_menu = Gui.QMenu(self)

        update_action = Gui.QAction('Update', self)
        update_action.triggered.connect(self.update)
        self.right_click_menu.addAction(update_action)

        delete_action = Gui.QAction('Delete', self)
        delete_action.triggered.connect(self.delete)
        self.right_click_menu.addAction(delete_action)

        info_action = Gui.QAction('Info', self)
        info_action.triggered.connect(self.info)
        self.right_click_menu.addAction(info_action)

        self.right_click_menu.popup(Gui.QCursor.pos())

    def info(self):
        self.info_button.setEnabled(False)

        rows = self.get_selected_rows()

        global wid
        # prevents the garbage collector from immediatley destroying it
        wid = info_widget(self)
        wid.build()

        wid.set_data(self.table.item(rows[0], 0).text())
        self.info_button.setEnabled(True)


class main_window(Gui.QMainWindow):
    def build(self):
        self.setWindowTitle("PipQt")
        self.setWindowIcon(Gui.QIcon("icons/main_icon.png"))

        self.main_widget = main_widget()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')

        menuAction = Gui.QAction('Exit', self)
        menuAction.triggered.connect(sys.exit)
        fileMenu.addAction(menuAction)

        editMenu = mainMenu.addMenu('Edit')

        menuAction = Gui.QAction('Add Packages', self)
        menuAction.triggered.connect(self.main_widget.add)
        editMenu.addAction(menuAction)

        editMenu.addSeparator()

        menuAction = Gui.QAction('Refresh Packages', self)
        menuAction.triggered.connect(self.main_widget.refresh)
        editMenu.addAction(menuAction)

        editMenu.addSeparator()

        menuAction = Gui.QAction('Update Selected Packages', self)
        menuAction.triggered.connect(self.main_widget.update)
        editMenu.addAction(menuAction)

        menuAction = Gui.QAction('Update All Packages', self)
        menuAction.triggered.connect(self.main_widget.update_all)
        editMenu.addAction(menuAction)

        editMenu.addSeparator()

        menuAction = Gui.QAction('Delete Selected Packages', self)
        menuAction.triggered.connect(self.main_widget.delete)
        editMenu.addAction(menuAction)

        self.show()

        self.setCentralWidget(self.main_widget)
        self.main_widget.build()

        self.resize(self.width(), 500)

        self.setStatusBar(Gui.QStatusBar().showMessage("Getting pip packages"))


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def center_widget(widget):
    x = main.pos().x() + (0.5 * main.width()) - (0.5 * widget.width())
    y = main.pos().y() + (0.5 * main.height()) - (0.5 * widget.height())

    widget.move(x, y)


if __name__ == "__main__":
    args = sys.argv

    app = Gui.QApplication(args)

    global main

    main = main_window()
    main.build()

    sys.exit(app.exec_())
