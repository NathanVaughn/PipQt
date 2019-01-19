import webbrowser

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets

import lib.functions


class info_widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent

    def build(self):
        """Build widget"""
        self.setWindowTitle("Info")
        self.setWindowIcon(QtGui.QIcon("icons/main_icon.png"))
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.layout = QtWidgets.QGridLayout()

        self.name_label = QtWidgets.QLabel("Name:")
        self.layout.addWidget(self.name_label, 0, 0)

        self.name = QtWidgets.QLineEdit()
        self.name.setReadOnly(True)
        self.layout.addWidget(self.name, 0, 1)

        self.version_label = QtWidgets.QLabel("Version:")
        self.layout.addWidget(self.version_label, 1, 0)

        self.version = QtWidgets.QLineEdit()
        self.version.setReadOnly(True)
        self.layout.addWidget(self.version, 1, 1)

        self.summary_label = QtWidgets.QLabel("Summary:")
        self.layout.addWidget(self.summary_label, 2, 0)

        self.summary = QtWidgets.QLineEdit()
        self.summary.setReadOnly(True)
        self.layout.addWidget(self.summary, 2, 1)

        self.homepage_label = QtWidgets.QLabel("Homepage:")
        self.layout.addWidget(self.homepage_label, 3, 0)

        self.homepage = QtWidgets.QLineEdit()
        self.homepage.setReadOnly(True)
        self.layout.addWidget(self.homepage, 3, 1)

        self.sub_layout = QtWidgets.QHBoxLayout()

        self.homepage_button = QtWidgets.QPushButton("Open Homepage")
        self.sub_layout.addWidget(self.homepage_button)

        self.pypi_button = QtWidgets.QPushButton("Open on PyPi")
        self.sub_layout.addWidget(self.pypi_button)
        self.layout.addLayout(self.sub_layout, 4, 0, 2, 2)

        self.author_label = QtWidgets.QLabel("Author(s):")
        self.layout.addWidget(self.author_label, 6, 0)

        self.author = QtWidgets.QLineEdit()
        self.author.setReadOnly(True)
        self.layout.addWidget(self.author, 6, 1)

        self.author_email_label = QtWidgets.QLabel("Author Email:")
        self.layout.addWidget(self.author_email_label, 7, 0)

        self.author_email = QtWidgets.QLineEdit()
        self.author_email.setReadOnly(True)
        self.layout.addWidget(self.author_email, 7, 1)

        self.license_label = QtWidgets.QLabel("License:")
        self.layout.addWidget(self.license_label, 8, 0)

        self.license = QtWidgets.QLineEdit()
        self.license.setReadOnly(True)
        self.layout.addWidget(self.license, 8, 1)

        self.requirements_label = QtWidgets.QLabel("Requirements:")
        self.layout.addWidget(self.requirements_label, 9, 0)

        self.requirements = QtWidgets.QLineEdit()
        self.requirements.setReadOnly(True)
        self.layout.addWidget(self.requirements, 9, 1)

        self.location_label = QtWidgets.QLabel("Location:")
        self.layout.addWidget(self.location_label, 10, 0)

        self.location = QtWidgets.QLineEdit()
        self.location.setReadOnly(True)
        self.layout.addWidget(self.location, 10, 1)

        self.homepage_button.clicked.connect(self.open_homepage)
        self.pypi_button.clicked.connect(self.open_pypi)

        self.setLayout(self.layout)

        self.show()
        self.raise_()
        lib.functions.center_widget(self.parent.parent, self)

        self.setMaximumHeight(self.height())

    def set_data(self, package_data):
        """Apply passed data"""
        name_str = package_data["Name"]
        version_str = package_data["Version"]
        summary_str = package_data["Summary"]
        homepage_str = package_data["Home-page"]
        author_str = package_data["Author"]
        author_email_str = package_data["Author-email"]
        license_str = package_data["License"]
        location_str = package_data["Location"]
        requirements_str = package_data["Requires"]

        self.name.setText(name_str)
        self.name.home(False)

        self.version.setText(version_str)
        self.version.home(False)

        self.summary.setText(summary_str)
        self.summary.home(False)

        self.homepage.setText(homepage_str)
        self.homepage.home(False)

        self.author.setText(author_str)
        self.author.home(False)

        self.author_email.setText(author_email_str)
        self.author_email.home(False)

        self.license.setText(license_str)
        self.license.home(False)

        self.location.setText(location_str)
        self.location.home(False)

        self.requirements.setText(requirements_str)
        self.requirements.home(False)

        self.setWindowTitle(name_str + " Info")

    def open_homepage(self):
        """Open package homepage"""
        webbrowser.open(self.homepage.text())

    def open_pypi(self):
        """Open package on pypi"""
        webbrowser.open("https://pypi.org/project/" + self.name.text())
