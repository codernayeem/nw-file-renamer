from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
from main_ui import Ui_MainWindow
from tool import FileData, is_valid_dir, join, Path, get_splitted_by_pipe

import sys

app = ApplicationContext()

class CustomLabel(QtWidgets.QLabel):
    def __init__(self, parent, main):
        super(QtWidgets.QLabel, self).__init__(parent)
        self.setAcceptDrops(True)
        self.Root = main
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self.Root.select_folder(drag=True, folders=[i.toLocalFile() for i in event.mimeData().urls()])

class MainWindow(QtWidgets.QMainWindow):
    app_version = app.build_settings['version']
    main_icon = app.get_resource('icon.png')
    ui = Ui_MainWindow()
    FILEDATA = FileData()

    last_selected_dir = 'C:'

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui.setupUi(self, CustomLabel)
        self.setWindowTitle("NW File Renamer")
        self.about_page = None
        self.dialog = None
        self.setIcons(ic1=app.get_resource('plus.png'), ic2=app.get_resource('add.png'), ic3=app.get_resource('clear.png'), ic4=app.get_resource('reset.png'), ic5=app.get_resource('exit.png'))
        self.set_menu_toolbar_button_action()
        self.ui.txt_stat.setText(self.FILEDATA.get_status_txt())

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

    def set_menu_toolbar_button_action(self):
        # menu
        # self.ui.actionAbout_the_Author.triggered.connect(lambda: see_about(self))
        self.ui.actionExit_1.triggered.connect(lambda: sys.exit(0))
        self.ui.actionAdd_1.triggered.connect(lambda: self.select_folder())
        self.ui.actionAdd_Multiple_Folder.triggered.connect(lambda: self.select_folder(multiple=True))
        self.ui.actionClear.triggered.connect(lambda: self.clear_all_folders())
        # self.ui.actionReset.triggered.connect(lambda: self.reset_all())

        # toolbar
        self.ui.actionAdd.triggered.connect(lambda: self.select_folder())
        self.ui.actionClear.triggered.connect(lambda: self.clear_all_folders())
        # self.ui.actionReset.triggered.connect(lambda: self.reset_all())
        self.ui.actionExit.triggered.connect(lambda: sys.exit(0))

        # sidebar
        self.ui.bt_main_menu.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

        # mainbar main page
        self.ui.bt_menu_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.bt_menu_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.bt_menu_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.bt_menu_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))

    def select_folder(self, multiple=False, drag=False, folders=None):
        if multiple:
            file_dialog = QtWidgets.QFileDialog(directory=self.last_selected_dir)
            file_dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
            file_dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
            file_dialog.setWindowTitle("Select Folders")
            file_dialog.setWindowIcon(QtGui.QIcon(self.main_icon))
            f_tree_view = file_dialog.findChild(QtWidgets.QTreeView)
            if f_tree_view:
                f_tree_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            if not file_dialog.exec():
                return
            folders = file_dialog.selectedFiles()
        elif drag:
            folders = [f for f in folders if is_valid_dir(f)]
        else:
            folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", directory=self.last_selected_dir))
            if folder == '':
                return
            folder = str(Path(folder))
            self.last_selected_dir = join(*folder.split('\\')[:len(folder.split('\\'))-1])
            folders = [folder]
        self.FILEDATA.select_dirs(folders)
        self.ui.txt_stat.setText(self.FILEDATA.get_status_txt())

    def clear_all_folders(self):
        self.FILEDATA.reset()
        self.ui.txt_stat.setText(self.FILEDATA.get_status_txt())


if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.app.exec_())
