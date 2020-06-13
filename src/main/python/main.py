from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from main_ui import Ui_MainWindow

import sys

app = ApplicationContext()


class MainWindow(QMainWindow):
    app_version = app.build_settings['version']
    ui = Ui_MainWindow()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("NW File Renamer")
        self.ui.setupUi(self)



if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.app.exec_())
