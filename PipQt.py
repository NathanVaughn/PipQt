import sys

import PySide2.QtWidgets as QtWidgets

import widgets

if __name__ == "__main__":
    args = sys.argv

    app = QtWidgets.QApplication(args)

    # create instance of main window class
    main_window = widgets.main_window(app)
    # build the main window
    main_window.build()
    # load data
    main_window.main_widget.refresh()

    sys.exit(app.exec_())
