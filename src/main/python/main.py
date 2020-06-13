from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
from main_ui import Ui_MainWindow

import sys

app = ApplicationContext()

class MainWindow(QtWidgets.QMainWindow):
    app_version = app.build_settings['version']
    main_icon = app.get_resource('icon.png')
    ui = Ui_MainWindow()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui.setupUi(self)
        self.setWindowTitle("NW File Renamer")
        self.setIcons(ic1=app.get_resource('plus.png'), ic2=app.get_resource('add.png'), ic3=app.get_resource('clear.png'), ic4=app.get_resource('reset.png'), ic5=app.get_resource('exit.png'))
        self.about_page = None
        self.dialog = None

    def setIcons(self, **arg):
        icon = QtGui.QIcon(arg.get('ic4', ''))
        self.ui.bt_reset_1.setIcon(icon)
        self.ui.bt_reset_2.setIcon(icon)
        self.ui.bt_reset_3.setIcon(icon)
        self.ui.bt_reset_4.setIcon(icon)
        self.ui.actionReset.setIcon(icon)
        self.ui.actionReset_1.setIcon(icon)
        icon = QtGui.QIcon(arg.get('ic5', ''))
        self.ui.actionExit.setIcon(icon)
        self.ui.actionExit_1.setIcon(icon)
        icon = QtGui.QIcon(arg.get('ic1', ''))
        self.ui.actionAdd.setIcon(icon)
        self.ui.actionAdd_1.setIcon(icon)
        icon = QtGui.QIcon(arg.get('ic3', ''))
        self.ui.actionClear.setIcon(icon)
        self.ui.actionClear_1.setIcon(icon)
        self.ui.actionAdd_Multiple_Folder.setIcon(QtGui.QIcon(arg.get('ic2', '')))
        self.ui.actionAbout_the_Author.setIcon(QtGui.QIcon(self.main_icon))


if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.app.exec_())
