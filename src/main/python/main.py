from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
from main_ui import Ui_MainWindow
from dialogs import Ui_AboutPage
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
        self.set_mainpage_buttons()
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
        self.ui.actionAbout_the_Author.triggered.connect(lambda: self.see_about())
        self.ui.actionExit_1.triggered.connect(lambda: sys.exit(0))
        self.ui.actionAdd_1.triggered.connect(lambda: self.select_folder())
        self.ui.actionAdd_Multiple_Folder.triggered.connect(lambda: self.select_folder(multiple=True))
        self.ui.actionClear.triggered.connect(lambda: self.clear_all_folders())
        self.ui.actionReset.triggered.connect(lambda: self.reset_all())

        # toolbar
        self.ui.actionAdd.triggered.connect(lambda: self.select_folder())
        self.ui.actionClear.triggered.connect(lambda: self.clear_all_folders())
        self.ui.actionReset.triggered.connect(lambda: self.reset_all())
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

    def see_about(self):
        if self.about_page is None:
            self.about_page = QtWidgets.QWidget()
            self.about_page.ui = Ui_AboutPage()
            self.about_page.ui.setupUi(self.about_page)
            self.about_page.ui.version.setText(f'v{self.app_version}')
            self.about_page.ui.icon.setPixmap(QtGui.QPixmap(self.main_icon))
            self.about_page.ui.name.setText("NW File Renamer")
        self.about_page.destroy()
        self.about_page.show()

    def show_help_dialog(self, no):
        if self.dialog is None:
            self.dialog = QtWidgets.QWidget()
            font = QtGui.QFont()
            font.setPointSize(11)
            self.dialog.setFont(font)
            self.dialog.setWindowTitle("Help")
            self.dialog.gridlayout = QtWidgets.QGridLayout(self.dialog)
            self.dialog.main_text = QtWidgets.QTextBrowser(self.dialog)
            self.dialog.gridlayout.addWidget(self.dialog.main_text, 0, 0, 1, 2)
            self.dialog.bt_close = QtWidgets.QPushButton(self.dialog)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.dialog.bt_close.sizePolicy().hasHeightForWidth())
            self.dialog.bt_close.setSizePolicy(sizePolicy)
            self.dialog.bt_close.setText("Close")
            self.dialog.gridlayout.addWidget(self.dialog.bt_close, 1, 1, 1, 1)
            self.dialog.setWindowIcon(QtGui.QIcon(self.main_icon))
            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)
            QtWidgets.QShortcut(QtGui.QKeySequence('Esc'), self.dialog).activated.connect(lambda: self.dialog.close())
            self.dialog.bt_close.clicked.connect(lambda: self.dialog.close())
        
        if no == 1:
            self.dialog.setFixedWidth(400)
            self.dialog.setFixedHeight(270)
            self.dialog.main_text.setHtml("<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt; font-weight:600; text-decoration: underline;\">You can use these statement in name format :</span></p>\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Arial'; font-weight:600; text-decoration: underline;\"><br /></p>"
            "<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">&lt;no&gt;</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get file number </span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">&lt;file&gt;</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get full filename </span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">&lt;filename&gt;</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get filename without extension </span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">&lt;ext&gt;</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get file extension </span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">&lt;c_date&gt;</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get creation date </span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">&lt;m_date&gt;</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get modification date </span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">&lt;size&gt;</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get file size </span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">&lt;sizeb&gt;</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get file size in bytes </span></p></td></tr></table></body></html>")
        elif no == 2:
            self.dialog.setFixedWidth(590)
            self.dialog.setFixedHeight(250)
            self.dialog.main_text.setHtml("<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-size:12pt; font-weight:600; text-decoration: underline;\">You can use these statement in date format :</span></p>\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Arial\'; font-size:12pt; font-weight:600; text-decoration: underline;\"><br /></p>\n"
            "<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%a</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get short weekday (Sun , Mon)</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">   |  </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%A</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get full weekday (Sunday , Monday)</span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%d</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get day (01, 24)</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">   |  </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%m</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get month (01, 12)</span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%b</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get short month (Jan, Feb)</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">   |  </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%B</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get full month (January, February)</span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%y</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get short year (99, 20)</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">   |  </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%Y</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get full year(1999, 2020)</span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%I</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get Hour 12-hour clock (4, 12)</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">   |  </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%H</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get Hour 24-hour clock (6, 23)</span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%M</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get minute (10, 59)</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">   |  </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%S</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get second (10, 59)</span></p></td></tr>\n"
            "<tr>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">%%</span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\"> : </span></p></td>\n"
            "<td>\n"
            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\';\">get \'%\' character</span></p></td>\n"
            "<td></td>\n"
            "<td></td>\n"
            "<td></td>\n"
            "<td></td></tr></table></body></html>")
            
        self.dialog.destroy()
        self.dialog.show()

    def set_mainpage_buttons(self):
        # mainbar page 1
        self.ui.bt_rename_1.clicked.connect(lambda: self.go_for_rename(1, i1=self.ui.rn_1_input_1.currentIndex(), i2=self.ui.rn_1_input_2.text()))
        self.ui.bt_reset_1.clicked.connect(lambda: self.reset_page_1())
        def disable_wanted_ext(self, i):
            if i == 2:
                self.ui.widget_1_1.setEnabled(False)
            else:
                self.ui.widget_1_1.setEnabled(True)
        self.ui.rn_1_input_1.currentIndexChanged['int'].connect(lambda i: disable_wanted_ext(self, i))
        
        # mainbar page 2
        self.ui.bt_rename_2.clicked.connect(lambda: self.go_for_rename(2, i1=self.ui.rn_2_input_1.text(), i2=self.ui.rn_2_input_2.text(), i3=self.ui.rn_2_input_3.isChecked()))
        self.ui.bt_reset_2.clicked.connect(lambda: self.reset_page_2())

        # mainbar page 3
        self.ui.bt_rename_3.clicked.connect(lambda: self.go_for_rename(3, i1=self.ui.rn_3_input_1.text(), i2=self.ui.rn_3_input_2.isChecked(), i3=self.ui.rn_3_input_3.currentIndex(), i4=self.ui.rn_3_input_4.currentIndex(), i5=self.ui.rn_3_input_5.text(), i6=self.ui.rn_3_input_6.text(), i7=self.ui.rn_3_input_7.isChecked(), i8=self.ui.rn_3_input_8.text(), i9=self.ui.rn_3_input_9.text()))
        self.ui.bt_reset_3.clicked.connect(lambda: self.reset_page_3())
        self.ui.bt_help_3_1.clicked.connect(lambda: self.show_help_dialog(1))
        self.ui.bt_help_3_2.clicked.connect(lambda: self.show_help_dialog(2))
        self.ui.bt_help_3_3.clicked.connect(lambda: self.show_help_dialog(2))

        # mainbar page 4
        self.ui.bt_rename_4.clicked.connect(lambda: self.go_for_rename(4, i1=self.ui.rn_4_input_1.text(), i2=self.ui.rn_4_input_2.text(), i3=self.ui.rn_4_input_3.isChecked(), i4=self.ui.rn_4_input_4.text(), i5=self.ui.rn_4_input_5.text(), i6=self.ui.rn_4_input_6.text(), i7=self.ui.rn_4_input_7.text(), i8=self.ui.rn_4_input_8.text(), i9=self.ui.rn_4_input_9.text(), i10=self.ui.rn_4_input_10.currentIndex(), i11=self.ui.rn_4_input_11.text(), i12=self.ui.rn_4_input_12.text(), i13=self.ui.rn_4_input_13.text(), i14=self.ui.rn_4_input_14.text(), i15=self.ui.rn_4_input_15.text(), i16=self.ui.rn_4_input_16.text(), i17=self.ui.rn_4_input_17.currentIndex(), i18=self.ui.rn_4_input_18.text(), i19=self.ui.rn_4_input_19.text(), i20=self.ui.rn_4_input_20.text(), i21=self.ui.rn_4_input_21.text(), i22=self.ui.rn_4_input_22.text(), i23=self.ui.rn_4_input_23.currentIndex()))
        self.ui.bt_reset_4.clicked.connect(lambda: self.reset_page_4())

    def reset_page_1(self):
        self.ui.rn_1_input_1.setCurrentIndex(0)
        self.ui.rn_1_input_2.setText('')

    def reset_page_2(self):
        self.ui.rn_2_input_1.setText("")
        self.ui.rn_2_input_2.setText("")
        self.ui.rn_2_input_3.setChecked(True)

    def reset_page_3(self):
        self.ui.rn_3_input_1.setText("")
        self.ui.rn_3_input_2.setChecked(True)
        self.ui.rn_3_input_3.setCurrentIndex(0)
        self.ui.rn_3_input_4.setCurrentIndex(0)
        self.ui.rn_3_input_5.setText("")
        self.ui.rn_3_input_6.setText("")
        self.ui.rn_3_input_7.setChecked(True)
        self.ui.rn_3_input_8.setText("")
        self.ui.rn_3_input_9.setText("")

    def reset_page_4(self):
        self.ui.rn_4_input_1.setText("")
        self.ui.rn_4_input_2.setText("")
        self.ui.rn_4_input_3.setChecked(True)
        self.ui.rn_4_input_4.setText("")
        self.ui.rn_4_input_5.setText("")
        self.ui.rn_4_input_6.setText("")
        self.ui.rn_4_input_7.setText("")
        self.ui.rn_4_input_8.setText("")
        self.ui.rn_4_input_9.setText("")
        self.ui.rn_4_input_10.setCurrentIndex(0)
        self.ui.rn_4_input_11.setText("")
        self.ui.rn_4_input_12.setText("")
        self.ui.rn_4_input_13.setText("")
        self.ui.rn_4_input_14.setText("")
        self.ui.rn_4_input_15.setText("")
        self.ui.rn_4_input_16.setText("")
        self.ui.rn_4_input_17.setCurrentIndex(0)
        self.ui.rn_4_input_18.setText("")
        self.ui.rn_4_input_19.setText("")
        self.ui.rn_4_input_20.setText("")
        self.ui.rn_4_input_21.setText("")
        self.ui.rn_4_input_22.setText("")
        self.ui.rn_4_input_23.setCurrentIndex(0)

    def reset_all(self):
        self.last_selected_dir = 'C:'
        self.ui.side_input_1.setChecked(False)
        self.ui.side_input_2.setChecked(False)
        self.ui.side_input_3.setChecked(False)
        self.ui.side_input_4.setText("")
        self.ui.side_input_5.setText("")
        self.ui.side_input_6.setText("")
        self.ui.side_input_7.setText("")
        self.ui.side_input_8.setChecked(False)
        self.ui.side_input_9.setChecked(False)
        self.ui.side_input_10.setText("")
        self.ui.side_input_11.setText("")
        self.ui.side_input_12.setText("")
        self.ui.side_input_13.setText("")
        self.reset_page_1()
        self.reset_page_2()
        self.reset_page_3()
        self.reset_page_4()

    def go_for_rename(self, code, **arg):
        pass

if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.app.exec_())
