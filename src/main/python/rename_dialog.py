from PyQt5 import QtCore, QtGui, QtWidgets
from tool import rename_file, join, get_sizebyte, sizeSince, get_c_date, get_m_date, get_splitted_by_pipe, is_valid_dir, is_valid_date_format, get_files, get_folders, check_plural, is_valid_filename, get_filename_extension
from os import system
from pathlib import Path
from threading import Thread

class RenameDialog(QtWidgets.QWidget):
    make_log = True
    make_log_error = False

    def __init__(self, parent=None):
        super(RenameDialog, self).__init__(parent)
        self.ui = Ui_RenameDialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Rename')
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui.bt_cancel.clicked.connect(self.close)
        self.ui.bt_finish.clicked.connect(self.close)
        self.ui.bt_start.clicked.connect(self.on_start_click)
        self.ui.bt_openlog.clicked.connect(self.open_log)
        self.ui.checkBox_log.toggled['bool'].connect(self.turn_on_log)

    def turn_on_log(self, i):
        self.make_log = i

    def set_data(self, folders, code, data, arg):
        self.folders = folders
        self.code = code
        self.sidedata = data
        self.arg = arg
        self.log = {}
        self.log_file = None

        self.sidedata['s4'] = get_splitted_by_pipe(self.sidedata['s4'])
        self.sidedata['s5'] = get_splitted_by_pipe(self.sidedata['s5'])
        self.sidedata['s6'] = get_splitted_by_pipe(self.sidedata['s6'])
        self.sidedata['s7'] = get_splitted_by_pipe(self.sidedata['s7'])
        self.sidedata['s10'] = get_splitted_by_pipe(self.sidedata['s10'])
        self.sidedata['s11'] = get_splitted_by_pipe(self.sidedata['s11'])
        self.sidedata['s12'] = get_splitted_by_pipe(self.sidedata['s12'])
        self.sidedata['s13'] = get_splitted_by_pipe(self.sidedata['s13'])

        self.ui.bt_finish.setEnabled(False)
        self.ui.bt_start.setEnabled(True)
        self.ui.bt_openlog.setEnabled(False)
        self.ui.bt_cancel.setEnabled(True)
        self.ui.main_text.clear()
        self.ui.txt_count_stat.setText("")

        if code == 1:
            self.ui.txt_title.setText("Change Extension")
            self.add_text_on_board("[?] - <b>Task :</b> Change Extension")
            if self.arg['i1'] == 2:
                self.add_text_on_board(f"|||||----- Action : <b>Remove Extension</b>")
            else:
                if self.arg['i1'] == 0:
                    self.add_text_on_board(f"|||||----- Action : <b>Change Extension</b>")
                else:
                    self.add_text_on_board(f"|||||----- Action : <b>Add Extension</b>")
                self.add_text_on_board(f"|||||----- Wanted extension : <b>\"{self.arg['i2']}\"</b>")
        elif code == 2:
            self.ui.txt_title.setText("Suffix Prefix")
            self.add_text_on_board("[?] - <b>Task :</b> Add Suffix Prefix")
            if self.arg['i1']:
                self.add_text_on_board(f"|||||----- Wanted Prefix : <b>\"{self.arg['i1']}\"</b>")
            if self.arg['i2']:
                self.add_text_on_board(f"|||||----- Wanted Suffix : <b>\"{self.arg['i2']}\"</b>")
            self.add_text_on_board(f"|||||----- Don't Change extension : <b>{self.arg['i3']}</b>")
        elif code == 3:
            self.ui.txt_title.setText("Serialize")
            self.add_text_on_board("[?] - <b>Task :</b> Serialize")
            self.add_text_on_board(f"|||||----- Name Format : <b>\"{self.arg['i1']}\"</b>")
            if self.arg['i5']:
                self.add_text_on_board(f"|||||----- Wanted Prefix : <b>\"{self.arg['i5']}\"</b>")
            if self.arg['i6']:
                self.add_text_on_board(f"|||||----- Wanted Suffix : <b>\"{self.arg['i6']}\"</b>")
            self.add_text_on_board(f"|||||----- Don't Change extension : <b>{self.arg['i2']}</b>")
            self.add_text_on_board(f"|||||----- Each Folder System : <b>{self.arg['i7']}</b>")
        elif code == 4:
            self.ui.txt_title.setText("Name Fixer")
            self.add_text_on_board("[?] - <b>Task :</b> Name Fix")

        self.add_text_on_board("")
        self.add_text_on_board(f"[+] - <b>Selected Folders :</b> {len(folders)}")
        for f in self.folders:
            self.add_text_on_board(f"       |-- {f}")

        self.add_text_on_board(f"")
        self.add_text_on_board(f"[!] - <b>Ready to go ... ...</b>")
        self.add_text_on_board(f"")

    def add_text_on_board(self, s):
        self.ui.main_text.append(s)

    def sort_file_list(self, folder, file_list, sort, order):
        if sort == 0:
            file_list.sort(reverse=order)
        elif sort == 1:
            file_list.sort(key=lambda file: get_sizebyte(folder, file), reverse=order)
        elif sort == 2:
            file_list.sort(key=lambda file: get_c_date(folder, file), reverse=order)
        elif sort == 3:
            file_list.sort(key=lambda file: get_m_date(folder, file), reverse=order)
        return file_list

    def on_start_click(self):
        self.ui.bt_start.setEnabled(False)
        self.ui.bt_cancel.setEnabled(False)
        self.add_text_on_board(f"<b>[+] - Renaming Started</b>")
        self.add_text_on_board(f"")

        done = 0
        fail = 0
        ignored = 0
        not_allowed = 0

        if self.make_log is None:
            try:
                self.log_file = open('logs.txt', 'w')
            except:
                self.make_log_error = True

        total_on_folders = 0
        for folder in self.folders:
            files = get_files(folder)
            if self.code == 3:
                files = self.sort_file_list(folder, files, self.arg['i3'], self.arg['i4'])
            total_on_a_folder = 0
            for a_file in files:
                filename, ext = get_filename_extension(a_file)
                status = self.check_for_allow_and_ignore(a_file, filename, ext)
                if status == 1:
                    ignored += 1
                    self.add_text_on_board(f"<b>[+] - Ignored :</b> {join(folder, a_file)}")
                elif status == 2:
                    not_allowed += 1
                    self.add_text_on_board(f"<b>[+] - Not Allowed :</b> {join(folder, a_file)}")
                else:
                    total_on_a_folder += 1
                    total_on_folders += 1

                    try:
                        new_name = self.get_new_name(a_file, filename, ext, folder, total_on_a_folder, total_on_folders)
                    except Exception as e:
                        print(e)
                        self.add_text_on_board(f"<b>[+] - Error :</b> {join(folder, a_file)}  <b>>>></b> Error on making new name")
                        self.add_text_on_board(f"<b>[+] - Stopping Renaming</b>")
                        self.do_log(False, join(folder, a_file), '')
                        break

                    if rename_file(folder, a_file, new_name):
                        done += 1
                        self.add_text_on_board(f"<b>[+] - Done :</b> {join(folder, a_file)}  <b>>></b>  {new_name}")
                        self.do_log(True, join(folder, a_file), new_name)
                    else:
                        fail += 1
                        self.do_log(False, join(folder, a_file), new_name)
                        self.add_text_on_board(f"<b>[+] - Failed :</b> {join(folder, a_file)}  <b>>></b>  {new_name}")
        self.ui.bt_finish.setEnabled(True)
        if self.make_log and not self.make_log_error:
            self.ui.bt_openlog.setEnabled(True)
        self.ui.txt_count_stat.setText("Done")
        self.add_text_on_board("")
        self.add_text_on_board(f"<b>[+] - Renaming Finished</b>")
        self.add_text_on_board("")
        total = done + fail + ignored + not_allowed
        self.add_text_on_board(f"<table> <tr> <td><b>[+] - Total</b></td> <td>:</td> <td>{total}</td> </tr> <tr> <td><b>[+] - Renamed</b></td> <td>:</td> <td>{done}</td> </tr> <tr> <td><b>[+] - Failed</b></td> <td>:</td> <td>{fail}</td> </tr> <tr> <td><b>[+] - Not Allowed</b></td> <td>:</td> <td>{not_allowed}</td> </tr> <tr> <td><b>[+] - Ignored</b></td> <td>:</td> <td>{ignored}</td> </tr> </table>")
        self.add_text_on_board("")
        if self.log_file is not None and self.make_log:
            self.log_file.close()
            if self.make_log_error:
                self.add_text_on_board(f"[+] - <b>Log Failed</b>")
            else:
                self.add_text_on_board(f"[+] - Log path : <b>{str(Path('logs.txt').absolute())}</b>")
        self.add_text_on_board(f"[+] - Press Finish to quit")

    def check_for_allow_and_ignore(self, fl_name, filename, ext):
        if self.sidedata['s8']:
            if (self.sidedata['s9'] and not ext) or (self.sidedata['s10'] and ext in self.sidedata['s10']):
                return 1
            if self.sidedata['s11']:
                for i in self.sidedata['s11']:
                    if filename.startswith(i):
                        return 1
            if self.sidedata['s12']:
                for i in self.sidedata['s12']:
                    if filename.endswith(i):
                        return 1
            if self.sidedata['s13']:
                for i in self.sidedata['s13']:
                    if i in filename:
                        return 1

        if self.sidedata['s2']:
            add_item = False
            if (self.sidedata['s3'] and not ext) or (self.sidedata['s4'] and ext in self.sidedata['s4']):
                add_item = True
            elif self.sidedata['s5']:
                for i in self.sidedata['s5']:
                    if filename.startswith(i):
                        add_item = True
                        break
            elif self.sidedata['s6']:
                for i in self.sidedata['s6']:
                    if filename.endswith(i):
                        add_item = True
                        break
            elif self.sidedata['s7']:
                for i in self.sidedata['s7']:
                    if i in filename:
                        add_item = True
                        break
            if not add_item:
                return 2
        return 0

    def get_new_name(self, fl_name, filename, ext, folder, no_on_folder, no_on_total):
        new_name = None

        if self.code == 1:
            if self.arg['i1'] == 0:
                new_name = filename + '.' + self.arg['i2']
            elif self.arg['i1'] == 1:
                new_name = fl_name + '.' + self.arg['i2']
            else:
                new_name = filename
        elif self.code == 2:
            if not self.arg['i3'] or not ext:
                new_name = self.arg['i1'] + fl_name + self.arg['i2']
            else:
                new_name = self.arg['i1'] + filename + self.arg['i2'] + '.' + ext
        elif self.code == 3:
            if self.arg["i7"]:
                no = no_on_folder
            else:
                no = no_on_total
            formatted_name = self.arg["i1"]
            if "<no>" in formatted_name:
                formatted_name = formatted_name.replace("<no>", str(no))
            if "<file>" in formatted_name:
                formatted_name = formatted_name.replace("<file>", fl_name)
            if "<filename>" in formatted_name:
                formatted_name = formatted_name.replace("<filename>", filename)
            if "<ext>" in formatted_name:
                formatted_name = formatted_name.replace("<ext>", ext)
            if "<size>" in formatted_name:
                formatted_name = formatted_name.replace("<size>", sizeSince(get_sizebyte(folder, fl_name)))
            if "<sizeb>" in formatted_name:
                formatted_name = formatted_name.replace("<sizeb>", str(get_sizebyte(folder, fl_name)))
            if "<c_date>" in formatted_name:
                formatted_name = formatted_name.replace("<c_date>", get_c_date(folder, fl_name).strftime(self.arg['i8']))
            if "<m_date>" in formatted_name:
                formatted_name = formatted_name.replace("<m_date>", get_m_date(folder, fl_name).strftime(self.arg['i9']))
            new_name = self.arg["i5"] + formatted_name + self.arg["i6"]
            if self.arg["i2"] and ext:
                new_name += '.' + ext
        elif self.code == 4:
            if self.arg['i3']:
                new_name = filename
            else:
                new_name = fl_name

            if self.arg['i4']:
                new_name = new_name.replace(self.arg['i4'], self.arg['i5'])
            if self.arg['i7'] is not None or self.arg['i8'] is not None:
                if self.arg['i7'] is None:
                    new_name = self.arg['i6'] + new_name[self.arg['i8']+1:]
                elif self.arg['i8'] is None:
                    new_name = new_name[:self.arg['i7']] + self.arg['i6']
                else:
                    new_name = new_name[:self.arg['i7']] + self.arg['i6'] + new_name[self.arg['i8']+1:]
            if self.arg['i9']:
                new_name = new_name.replace(self.arg['i9'], '')
            if self.arg['i11']:
                index = new_name.find(self.arg['i11'])
                if index != -1:
                    if self.arg['i10'] == 0:
                        if self.arg['i12'] is None:
                            new_name = new_name[index:]
                        elif index - self.arg['i12'] >= 0:
                            new_name = new_name[:index - self.arg['i12']] + new_name[index:]
                    else:
                        if self.arg['i12'] is None:
                            new_name = new_name[:index+len(self.arg['i11'])]
                        else:
                            new_name = new_name[:index+len(self.arg['i11'])] + new_name[index+len(self.arg['i11'])+self.arg['i12']:]
            if self.arg['i13'] is not None or self.arg['i14'] is not None:
                if self.arg['i14'] is None:
                    new_name = new_name[:self.arg['i13']]
                elif self.arg['i13'] is None:
                    new_name = new_name[self.arg['i14']+1:]
                else:
                    new_name = new_name[:self.arg['i13']] + new_name[self.arg['i14']+1:]
            if self.arg['i15']:
                new_name = new_name[:self.arg['i16']] + self.arg['i15'] + new_name[self.arg['i16']:]
            if self.arg['i18']:
                index = new_name.find(self.arg['i18'])
                if index != -1:
                    if self.arg['i17'] == 0:
                        new_name = new_name[:index] + self.arg['i19'] + new_name[index:]
                    else:
                        new_name = new_name[:index+len(self.arg['i18'])] + self.arg['i19'] + new_name[index+len(self.arg['i18']):]

            if self.arg['i20'] is not None:
                if self.arg['i22'] is None:
                    new_name = new_name[:self.arg['i20']] + new_name[self.arg['i21']:] + new_name[self.arg['i20']:]
                elif self.arg['i21'] is None:
                    new_name = new_name[:self.arg['i20']] + new_name[:self.arg['i22']+1] + new_name[self.arg['i20']:]
                else:
                    new_name = new_name[:self.arg['i20']] + new_name[self.arg['i21']:self.arg['i22']+1] + new_name[self.arg['i20']:]

            new_name = self.arg['i1'] + new_name + self.arg['i2']
            if self.arg['i3'] and ext:
                new_name = new_name + '.' + ext

        return new_name

    def do_log(self, succes, path, newname):
        if self.make_log and not self.make_log_error:
            try:
                self.log_file.write(f'{succes}  "{path}" "{newname}"\n')
            except:
                try:
                    self.log_file.write(f'{succes}  "<Cannot write filepath and newname>"\n')
                except:
                    self.make_log_error = True

    def open_log(self):
        try:
            Thread(target=lambda: system('logs.txt')).start()
        except:
            pass

class Ui_RenameDialog(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(580, 404)
        font = QtGui.QFont()
        font.setPointSize(11)
        Form.setFont(font)
        self.gridlayout = QtWidgets.QGridLayout(Form)
        self.gridlayout.setObjectName("gridlayout")
        self.checkBox_log = QtWidgets.QCheckBox(Form)
        self.checkBox_log.setText("Make Log")
        self.checkBox_log.setChecked(True)
        self.checkBox_log.setObjectName("checkBox_log")
        self.gridlayout.addWidget(self.checkBox_log, 2, 0, 1, 1)
        self.main_text = QtWidgets.QTextBrowser(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.main_text.setFont(font)
        self.main_text.setObjectName("main_text")
        self.gridlayout.addWidget(self.main_text, 1, 0, 1, 6)
        self.txt_title = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(14)
        self.txt_title.setFont(font)
        self.txt_title.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_title.setObjectName("txt_title")
        self.gridlayout.addWidget(self.txt_title, 0, 0, 1, 5)
        self.bt_finish = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_finish.sizePolicy().hasHeightForWidth())
        self.bt_finish.setSizePolicy(sizePolicy)
        self.bt_finish.setText("Finish")
        self.bt_finish.setObjectName("bt_finish")
        self.gridlayout.addWidget(self.bt_finish, 2, 4, 1, 1)
        self.bt_start = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_start.sizePolicy().hasHeightForWidth())
        self.bt_start.setSizePolicy(sizePolicy)
        self.bt_start.setText("Start")
        self.bt_start.setObjectName("bt_start")
        self.gridlayout.addWidget(self.bt_start, 2, 2, 1, 1)
        self.bt_cancel = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_cancel.sizePolicy().hasHeightForWidth())
        self.bt_cancel.setSizePolicy(sizePolicy)
        self.bt_cancel.setText("Cancel")
        self.bt_cancel.setObjectName("bt_cancel")
        self.gridlayout.addWidget(self.bt_cancel, 2, 1, 1, 1)
        self.txt_count_stat = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_count_stat.sizePolicy().hasHeightForWidth())
        self.txt_count_stat.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.txt_count_stat.setFont(font)
        self.txt_count_stat.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_count_stat.setObjectName("txt_count_stat")
        self.gridlayout.addWidget(self.txt_count_stat, 0, 5, 1, 1)
        self.bt_openlog = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_openlog.sizePolicy().hasHeightForWidth())
        self.bt_openlog.setSizePolicy(sizePolicy)
        self.bt_openlog.setText("Open Log")
        self.bt_openlog.setObjectName("bt_openlog")
        self.gridlayout.addWidget(self.bt_openlog, 2, 3, 1, 1)

        Form.setTabOrder(self.main_text, self.checkBox_log)
        Form.setTabOrder(self.checkBox_log, self.bt_cancel)
        Form.setTabOrder(self.bt_cancel, self.bt_start)
        Form.setTabOrder(self.bt_start, self.bt_openlog)
        Form.setTabOrder(self.bt_openlog, self.bt_finish)
