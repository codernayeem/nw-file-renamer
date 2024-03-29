from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutPage(object):
    def setupUi(self, AboutPage):
        AboutPage.setWindowModality(QtCore.Qt.ApplicationModal)
        AboutPage.setFixedHeight(350)
        AboutPage.setFixedHeight(215)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        AboutPage.setFont(font)
        AboutPage.setWindowTitle("About")
        AboutPage.setStyleSheet("QWidget{background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3e92ff, stop:.6 #3e92ff, stop:1 #3ebfff);} QLabel{background: transparent}")
        self.gridLayoutWidget = QtWidgets.QWidget(AboutPage)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 90, 331, 71))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(10)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setText("Email :")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setText("Author :")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.author = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.author.setFont(font)
        self.author.setText("Md. Nayeem")
        self.gridLayout.addWidget(self.author, 0, 1, 1, 1)
        self.email = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.email.setFont(font)
        self.email.setText("nayeem.code@gmail.com")
        self.gridLayout.addWidget(self.email, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.widget = QtWidgets.QWidget(AboutPage)
        self.widget.setGeometry(QtCore.QRect(0, 0, 351, 80))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.widget.setFont(font)
        self.widget.setStyleSheet("QWidget{background: #d5e2e8;}")
        self.icon = QtWidgets.QLabel(self.widget)
        self.icon.setGeometry(QtCore.QRect(10, 10, 64, 64))
        self.icon.setScaledContents(True)
        self.name = QtWidgets.QLabel(self.widget)
        self.name.setGeometry(QtCore.QRect(90, 16, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.name.setFont(font)
        self.version = QtWidgets.QLabel(self.widget)
        self.version.setGeometry(QtCore.QRect(95, 45, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.version.setFont(font)
        self.widget_2 = QtWidgets.QWidget(AboutPage)
        self.widget_2.setGeometry(QtCore.QRect(0, 170, 351, 51))
        self.widget_2.setStyleSheet("QWidget{background: #e6e6e6;}")
        self.thanks_label = QtWidgets.QLabel(self.widget_2)
        self.thanks_label.setGeometry(QtCore.QRect(0, 0, 271, 51))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        font.setPointSize(11)
        self.thanks_label.setFont(font)
        self.thanks_label.setText("Thanks for using this software")
        self.thanks_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ok_bt = QtWidgets.QPushButton(self.widget_2)
        self.ok_bt.setGeometry(QtCore.QRect(273, 13, 71, 25))
        self.ok_bt.setText("Ok")
        self.ok_bt.clicked.connect(AboutPage.close)
